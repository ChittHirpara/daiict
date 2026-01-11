import { expectationEngine } from '@/veritas1/engine/expectation-engine';
import { NextResponse } from 'next/server';

export async function POST(request) {
    try {
        const formData = await request.formData();
        const file = formData.get('file');

        if (!file) {
            return NextResponse.json(
                { error: 'No file uploaded' },
                { status: 400 }
            );
        }

        // Convert file to buffer
        const bytes = await file.arrayBuffer();
        const buffer = Buffer.from(bytes);

        // Process PDF
        const result = await expectationEngine.extractFromBuffer(buffer, file.name);

        if (!result) {
            return NextResponse.json(
                { error: 'Failed to extract data from PDF' },
                { status: 500 }
            );
        }

        return NextResponse.json(result);
    } catch (error) {
        console.error('PDF Processing Error:', error);
        return NextResponse.json(
            { error: 'Internal Server Error', details: error.message },
            { status: 500 }
        );
    }
}
