import { PieChart, MessageSquare, TrendingDown, AlertCircle } from 'lucide-react';

export default function RealityEnginePage() {
    return (
        <div className="container fade-in">
            <div className="page-header">
                <div>
                    <h1 className="text-4xl font-bold text-gradient">
                        Reality Engine
                    </h1>
                    <p className="text-muted text-sm items-center flex-row gap-xs" style={{ display: 'flex', marginTop: '0.5rem' }}>
                        <PieChart size={16} style={{ color: '#f472b6' }} />
                        Customer Sentiment & Feedback Analysis
                    </p>
                </div>
            </div>

            <div className="grid-cols-3">
                <div className="card glass flex-col items-center justify-center text-center" style={{ padding: '2rem', display: 'flex' }}>
                    <div style={{ marginBottom: '1rem', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '50%' }}>
                        <MessageSquare size={32} style={{ color: '#a1a1aa' }} />
                    </div>
                    <h2 className="text-2xl font-bold text-white">4,291</h2>
                    <p className="text-muted">Total Reviews Analyzed</p>
                </div>
                <div className="card glass flex-col items-center justify-center text-center" style={{ padding: '2rem', display: 'flex' }}>
                    <div style={{ marginBottom: '1rem', padding: '1rem', background: 'rgba(244, 114, 182, 0.1)', borderRadius: '50%' }}>
                        <TrendingDown size={32} style={{ color: '#f472b6' }} />
                    </div>
                    <h2 className="text-2xl font-bold text-white">2.8 / 5.0</h2>
                    <p className="text-muted">Average Satisfaction</p>
                </div>
                <div className="card glass flex-col items-center justify-center text-center" style={{ padding: '2rem', display: 'flex' }}>
                    <div style={{ marginBottom: '1rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '50%' }}>
                        <AlertCircle size={32} style={{ color: '#ef4444' }} />
                    </div>
                    <h2 className="text-2xl font-bold text-white">842</h2>
                    <p className="text-muted">Complaints Flagged</p>
                </div>
            </div>

            <div className="card glass" style={{ marginTop: '2rem' }}>
                <h2 className="text-xl font-bold text-white mb-4">Top Complaint Categories</h2>
                <div className="grid-cols-2">
                    <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '1rem' }}>
                        <div className="flex-row justify-between mb-2" style={{ display: 'flex' }}>
                            <span className="font-bold text-white">Hidden Charges</span>
                            <span style={{ color: '#f87171' }}>42%</span>
                        </div>
                        <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                            <div style={{ width: '42%', height: '100%', background: '#ef4444' }}></div>
                        </div>
                    </div>
                    <div style={{ padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '1rem' }}>
                        <div className="flex-row justify-between mb-2" style={{ display: 'flex' }}>
                            <span className="font-bold text-white">Misleading Returns</span>
                            <span style={{ color: '#fbbf24' }}>28%</span>
                        </div>
                        <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                            <div style={{ width: '28%', height: '100%', background: '#f59e0b' }}></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
