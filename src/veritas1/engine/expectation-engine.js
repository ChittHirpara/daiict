import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const pdf = require('pdf-parse');

/**
 * @typedef {Object} FinancialPromise
 * @property {string} product_name
 * @property {string} issuer
 * @property {string} investment_objective
 * @property {string|null} promised_returns
 * @property {string} risk_category
 * @property {string|null} lock_in_period
 * @property {string|null} exit_load
 * @property {string|null} min_investment
 * @property {string[]} key_features
 * @property {string[]} warnings
 * @property {number} extraction_confidence
 */

export class ExpectationEngine {
    constructor() {
        this.patterns = {
            returns: [
                /(\d+(\.\d+)?)%\s*(p\.a\.|per annum|annual|yearly|return|yield)/i,
                /returns?\s*(?:of|up to|around|@)\s*(\d+(\.\d+)?)%/i,
                /(?:earn|yield|get)\s*(?:up to\s*)?(\d+(\.\d+)?)%/i,
                /(\d+(\.\d+)?)%\s*interest/i
            ],
            risk: [
                /(low|moderate|high|very high)\s*risk/i,
                /risk\s*(?:level|category|profile):?\s*(low|moderate|high)/i,
                /capital\s+protection/i,
                /principal\s+guaranteed/i,
                /safe\s+investment/i
            ],
            lock_in: [
                /lock[-\s]*in\s*(?:period)?:?\s*(\d+)\s*(years?|yrs?|months?|mths?)/i,
                /maturity[:\s]*(\d+)\s*(years?|yrs?|months?|mths?)/i,
                /minimum\s*tenure:?\s*(\d+)\s*(years?|yrs?|months?|mths?)/i,
                /tenure:?\s*(\d+)\s*(years?|yrs?|months?|mths?)/i,
                /duration:?\s*(\d+)\s*(years?|yrs?|months?|mths?)/i
            ],
            fees: [
                /exit\s*load:?\s*(\d+(\.\d+)?)%/i,
                /early\s*withdrawal\s*charge:?\s*(\d+(\.\d+)?)%/i,
                /management\s*fee:?\s*(\d+(\.\d+)?)%/i,
                /fee:?\s*(\d+(\.\d+)?)%/i
            ],
            investment: [
                /minimum\s*investment:?\s*[₹$]?\s*(\d+(?:,\d+)*(?:\.\d+)?)/i,
                /invest\s*as\s*low\s*as\s*[₹$]?\s*(\d+(?:,\d+)*(?:\.\d+)?)/i,
                /min\.?\s*inv\.?:?\s*[₹$]?\s*(\d+(?:,\d+)*(?:\.\d+)?)/i,
                /starts\s*at\s*[₹$]?\s*(\d+(?:,\d+)*(?:\.\d+)?)/i
            ]
        };
    }

    /**
     * Extract promises from raw text
     * @param {string} text 
     * @param {Object} productInfo 
     * @returns {FinancialPromise}
     */
    extractFromText(text, productInfo = {}) {
        const extraction = {
            product_name: productInfo.product_name || 'Unknown',
            issuer: productInfo.issuer || 'Unknown',
            investment_objective: '',
            promised_returns: null,
            risk_category: 'Unknown',
            lock_in_period: null,
            exit_load: null,
            min_investment: null,
            key_features: [],
            warnings: [],
            extraction_confidence: 0.0,
            raw_text: text || '' // Include the raw text
        };

        // Split sentences generally
        const sentences = text.split('.').map(s => s.trim()).filter(s => s.length > 0);

        // Simple objective extraction (usually first sentence)
        if (sentences.length > 0) {
            extraction.investment_objective = sentences[0];
        }

        // Extract Features and Warnings using keywords
        sentences.forEach(sent => {
            const lower = sent.toLowerCase();
            if (['feature', 'benefit', 'advantage', 'offer', 'highlight', 'why invest'].some(w => lower.includes(w))) {
                if (sent.split(' ').length < 40) extraction.key_features.push(sent);
            }
            if (['warning', 'risk', 'caution', 'note:', 'important:', 'disclaimer', 'subject to'].some(w => lower.includes(w))) {
                extraction.warnings.push(sent);
            }
        });

        // Fallback: If no features found, take meaningful sentences
        if (extraction.key_features.length === 0) {
            extraction.key_features = sentences
                .filter(s => s.length > 30 && s.length < 150 && !s.toLowerCase().includes('risk'))
                .slice(0, 3);
        }

        // Extract structured data using Regex
        for (const [category, patterns] of Object.entries(this.patterns)) {
            for (const pattern of patterns) {
                const matches = text.match(new RegExp(pattern, 'gi'));
                if (matches) {
                    for (const matchStr of matches) {
                        const match = matchStr.match(pattern); // Execute again to get groups
                        if (!match) continue;

                        if (category === 'returns') extraction.promised_returns = `${match[1]}%`;
                        else if (category === 'risk') {
                            if (match[1]) {
                                extraction.risk_category = match[1].charAt(0).toUpperCase() + match[1].slice(1);
                            } else {
                                extraction.risk_category = 'Low';
                            }
                        }
                        else if (category === 'lock_in') extraction.lock_in_period = `${match[1]} ${match[2] || 'years'}`;
                        else if (category === 'fees') extraction.exit_load = `${match[1]}%`;
                        else if (category === 'investment') extraction.min_investment = `₹${match[1]}`;
                    }
                }
            }
        }

        // Calculate Confidence
        let factors = 0;
        if (extraction.investment_objective) factors++;
        if (extraction.promised_returns) factors++;
        if (extraction.risk_category !== 'Unknown') factors++;
        if (extraction.key_features.length > 0) factors++;
        if (extraction.warnings.length > 0) factors++;

        extraction.extraction_confidence = factors / 5;

        return extraction;
    }

    /**
     * Process a PDF file
     * @param {string} filePath 
     * @param {string} [originalFilename] Optional original filename to use for product extraction
     * @returns {Promise<FinancialPromise>}
     */
    async extractFromPdf(filePath, originalFilename = null) {
        try {
            const dataBuffer = fs.readFileSync(filePath);
            const data = await pdf(dataBuffer);
            const text = data.text.replace(/\s+/g, ' ').trim();

            const filename = (originalFilename || path.basename(filePath));
            const productName = filename.replace('.pdf', '').replace(/_/g, ' ').replace(/^\d+_/, ''); // Remove timestamp prefix if present

            return this.extractFromText(text, { product_name: productName, issuer: 'Detected from PDF' });
        } catch (error) {
            console.error(`Error reading PDF ${filePath}:`, error);
            return null;
        }
    }

    /**
     * Batch process a directory
     * @param {string} dirPath 
     * @returns {Promise<FinancialPromise[]>}
     */
    async batchExtract(dirPath) {
        const results = [];
        if (!fs.existsSync(dirPath)) return results;

        const files = fs.readdirSync(dirPath);

        for (const file of files) {
            if (file.endsWith('.pdf')) {
                const result = await this.extractFromPdf(path.join(dirPath, file));
                if (result) results.push(result);
            } else if (file.endsWith('.json')) {
                // Handle mock json files
                const content = JSON.parse(fs.readFileSync(path.join(dirPath, file), 'utf-8'));
                // Create pseudo-text from JSON
                const text = Object.entries(content).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join('. ');
                results.push(this.extractFromText(text, content));
            }
        }
        return results;
    }
}

export const expectationEngine = new ExpectationEngine();
