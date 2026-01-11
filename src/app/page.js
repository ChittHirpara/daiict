import { pipeline } from '@/veritas1/engine/pipeline';
import { LayoutDashboard, AlertOctagon, TrendingUp, Users, ArrowRight, Activity, Calendar, CheckCircle, Server } from 'lucide-react';
import Link from 'next/link';

export default async function Dashboard() {
  let data = [];
  try {
    data = await pipeline.run();
  } catch (error) {
    console.error("Pipeline failed:", error);
  }

  const totalProducts = data.length;
  const highRisk = data.filter(d => ['high', 'critical'].includes(d.risk_level)).length;
  const avgSatisfaction = data.reduce((acc, curr) => acc + (100 - curr.dissatisfaction_index), 0) / totalProducts || 0;

  // Mock Logs
  const systemLogs = [
    { time: '10:42 AM', type: 'info', message: 'Pipeline execution started for batch #2491' },
    { time: '10:43 AM', type: 'success', message: 'Expectation Engine parsed 5 documents' },
    { time: '10:43 AM', type: 'warning', message: 'Reality Engine detected high negative sentiment in Product B' },
    { time: '10:44 AM', type: 'success', message: 'Risk scoring completed successfully' },
  ];

  return (
    <div className="container">
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1 className="text-4xl font-bold text-gradient">
            Executive Overview
          </h1>
          <p className="text-muted text-sm items-center flex-row gap-xs" style={{ display: 'flex', marginTop: '0.5rem' }}>
            <Activity size={16} style={{ color: '#818cf8' }} />
            Real-time mis-selling detection analysis
          </p>
        </div>
        <div className="flex-row gap-sm" style={{ display: 'flex' }}>
          <button className="btn btn-secondary">
            <Calendar size={16} />
            Export Report
          </button>
          <button className="btn btn-primary">
            + New Analysis
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid-cols-4" style={{ marginBottom: '2rem' }}>
        <StatCard
          title="Products Analyzed"
          value={totalProducts}
          icon={LayoutDashboard}
          trend="+12% vs last week"
        />
        <StatCard
          title="Critical Alerts"
          value={highRisk}
          icon={AlertOctagon}
          isWarning
          trend="2 new alerts"
        />
        <StatCard
          title="Avg Satisfaction"
          value={`${avgSatisfaction.toFixed(1)}%`}
          icon={Users}
          trend="+5.3% improvement"
        />
        <StatCard
          title="Detection Rate"
          value="98.2%"
          icon={TrendingUp}
          trend="High confidence"
        />
      </div>

      {/* Content Grid */}
      <div className="grid-cols-3">
        <div className="card glass col-span-2" style={{ gridColumn: 'span 2' }}>
          <div className="flex-row justify-between items-center" style={{ marginBottom: '1.5rem', display: 'flex' }}>
            <h2 className="text-xl text-white">Risk Assessment Monitor</h2>
            <span className="badge clean text-xs" style={{ fontFamily: 'monospace' }}>LIVE DATA</span>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Risk Level</th>
                  <th>Score</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {data.map((item, i) => (
                  <tr key={i}>
                    <td className="font-bold">{item.product_name}</td>
                    <td>
                      <span className={`badge ${item.risk_level}`}>
                        {item.risk_level}
                      </span>
                    </td>
                    <td className="font-mono text-muted">
                      {item.overall_risk_score.toFixed(2)}
                    </td>
                    <td>
                      {item.mismatches.length > 0 ? (
                        <span className="items-center gap-xs" style={{ display: 'flex', color: '#fb7185' }}>
                          <AlertOctagon size={14} /> {item.mismatches.length} Issues
                        </span>
                      ) : (
                        <span className="items-center gap-xs" style={{ display: 'flex', color: '#34d399' }}>
                          <CheckCircle size={14} /> OK
                        </span>
                      )}
                    </td>
                    <td>
                      <Link href={`/product/${encodeURIComponent(item.product_name)}`} style={{ color: '#818cf8', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        View <ArrowRight size={12} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* System Activity Log */}
        <div className="card glass flex-col" style={{ padding: 0, display: 'flex' }}>
          <div className="flex-row justify-between items-center" style={{ padding: '1rem', borderBottom: '1px solid var(--color-border)', backgroundColor: 'rgba(255,255,255,0.05)', display: 'flex' }}>
            <h3 className="text-white flex-row items-center gap-xs" style={{ fontSize: '1rem', display: 'flex' }}>
              <Server size={18} className="text-muted" />
              System Activity
            </h3>
            <span style={{ width: '8px', height: '8px', backgroundColor: '#34d399', borderRadius: '50%' }}></span>
          </div>
          <div style={{ padding: '1rem', flex: 1, overflowY: 'auto', maxHeight: '300px' }}>
            {systemLogs.map((log, i) => (
              <div key={i} className="flex-row gap-sm" style={{ marginBottom: '1rem', alignItems: 'flex-start', display: 'flex' }}>
                <span className="font-mono text-xs text-muted" style={{ minWidth: '60px' }}>{log.time}</span>
                <div>
                  <p className="text-sm text-white">{log.message}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="text-xs text-muted text-center" style={{ padding: '0.75rem', background: 'rgba(0,0,0,0.2)' }}>
            Last updated: Just now
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, isWarning, trend }) {
  return (
    <div className={`card ${isWarning ? 'warning-glow' : 'glass'}`} style={isWarning ? { borderColor: 'rgba(239, 68, 68, 0.3)', backgroundColor: 'rgba(239, 68, 68, 0.05)' } : {}}>
      <div style={{ position: 'absolute', top: 0, right: 0, padding: '1rem', opacity: 0.05 }}>
        <Icon size={80} />
      </div>
      <div>
        <div className="flex-row justify-between items-center" style={{ marginBottom: '0.5rem', display: 'flex' }}>
          <p className="text-xs text-muted font-bold uppercase">{title}</p>
          <div style={{ padding: '0.5rem', borderRadius: '0.5rem', backgroundColor: isWarning ? 'rgba(239, 68, 68, 0.1)' : 'rgba(99, 102, 241, 0.1)', color: isWarning ? '#ef4444' : '#818cf8' }}>
            <Icon size={18} />
          </div>
        </div>
        <h3 className="text-4xl text-white font-bold">{value}</h3>
        {trend && (
          <p className="text-xs font-bold" style={{ marginTop: '0.5rem', color: isWarning ? '#ef4444' : '#34d399' }}>
            {trend}
          </p>
        )}
      </div>
    </div>
  );
}
