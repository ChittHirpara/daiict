import mongoose from 'mongoose';

const ReportSchema = new mongoose.Schema({
    product_name: {
        type: String,
        required: [true, 'Please provide a product name'],
    },
    issuer: {
        type: String,
    },
    upload_date: {
        type: Date,
        default: Date.now,
    },
    risk_level: {
        type: String,
        enum: ['Low', 'Moderate', 'High', 'Critical', 'Unknown'],
        default: 'Unknown',
    },
    confidence: {
        type: Number,
        default: 0,
    },
    key_features: {
        type: [String],
        default: [],
    },
    promised_returns: {
        type: String,
    },
    extracted_data: {
        type: mongoose.Schema.Types.Mixed, // Stores the full raw extraction object
    },
    filename: {
        type: String, // Original filename or generated ID
    }
});

export default mongoose.models.Report || mongoose.model('Report', ReportSchema);
