import mongoose from 'mongoose';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Manually load .env.local
try {
    const envPath = path.resolve(process.cwd(), '.env.local');
    if (fs.existsSync(envPath)) {
        const envConfig = fs.readFileSync(envPath, 'utf8');
        envConfig.split('\n').forEach(line => {
            const [key, value] = line.split('=');
            if (key && value) {
                process.env[key.trim()] = value.trim();
            }
        });
        console.log('Loaded .env.local');
    } else {
        console.error('.env.local file not found!');
        process.exit(1);
    }
} catch (e) {
    console.error('Error loading .env.local:', e);
}

const MONGODB_URI = process.env.MONGODB_URI;

if (!MONGODB_URI) {
    console.error('MONGODB_URI is missing from .env.local');
    process.exit(1);
}

console.log('Attempting to connect to MongoDB...');
// Mask the URI for safety in logs
console.log(`URI: ${MONGODB_URI.replace(/:([^:@]+)@/, ':****@')}`);

mongoose.connect(MONGODB_URI)
    .then(() => {
        console.log('✅ SUCCESS: Connected to MongoDB successfully!');
        return mongoose.connection.close();
    })
    .catch(err => {
        console.error('❌ FAILED: Could not connect to MongoDB.');
        // console.error(err); // Try to show less verbose error first
        if (err.name === 'MongooseServerSelectionError') {
            console.error('Error: Could not connect to any servers in your MongoDB Atlas cluster.');
            console.error('Possible causes:');
            console.error('1. IP Whitelist: Did you add your current IP to MongoDB Atlas Network Access?');
            console.error('2. Bad Connection String: Is the cluster address correct?');
        } else {
            console.error('Error:', err.message);
        }
        process.exit(1);
    });
