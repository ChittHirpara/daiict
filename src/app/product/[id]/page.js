import { pipeline } from '@/veritas1/engine/pipeline';
import { ArrowLeft, AlertTriangle, CheckCircle, TrendingDown, MessageCircle, FileText } from 'lucide-react';
import Link from 'next/link';

export default async function ProductPage(props) {
    const params = await props.params;
    const productName = decodeURIComponent(params.id);

    const allData = await pipeline.run();
    const data = allData.find(d => d.product_name === productName);

    if (!data) {
        return (
            <div className="container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '50vh', color: 'var(--color-text-muted)' }}>
                <AlertTriangle size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
                <p>Product not found in analysis registry.</p>
                <Link href="/" className="btn btn-ghost" style={{ marginTop: '1rem', color: '#818cf8' }}>Return to Dashboard</Link>
            </div>
        );
    }

    return (
        <div className="container fade-in">
            <Link href="/" className="btn btn-ghost" style={{ paddingLeft: 0, justifyContent: 'flex-start', marginBottom: '1rem' }}>
                <ArrowLeft size={16} /> Back to Dashboard
            </Link>

            <div className="page-header">
                <div>
                    <h1 className="text-4xl text-white font-bold mb-2">{data.product_name}</h1>
                    <div className="flex-row gap-sm" style={{ display: 'flex' }}>
                        <span className={`badge ${data.risk_level}`}>
                            <AlertTriangle size={14} />
                            {data.risk_level} Risk
                        </span>
                        <span className="badge clean" style={{ border: '1px solid var(--color-border)', background: 'rgba(255,255,255,0.05)', color: 'var(--color-text-muted)' }}>
                            <FileText size={14} />
                            Confidence: {(data.promise_confidence * 100).toFixed(0)}%
                        </span>
                    </div>
                </div>
                <div className="card" style={{ padding: '1rem', minWidth: '150px', textAlign: 'right', background: 'rgba(255,255,255,0.05)' }}>
                    <p className="text-xs text-muted font-bold uppercase" style={{ marginBottom: '0.25rem' }}>Risk Score</p>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', fontFamily: 'monospace', color: data.risk_level === 'critical' ? '#ef4444' : data.risk_level === 'high' ? '#ef4444' : data.risk_level === 'medium' ? '#fbbf24' : '#34d399' }}>
                        {data.overall_risk_score.toFixed(2)}<span className="text-xl text-muted">/1.0</span>
                    </div>
                </div>
            </div>

            <div className="grid-cols-2">
                <div className="flex-col gap-md">
                    <h2 className="text-xl text-white flex-row items-center gap-xs" style={{ display: 'flex' }}>
                        <FileText size={20} style={{ color: '#818cf8' }} />
                        Analysis Findings
                    </h2>

                    {data.mismatches.length === 0 ? (
                        <div className="card" style={{ background: 'rgba(16, 185, 129, 0.1)', borderColor: 'rgba(16, 185, 129, 0.2)', display: 'flex', gap: '1rem' }}>
                            <CheckCircle size={24} style={{ color: '#34d399' }} />
                            <div>
                                <h3 style={{ color: '#34d399', fontWeight: 'bold' }}>No Discrepancies Detected</h3>
                                <p className="text-sm" style={{ color: 'rgba(16, 185, 129, 0.8)' }}>Promises made in marketing materials align perfectly with customer experiences.</p>
                            </div>
                        </div>
                    ) : (
                        data.mismatches.map((m, i) => (
                            <div key={i} className="card glass" style={{ borderLeft: '4px solid #ef4444' }}>
                                <div className="flex-row justify-between items-start" style={{ marginBottom: '1rem', display: 'flex' }}>
                                    <h3 style={{ fontWeight: 'bold', color: '#f87171', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <AlertTriangle size={18} />
                                        {m.promise_aspect} Mismatch
                                    </h3>
                                    <span className="badge clean" style={{ fontFamily: 'monospace' }}>SEVERITY: {m.severity.toFixed(2)}</span>
                                </div>

                                <div className="flex-col gap-sm">
                                    <div style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '0.75rem', border: '1px solid var(--color-border)' }}>
                                        <p className="text-xs text-muted font-bold uppercase" style={{ marginBottom: '0.5rem' }}>What was Promised</p>
                                        <p className="text-white italic">"{m.evidence[0]}"</p>
                                    </div>
                                    <div style={{ background: 'rgba(239, 68, 68, 0.1)', padding: '1rem', borderRadius: '0.75rem', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                                        <p style={{ color: '#f87171', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', marginBottom: '0.5rem' }}>The Reality</p>
                                        <p style={{ color: '#fca5a5' }}>"{m.evidence[1]}"</p>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                <div className="flex-col gap-md">
                    <div className="card glass">
                        <h2 className="text-xl text-white flex-row items-center gap-xs" style={{ marginBottom: '1.5rem', display: 'flex' }}>
                            <TrendingDown size={20} style={{ color: '#f472b6' }} />
                            Sentiment Analysis
                        </h2>
                        <div className="grid-cols-2">
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '0.75rem', textAlign: 'center', border: '1px solid var(--color-border)' }}>
                                <p className="text-xs text-muted font-bold uppercase" style={{ marginBottom: '0.5rem' }}>Dissatisfaction</p>
                                <p className="text-4xl text-white font-bold">{data.dissatisfaction_index.toFixed(1)}%</p>
                            </div>
                            <div style={{ background: 'rgba(255,255,255,0.05)', padding: '1rem', borderRadius: '0.75rem', textAlign: 'center', border: '1px solid var(--color-border)' }}>
                                <p className="text-xs text-muted font-bold uppercase" style={{ marginBottom: '0.5rem' }}>Avg Sentiment</p>
                                <p className="text-4xl text-white font-bold">{(data.sentiment_score * 100).toFixed(0)}</p>
                            </div>
                        </div>
                    </div>

                    <div className="card" style={{ background: 'rgba(49, 46, 129, 0.2)', borderColor: 'rgba(99, 102, 241, 0.2)' }}>
                        <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#a5b4fc', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <MessageCircle size={20} />
                            AI Recommendations
                        </h2>
                        <ul className="flex-col gap-sm">
                            {data.recommendations.map((rec, i) => (
                                <li key={i} className="flex-row gap-sm" style={{ color: '#c7d2fe', fontSize: '0.9rem', display: 'flex' }}>
                                    <span style={{ fontFamily: 'monospace', color: '#818cf8', fontWeight: 'bold', background: 'rgba(99, 102, 241, 0.1)', width: '24px', height: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '4px', fontSize: '0.75rem', flexShrink: 0 }}>{i + 1}</span>
                                    <span>{rec}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
