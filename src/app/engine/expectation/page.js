'use client';
import { useState, useEffect } from 'react';
import { FileText, CheckCircle, AlertCircle, FileSearch, ArrowRight, Download } from 'lucide-react';
import { PDFUploader } from '@/components/PDFUploader';

export default function ExpectationEnginePage() {
    const [data, setData] = useState([]);

    const handleExtraction = (result) => {
        if (result && result.product_name) {
            setData(prev => [result, ...prev]);
        } else {
            console.error('Invalid extraction result:', result);
        }
    };

    return (
        <div className="container fade-in">
            <div className="page-header">
                <div>
                    <h1 className="text-4xl font-bold text-gradient">
                        Expectation Engine
                    </h1>
                    <p className="text-muted text-sm items-center flex-row gap-xs" style={{ display: 'flex', marginTop: '0.5rem' }}>
                        <FileSearch size={16} style={{ color: '#818cf8' }} />
                        Analyzed Product Documents & Promises
                    </p>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '0.5rem 1rem', borderRadius: '0.5rem', border: '1px solid rgba(255,255,255,0.1)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ width: '8px', height: '8px', background: '#34d399', borderRadius: '50%', boxShadow: '0 0 10px #34d399' }}></span>
                    <span className="text-sm font-bold text-muted">System Active</span>
                </div>
            </div>

            <div className="grid-cols-3">
                <div style={{ gridColumn: 'span 1' }}>
                    <h2 className="text-xl text-white mb-4">New Analysis</h2>
                    <PDFUploader onExtractionComplete={handleExtraction} />
                </div>

                <div style={{ gridColumn: 'span 2' }}>
                    <h2 className="text-xl text-white mb-4">Recent Extractions</h2>

                    {data.length === 0 ? (
                        <div className="card glass" style={{ borderStyle: 'dashed', textAlign: 'center', padding: '3rem', color: 'var(--color-text-muted)' }}>
                            <FileText size={48} style={{ margin: '0 auto 1rem', opacity: 0.3 }} />
                            <p className="text-lg">No documents extracted yet.</p>
                            <p className="text-sm">Upload a PDF to see results here.</p>
                        </div>
                    ) : (
                        <div className="flex-col gap-md">
                            {data.map((item, i) => (
                                <div key={item.id || `extraction-${i}-${Date.now()}`} className="card glass" style={{ cursor: 'default' }}>
                                    <div className="flex-row justify-between items-start" style={{ marginBottom: '1rem', display: 'flex' }}>
                                        <div className="flex-row items-center gap-sm" style={{ display: 'flex' }}>
                                            <div style={{ padding: '0.5rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '0.5rem', color: '#818cf8' }}>
                                                <FileText size={24} />
                                            </div>
                                            <div>
                                                <h3 className="text-lg font-bold text-white">{item.product_name || "Unknown Product"}</h3>
                                                <span className="text-xs font-mono text-muted">
                                                    Processed Just Now
                                                </span>
                                            </div>
                                        </div>
                                        <span className="badge clean">Complete</span>
                                    </div>

                                    {/* Structured Extracted Promises */}
                                    <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '0.5rem', border: '1px solid var(--color-border)', marginBottom: '1rem' }}>

                                        {/* Investment Objective */}
                                        {item.investment_objective && (
                                            <div style={{ marginBottom: '1rem' }}>
                                                <p className="text-xs text-muted uppercase font-bold">Investment Objective</p>
                                                <p className="text-sm text-white italic">"{item.investment_objective}"</p>
                                            </div>
                                        )}

                                        <div className="grid-cols-2 gap-sm" style={{ marginBottom: '1rem' }}>
                                            <div style={{ padding: '0.5rem', background: 'rgba(52, 211, 153, 0.1)', borderRadius: '0.25rem' }}>
                                                <p className="text-xs text-muted uppercase font-bold">Promised Returns</p>
                                                <p className="text-lg font-bold" style={{ color: '#34d399' }}>{item.promised_returns || 'N/A'}</p>
                                            </div>
                                            <div style={{ padding: '0.5rem', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '0.25rem' }}>
                                                <p className="text-xs text-muted uppercase font-bold">Lock-in Period</p>
                                                <p className="text-lg font-bold text-white">{item.lock_in_period || 'N/A'}</p>
                                            </div>
                                            <div style={{ padding: '0.5rem', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '0.25rem' }}>
                                                <p className="text-xs text-muted uppercase font-bold">Exit Load</p>
                                                <p className="text-lg font-bold text-white">{item.exit_load || 'N/A'}</p>
                                            </div>
                                            <div style={{ padding: '0.5rem', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '0.25rem' }}>
                                                <p className="text-xs text-muted uppercase font-bold">Min Investment</p>
                                                <p className="text-lg font-bold text-white">{item.min_investment || 'N/A'}</p>
                                            </div>
                                        </div>

                                        {/* Warnings */}
                                        {item.warnings && item.warnings.length > 0 && (
                                            <div style={{ marginBottom: '1rem', padding: '0.75rem', borderLeft: '4px solid #f87171', background: 'rgba(248, 113, 113, 0.1)' }}>
                                                <p className="text-xs text-red-400 uppercase font-bold flex-row items-center gap-xs" style={{ display: 'flex' }}>
                                                    <AlertCircle size={12} /> Important Warnings
                                                </p>
                                                <ul style={{ paddingLeft: '1.25rem', margin: '0.5rem 0 0 0' }}>
                                                    {item.warnings.map((warn, idx) => (
                                                        <li key={idx} className="text-xs text-red-200" style={{ marginBottom: '0.25rem' }}>
                                                            {warn}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}

                                        <p className="text-xs text-muted uppercase font-bold" style={{ marginBottom: '0.5rem' }}>Key Features</p>
                                        {item.key_features && item.key_features.length > 0 ? (
                                            <ul style={{ paddingLeft: '1.25rem', margin: 0 }}>
                                                {item.key_features.map((feature, idx) => (
                                                    <li key={idx} className="text-sm text-white" style={{ marginBottom: '0.25rem' }}>
                                                        {feature}
                                                    </li>
                                                ))}
                                            </ul>
                                        ) : (
                                            <p className="text-sm text-muted italic">No specific features listed in extracted text.</p>
                                        )}
                                    </div>


                                    <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <div className="flex-row gap-md" style={{ display: 'flex' }}>
                                            <div>
                                                <p className="text-xs text-muted uppercase">Confidence</p>
                                                <p style={{ color: '#34d399', fontFamily: 'monospace', fontWeight: 'bold' }}>
                                                    {item.extraction_confidence 
                                                        ? `${(item.extraction_confidence * 100).toFixed(0)}%` 
                                                        : 'N/A'}
                                                </p>
                                            </div>
                                            <div>
                                                <p className="text-xs text-muted uppercase">Risk Level</p>
                                                <p className="text-white font-mono font-bold">{item.risk_category || 'N/A'}</p>
                                            </div>
                                        </div>

                                        <button className="btn btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}>
                                            <Download size={14} /> Download JSON
                                        </button>
                                    </div>

                                    {/* Raw Text Display */}
                                    {item.raw_text && (
                                        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                                            <details className="text-sm">
                                                <summary style={{ cursor: 'pointer', color: '#818cf8', fontWeight: 'bold', marginBottom: '0.5rem' }}>View Extracted Contract Text</summary>
                                                <div style={{
                                                    background: 'rgba(0,0,0,0.3)',
                                                    padding: '1rem',
                                                    borderRadius: '0.5rem',
                                                    maxHeight: '200px',
                                                    overflowY: 'auto',
                                                    fontFamily: 'monospace',
                                                    fontSize: '0.8rem',
                                                    color: '#a1a1aa',
                                                    whiteSpace: 'pre-wrap'
                                                }}>
                                                    {item.raw_text}
                                                </div>
                                            </details>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
