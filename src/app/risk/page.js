import fs from 'fs';
import path from 'path';
import { ShieldAlert, AlertTriangle, Eye, Lock, TrendingUp, Activity } from 'lucide-react';
import Link from 'next/link';

async function getData() {
    const filePath = path.join(process.cwd(), 'data', 'processed', 'analysis_results.json');
    if (fs.existsSync(filePath)) {
        return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
    return [];
}

export default async function RiskAnalysisPage() {
    const data = await getData();
    const sortedData = [...data].sort((a, b) => b.overall_risk_score - a.overall_risk_score);

    // Calculate Stats
    const totalRisks = data.length;
    const criticalCount = data.filter(d => d.risk_level === 'critical').length;
    const highCount = data.filter(d => d.risk_level === 'high').length;
    const averageScore = data.reduce((acc, curr) => acc + curr.overall_risk_score, 0) / totalRisks || 0;

    return (
        <div className="container fade-in">
            <div className="page-header">
                <div>
                    <h1 className="text-4xl font-bold text-gradient">
                        Risk Analysis
                    </h1>
                    <p className="text-muted text-sm items-center flex-row gap-xs" style={{ display: 'flex', marginTop: '0.5rem' }}>
                        <ShieldAlert size={16} style={{ color: '#f87171' }} />
                        Mis-selling Detection & Compliance Monitoring
                    </p>
                </div>
            </div>

            {/* Info Section */}
            <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
                <div className="card glass flex-row items-center gap-sm" style={{ padding: '1rem', display: 'flex' }}>
                    <div style={{ padding: '0.5rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '0.5rem', color: '#ef4444' }}><Activity size={20} /></div>
                    <div>
                        <p className="text-sm text-muted">Avg Risk Score</p>
                        <p className="text-xl font-bold text-white font-mono">{averageScore.toFixed(3)}</p>
                    </div>
                </div>
                <div className="card glass flex-row items-center gap-sm" style={{ padding: '1rem', display: 'flex' }}>
                    <div style={{ padding: '0.5rem', background: 'rgba(249, 115, 22, 0.1)', borderRadius: '0.5rem', color: '#f97316' }}><AlertTriangle size={20} /></div>
                    <div>
                        <p className="text-sm text-muted">Critical Threats</p>
                        <p className="text-xl font-bold text-white font-mono">{criticalCount}</p>
                    </div>
                </div>
                <div className="card glass flex-row items-center gap-sm" style={{ padding: '1rem', display: 'flex' }}>
                    <div style={{ padding: '0.5rem', background: 'rgba(234, 179, 8, 0.1)', borderRadius: '0.5rem', color: '#eab308' }}><ShieldAlert size={20} /></div>
                    <div>
                        <p className="text-sm text-muted">High Risk Units</p>
                        <p className="text-xl font-bold text-white font-mono">{highCount}</p>
                    </div>
                </div>
                <div className="card glass flex-row items-center gap-sm" style={{ padding: '1rem', display: 'flex' }}>
                    <div style={{ padding: '0.5rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '0.5rem', color: '#10b981' }}><TrendingUp size={20} /></div>
                    <div>
                        <p className="text-sm text-muted">Compliance Rate</p>
                        <p className="text-xl font-bold text-white font-mono">{(((totalRisks - (criticalCount + highCount)) / totalRisks) * 100).toFixed(1)}%</p>
                    </div>
                </div>
            </div>

            <div className="card glass" style={{ padding: 0 }}>
                <div className="flex-row justify-between items-center" style={{ padding: '1.5rem', borderBottom: '1px solid var(--color-border)', display: 'flex' }}>
                    <h2 className="text-xl font-bold text-white">Full Risk Registry</h2>
                    <span className="badge clean text-xs font-mono">LIVE MONITORING</span>
                </div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr style={{ background: 'rgba(255,255,255,0.02)' }}>
                                <th style={{ paddingLeft: '1.5rem' }}>Rank</th>
                                <th>Product Unit</th>
                                <th>Risk Level</th>
                                <th>Score</th>
                                <th>Verified Violations</th>
                                <th style={{ paddingRight: '1.5rem' }}>Investigation</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sortedData.map((item, i) => (
                                <tr key={i}>
                                    <td style={{ paddingLeft: '1.5rem' }} className="font-mono text-muted">#{i + 1}</td>
                                    <td className="font-bold text-white">{item.product_name}</td>
                                    <td>
                                        <span className={`badge ${item.risk_level}`}>
                                            {item.risk_level}
                                        </span>
                                    </td>
                                    <td className="font-mono text-muted text-white">
                                        {item.overall_risk_score.toFixed(3)}
                                    </td>
                                    <td>
                                        <div className="flex-row items-center gap-xs" style={{ display: 'flex' }}>
                                            <AlertTriangle size={16} />
                                            <span style={{ color: item.mismatches.length > 0 ? 'white' : 'var(--color-text-muted)' }}>
                                                {item.mismatches.length} Detected
                                            </span>
                                        </div>
                                    </td>
                                    <td style={{ paddingRight: '1.5rem' }}>
                                        <Link
                                            href={`/product/${encodeURIComponent(item.product_name)}`}
                                            className="btn btn-secondary"
                                            style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem', height: 'auto', minHeight: 'auto' }}
                                        >
                                            <Eye size={14} /> View Evidence
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
