import Sentiment from 'sentiment';

/**
 * @typedef {Object} SentimentResult
 * @property {string} product
 * @property {number} avg_sentiment
 * @property {number} positive_count
 * @property {number} negative_count
 * @property {number} neutral_count
 * @property {number} total_reviews
 * @property {number} dissatisfaction_index
 * @property {[string, number][]} top_complaints
 * @property {number} risk_score
 */

class RealityEngine {
    constructor() {
        this.analyzer = new Sentiment();
        this.financialKeywords = {
            'hidden_charges': ['hidden charge', 'hidden fee', 'undisclosed cost', 'extra charge', 'deducted money'],
            'poor_returns': ['poor return', 'low return', 'bad return', 'not getting returns', 'loss', 'underperforming'],
            'misleading': ['mislead', 'false promise', 'lied', 'fake promise', 'scam', 'cheat'],
            'service_issues': ['bad service', 'poor service', 'no response', 'ignore', 'rude', 'unhelpful'],
            'difficult_exit': ['cannot exit', 'exit problem', 'withdrawal issue', 'lock in', 'stuck'],
            'transparency': ['fine print', 'terms and conditions', 'complicated', 'confusing', 'not clear']
        };
    }

    /**
     * Analyze a single text string
     * @param {string} text 
     */
    analyzeText(text) {
        const result = this.analyzer.analyze(text);
        // Normalize score to 0-1 range roughly (AFINN scores usually -5 to 5)
        // -5 -> 0, 0 -> 0.5, 5 -> 1
        const normalized = Math.max(0, Math.min(1, (result.score + 5) / 10));

        let label = 'NEUTRAL';
        if (result.score > 0) label = 'POSITIVE';
        if (result.score < 0) label = 'NEGATIVE';

        return {
            score: result.score,
            normalized,
            label,
            tokens: result.tokens
        };
    }

    /**
     * Analyze batch of reviews for a product
     * @param {Object[]} reviews - Array of review objects { product: string, text: string, ... }
     * @param {string} productName 
     * @returns {SentimentResult}
     */
    analyzeProduct(reviews, productName) {
        const productReviews = reviews.filter(r => r.product === productName);

        if (productReviews.length === 0) {
            return this._getEmptyResult(productName);
        }

        let totalScore = 0;
        let positive = 0;
        let negative = 0;
        let neutral = 0;
        const negativeTexts = [];

        productReviews.forEach(review => {
            const analysis = this.analyzeText(review.text);
            totalScore += analysis.normalized;

            if (analysis.label === 'POSITIVE') positive++;
            else if (analysis.label === 'NEGATIVE') {
                negative++;
                negativeTexts.push(review.text.toLowerCase());
            }
            else neutral++;
        });

        const total = productReviews.length;
        const avgSentiment = totalScore / total;
        const dissatisfactionIndex = (negative / total) * 100;

        // Topic Detection on negative texts
        const complaintCounts = {};
        negativeTexts.forEach(text => {
            for (const [category, keywords] of Object.entries(this.financialKeywords)) {
                if (keywords.some(k => text.includes(k))) {
                    const readableCat = category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
                    complaintCounts[readableCat] = (complaintCounts[readableCat] || 0) + 1;
                }
            }
        });

        const topComplaints = Object.entries(complaintCounts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 3);

        return {
            product: productName,
            avg_sentiment: avgSentiment,
            positive_count: positive,
            negative_count: negative,
            neutral_count: neutral,
            total_reviews: total,
            dissatisfaction_index: dissatisfactionIndex,
            top_complaints: topComplaints.length ? topComplaints : [['General Dissatisfaction', negative]],
            risk_score: Math.min(1.0, dissatisfactionIndex / 100)
        };
    }

    _getEmptyResult(productName) {
        return {
            product: productName,
            avg_sentiment: 0.5,
            positive_count: 0,
            negative_count: 0,
            neutral_count: 0,
            total_reviews: 0,
            dissatisfaction_index: 0,
            top_complaints: [],
            risk_score: 0
        };
    }
}

export const realityEngine = new RealityEngine();
