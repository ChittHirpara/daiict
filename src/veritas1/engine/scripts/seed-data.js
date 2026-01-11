import fs from 'fs';
import path from 'path';
import { faker } from '@faker-js/faker';
import Papa from 'papaparse';

const PRODUCTS = [
    "Alpha Growth Mutual Fund",
    "SecureLife Insurance Policy",
    "MaxReturns Fixed Deposit",
    "WealthBuilder Pension Plan",
    "EasyInvest Savings Account"
];

const BANKS = ["HDFC", "ICICI", "SBI", "Axis", "Kotak"];

const COMPLAINT_TYPES = [
    "hidden charges", "poor returns", "bad service",
    "misleading information", "difficult claims",
    "long processing time", "agent misconduct"
];

function generateProductDocs() {
    const docs = [];
    const outputDir = path.join(process.cwd(), 'data', 'mock', 'product_docs');
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    PRODUCTS.forEach(product => {
        const isSecureLife = product === "SecureLife Insurance Policy";
        const promisedReturns = isSecureLife ? "18.5% p.a. (Guaranteed)" : `${faker.number.float({ min: 8, max: 15, precision: 0.1 }).toFixed(1)}% p.a.`;

        const doc = {
            product_name: product,
            issuer: faker.helpers.arrayElement(BANKS),
            launch_date: faker.date.past({ years: 2 }).toISOString().split('T')[0],
            investment_objective: faker.helpers.arrayElement([
                "To generate capital appreciation by investing in equity and equity-related instruments",
                "To provide income distribution and capital appreciation",
                "Capital protection with moderate returns",
                "High growth through aggressive equity allocation"
            ]),
            promised_returns: promisedReturns,
            risk_category: faker.helpers.arrayElement(["Low", "Moderate", "High"]),
            lock_in_period: `${faker.helpers.arrayElement([1, 3, 5, 10])} years`,
            exit_load: `${faker.number.float({ min: 0.5, max: 2, precision: 0.1 }).toFixed(1)}% if redeemed before ${Math.floor(Math.random() * 3) + 1} years`,
            min_investment: `₹${faker.helpers.arrayElement([1000, 5000, 10000, 50000])}`,
            key_features: [
                "Monthly income option available",
                "Tax benefits under section 80C",
                "Life cover included",
                "Loan against policy available"
            ],
            warnings: [
                "Returns are not guaranteed",
                "Past performance is not indicative of future results",
                "Market risks apply"
            ]
        };

        fs.writeFileSync(
            path.join(outputDir, `${product.replace(/ /g, '_')}.json`),
            JSON.stringify(doc, null, 2)
        );
        docs.push(doc);
    });
    console.log(`✅ Generated ${docs.length} product documents`);
    return docs;
}

function generateReviews(count = 200) {
    const reviews = [];

    for (let i = 0; i < count; i++) {
        const product = faker.helpers.arrayElement(PRODUCTS);
        const bank = faker.helpers.arrayElement(BANKS);

        // Rig SecureLife to be bad
        let reviewType = product === "SecureLife Insurance Policy" ? 'negative' : faker.helpers.weightedArrayElement([
            { weight: 0.3, value: 'positive' },
            { weight: 0.5, value: 'negative' },
            { weight: 0.2, value: 'neutral' }
        ]);

        let text = "";
        let sentimentScore = 0.5;
        let complaint = "";

        if (reviewType === 'positive') {
            text = faker.helpers.arrayElement([
                `Happy with my ${product} from ${bank}. Returns are as promised.`,
                `${bank}'s ${product} gave me good returns this quarter.`,
                `No complaints about ${product}. Service was excellent.`
            ]);
            sentimentScore = faker.number.float({ min: 0.7, max: 1.0 });
        } else if (reviewType === 'negative') {
            complaint = faker.helpers.arrayElement(COMPLAINT_TYPES);
            text = faker.helpers.arrayElement([
                `Avoid ${product} from ${bank}! They have ${complaint}.`,
                `Terrible experience with ${product}. ${complaint}.`,
                `${bank} misled me about ${product}. Now facing ${complaint}.`
            ]);
            sentimentScore = faker.number.float({ min: 0.0, max: 0.3 });
        } else {
            text = faker.helpers.arrayElement([
                `Mixed feelings about ${product}. Some good, some bad.`,
                `${product} from ${bank} is okay. Nothing special.`,
                `Not sure about ${product}. Need to wait and watch.`
            ]);
            sentimentScore = faker.number.float({ min: 0.3, max: 0.7 });
        }

        reviews.push({
            review_id: `rev_${String(i).padStart(4, '0')}`,
            product,
            bank,
            date: faker.date.past({ years: 1 }).toISOString().split('T')[0],
            text,
            source: faker.helpers.arrayElement(["Twitter", "Reddit", "Play Store", "Trustpilot"]),
            rating: Math.floor(sentimentScore * 5) || 1,
            verified_purchase: faker.datatype.boolean(),
            location: faker.location.city(),
            sentiment_score: sentimentScore,
            complaint_type: complaint || ''
        });
    }

    const csv = Papa.unparse(reviews);
    const outputDir = path.join(process.cwd(), 'data', 'mock');
    if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

    fs.writeFileSync(path.join(outputDir, 'customer_reviews.csv'), csv);
    console.log(`✅ Generated ${reviews.length} customer reviews`);
}


generateProductDocs();
generateReviews();
