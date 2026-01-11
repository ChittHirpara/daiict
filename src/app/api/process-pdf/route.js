import { NextResponse } from 'next/server';
import { ExpectationEngine } from '@/veritas1/engine/expectation-engine';
import dbConnect from '@/veritas1/db/connection';
import Report from '@/veritas1/db/Report';
import fs from 'fs';
import path from 'path';

// Disable default body parser to handle FormData
export const config = {
    api: {
        bodyParser: false,
    },
};

export async function POST(req) {
    let tempPath = null;
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
        tempPath = path.join(tempDir, `upload_${Date.now()}.pdf`);
        fs.writeFileSync(tempPath, buffer);

        // Run processing
        // Note: We are using a fresh instance since we're in an API context
        const engine = new ExpectationEngine();

        // In a real scenario, we'd pass the buffer directly if the engine supported it, 
        // or the path. The current engine implementation likely expects a path.
        const result = await engine.extractFromPdf(tempPath, file.name);

        // Validate result
        if (!result || !result.product_name) {
            // Cleanup temp file before returning error
            try {
                fs.unlinkSync(tempPath);
            } catch (e) {
                console.error("Failed to cleanup temp file:", e);
            }
            return NextResponse.json({
                error: "Failed to extract data from PDF",
                details: "The PDF may be corrupted, empty, or in an unsupported format"
            }, { status: 422 });
        }

        // Save result to MongoDB
        try {
            await dbConnect();

            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

            const report = await Report.create({
                product_name: result.product_name || 'Unknown Product',
                issuer: result.issuer || 'Unknown',
                risk_level: result.risk_category || 'Unknown',
                confidence: result.extraction_confidence || 0,
                key_features: result.key_features || [],
                promised_returns: result.promised_returns || null,
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
        } catch (dbError) {
            console.error("Database error:", dbError);
            // Cleanup temp file
            try {
                fs.unlinkSync(tempPath);
            } catch (e) {
                console.error("Failed to cleanup temp file:", e);
            }
            // Return the result even if database save fails
            return NextResponse.json({
                ...result,
                id: `temp-${Date.now()}`,
                date: new Date().toLocaleDateString(),
                type: 'Extraction Report',
                warning: 'Failed to save to database, but extraction succeeded'
            });
        }

    } catch (error) {
        console.error("PDF Processing Error:", error);

        // Cleanup temp file if it exists
        try {
            if (tempPath && fs.existsSync(tempPath)) {
                fs.unlinkSync(tempPath);
            }
        } catch (e) {
            console.error("Failed to cleanup temp file:", e);
        }

        // Return user-friendly error messages
        let errorMessage = "Failed to process PDF";
        let errorDetails = error.message;

        if (error.message.includes('ENOENT') || error.message.includes('no such file')) {
            errorMessage = "File not found";
            errorDetails = "The uploaded file could not be accessed";
        } else if (error.message.includes('permission denied')) {
            errorMessage = "Permission denied";
            errorDetails = "Unable to access the uploaded file";
        } else if (error.message.includes('invalid') || error.message.includes('parse')) {
            errorMessage = "Invalid PDF format";
            errorDetails = "The file may be corrupted or not a valid PDF";
        }

        return NextResponse.json({
            error: errorMessage,
            details: errorDetails
        }, { status: 500 });
    }
}
