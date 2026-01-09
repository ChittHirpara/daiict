import { NextResponse } from 'next/server';
import { ExpectationEngine } from '@/lib/engines/expectation-engine';
import dbConnect from '@/lib/db';
import Report from '@/models/Report';
import fs from 'fs';
import path from 'path';

// Disable default body parser to handle FormData
export const config = {
    api: {
        bodyParser: false,
    },
};

export async function POST(req) {
    try {
        const formData = await req.formData();
        const file = formData.get('file');

        if (!file) {
            return NextResponse.json({ error: "No file provided" }, { status: 400 });
        }

        // Convert file to buffer
        const arrayBuffer = await file.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);

        // Save temporarily (optional, but good for debugging/caching)
        const tempDir = path.join(process.cwd(), 'tmp');
        if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir);
        const tempPath = path.join(tempDir, `upload_${Date.now()}.pdf`);
        fs.writeFileSync(tempPath, buffer);

        // Run processing
        // Note: We are using a fresh instance since we're in an API context
        const engine = new ExpectationEngine();

        // In a real scenario, we'd pass the buffer directly if the engine supported it, 
        // or the path. The current engine implementation likely expects a path.
        const result = await engine.extractFromPdf(tempPath);

        // Save result to MongoDB
        await dbConnect();

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

        const report = await Report.create({
            product_name: result.product_name,
            issuer: result.issuer,
            risk_level: result.risk_category || 'Unknown',
            confidence: result.extraction_confidence,
            key_features: result.key_features,
            promised_returns: result.promised_returns,
            extracted_data: result,
            filename: `extraction_${timestamp}.json`
        });

        const enrichedResult = {
            ...result,
            id: report._id.toString(),
            date: report.upload_date.toLocaleDateString(),
            type: 'Extraction Report'
        };

        // Cleanup
        try {
            fs.unlinkSync(tempPath);
        } catch (e) {
            console.error("Failed to cleanup temp file:", e);
        }

        return NextResponse.json(enrichedResult);

    } catch (error) {
        console.error("PDF Processing Error:", error);
        return NextResponse.json({ error: "Failed to process PDF", details: error.message }, { status: 500 });
    }
}
