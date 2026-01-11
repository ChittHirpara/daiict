/**
 * @typedef {Object} Mismatch
 * @property {string} promise_aspect
 * @property {string} complaint_topic
 * @property {number} severity
 * @property {string[]} evidence
 * @property {string} mismatch_type
 * @property {number} confidence
 */

/**
 * @typedef {Object} GapAnalysisResult
 * @property {string} product_name
 * @property {number} promise_confidence
 * @property {number} sentiment_score
 * @property {number} dissatisfaction_index
 * @property {Mismatch[]} mismatches
 * @property {number} overall_risk_score
 * @property {string} risk_level
 * @property {string[]} recommendations
 */

class GapAnalyzer {
    constructor() {
        this.patterns = {
            returns: {
                promise: ['return', 'yield', 'profit', 'gain', 'earn'],
                complaint: ['no return', 'low return', 'loss', 'negative return', 'poor returns'],
                weight: 1.2
            },
            risk: {
                promise: ['low risk', 'safe', 'secure', 'protected', 'guaranteed'],
                complaint: ['risky', 'lost money', 'dangerous', 'unsafe', 'fraud'],
                weight: 1.3
            },
            fees: {
                promise: ['no charge', 'low fee', 'free', 'no hidden', 'transparent'],
                complaint: ['hidden charge', 'extra fee', 'unexpected cost', 'high fees'],
                weight: 1.0
            },
            liquidity: {
                promise: ['easy exit', 'liquid', 'withdraw anytime', 'no lock-in'],
                complaint: ['cannot exit', 'locked', 'withdrawal problem', 'stuck'],
                weight: 0.9
            }
        };
    }

    /**
     * Detect mismatches
     * @param {Object} promise 
     * @param {Object} sentiment 
     * @returns {Mismatch[]}
     */
    detectMismatches(promise, sentiment) {
        const mismatches = [];

        // Construct searchable text
        const promiseText = [
            promise.investment_objective,
            promise.promised_returns,
            promise.risk_category,
            ...promise.key_features,
            ...promise.warnings
        ].join(' ').toLowerCase();

        const complaintTopics = sentiment.top_complaints || [];
        const complaintText = complaintTopics.map(([topic]) => topic).join(' ').toLowerCase();

        for (const [aspect, pattern] of Object.entries(this.patterns)) {
            const hasPromise = pattern.promise.some(term => promiseText.includes(term));
            const hasComplaint = pattern.complaint.some(term => complaintText.includes(term));

            if (hasPromise && hasComplaint) {
                mismatches.push({
                    promise_aspect: aspect.toUpperCase(),
                    complaint_topic: complaintTopics.find(([t]) => pattern.complaint.some(c => t.toLowerCase().includes(c)))?.[0] || 'General Issue',
                    severity: Math.min(1.0, 0.5 * pattern.weight + (sentiment.dissatisfaction_index / 200)),
                    evidence: [
                        `Promised features related to ${aspect}`,
                        `Customers specifically complained about ${aspect}`
                    ],
                    mismatch_type: 'direct_contradiction',
                    confidence: 0.8
                });
            }
        }

        return mismatches;
    }

    calculateRiskScore(mismatches, sentiment) {
        const baseScore = mismatches.length > 0
            ? mismatches.reduce((acc, m) => acc + m.severity, 0) / mismatches.length
            : 0.2;

        const sentimentFactor = sentiment.dissatisfaction_index / 100;
        return Math.min(1.0, (baseScore * 0.7) + (sentimentFactor * 0.3));
    }

    determineRiskLevel(score) {
        if (score < 0.3) return 'low';
        if (score < 0.6) return 'medium';
        if (score < 0.8) return 'high';
        return 'critical';
    }

    generateRecommendations(riskLevel, mismatches) {
        const recs = [];
        if (riskLevel === 'critical') recs.push('🚨 IMMEDIATE INVESTIGATION REQUIRED');
        if (riskLevel === 'high') recs.push('⚠️ High priority review needed');

        mismatches.forEach(m => {
            recs.push(`Verify discrepancy in ${m.promise_aspect} claims`);
        });

        recs.push('Improve transparency in marketing materials');
        return recs;
    }

    analyze(promise, sentiment) {
        const mismatches = this.detectMismatches(promise, sentiment);
        const overallRiskScore = this.calculateRiskScore(mismatches, sentiment);
        const riskLevel = this.determineRiskLevel(overallRiskScore);
        const recommendations = this.generateRecommendations(riskLevel, mismatches);

        return {
            product_name: promise.product_name,
            promise_confidence: promise.extraction_confidence,
            sentiment_score: sentiment.avg_sentiment,
            dissatisfaction_index: sentiment.dissatisfaction_index,
            mismatches,
            overall_risk_score: overallRiskScore,
            risk_level: riskLevel,
            recommendations
        };
    }
}

export const gapAnalyzer = new GapAnalyzer();
