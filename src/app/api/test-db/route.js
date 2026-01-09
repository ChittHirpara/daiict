import { NextResponse } from 'next/server';
import dbConnect from '@/lib/db';
import Report from '@/models/Report';

export async function GET() {
    try {
        await dbConnect();

        // 1. Create a minimal test document
        const testReport = await Report.create({
            product_name: "DB Connectivity Test Request",
            issuer: "Test Issuer",
            risk_level: "Low",
            filename: "test_db_verification.json"
        });

        // 2. Fetch it back to confirm it was stored
        const retrievedReport = await Report.findById(testReport._id);

        if (!retrievedReport) {
            throw new Error("Document was created but could not be retrieved.");
        }

        // 3. Delete it to clean up
        await Report.findByIdAndDelete(testReport._id);

        return NextResponse.json({
            status: "success",
            message: "Database connection verified securely.",
            details: {
                test_id: testReport._id,
                storage_confirmed: true,
                cleanup_confirmed: true
            }
        });

    } catch (error) {
        console.error("Database Test Error:", error);
        return NextResponse.json({
            status: "error",
            message: "Database check failed",
            error: error.message
        }, { status: 500 });
    }
}
