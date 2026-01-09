import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Helper to load env vars before importing modules that need them
function loadEnv() {
    try {
        const envPath = path.resolve(process.cwd(), '.env.local');
        if (fs.existsSync(envPath)) {
            const envConfig = fs.readFileSync(envPath, 'utf8');
            envConfig.split('\n').forEach(line => {
                const [key, value] = line.split('=');
                if (key && value && !key.startsWith('#')) {
                    process.env[key.trim()] = value.trim();
                }
            });
            console.log('Loaded .env.local');
        }
    } catch (e) {
        console.error('Error loading .env.local:', e);
    }
}

loadEnv();

// Import pipeline AFTER loading env vars so dbConnect gets the URI
import { pipeline } from '../lib/engines/pipeline.js';

async function main() {
    try {
        console.log("Running pipeline verification...");
        const results = await pipeline.run();
        console.log("✅ Pipeline success. Result count:", results.length);
        process.exit(0);
    } catch (e) {
        console.error("❌ Pipeline failed:", e);
        process.exit(1);
    }
}

main();
