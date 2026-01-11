import { NextResponse } from 'next/server';
import dbConnect from '@/veritas1/db/connection';
import Report from '@/veritas1/db/Report';

export async function GET(request) {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
        return NextResponse.json({ error: 'Report ID not specified' }, { status: 400 });
    }

    try {
        await dbConnect();
        const report = await Report.findById(id);

        if (!report) {
            return NextResponse.json({ error: 'Report not found' }, { status: 404 });
        }

        const data = report.extracted_data;

        return new NextResponse(JSON.stringify(data, null, 2), {
            headers: {
                'Content-Type': 'application/json',
                'Content-Disposition': `attachment; filename="${report.product_name || 'report'}.json"`,
            },
        });
    } catch (error) {
        console.error(error);
        return NextResponse.json({ error: 'Database Error' }, { status: 500 });
    }
}
