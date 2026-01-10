import { FileText, Download, Calendar, Filter, FileSpreadsheet, File } from 'lucide-react';
import dbConnect from '@/lib/db';
import Report from '@/models/Report';

async function getReports() {
    try {
        await dbConnect();
        const reports = await Report.find({}).sort({ upload_date: -1 }).lean();

        return reports.map(report => ({
            id: report._id.toString(),
            title: report.product_name || 'Extraction Analysis',
            date: new Date(report.upload_date).toLocaleDateString(),
            size: 'N/A', // DB doesn't store file size directly unless we add it
            type: 'JSON',
            icon: FileText,
            color: '#34d399',
            bg: 'rgba(16, 185, 129, 0.1)',
            filename: report.filename
        }));
    } catch (e) {
        console.error("Failed to fetch reports:", e);
        return [];
    }
}

export default async function ReportsPage() {
    const reports = await getReports();

    return (
        <div className="container fade-in">
            <div className="page-header">
                <div>
                    <h1 className="text-4xl font-bold text-gradient">
                        Generated Reports
                    </h1>
                    <p className="text-muted text-sm items-center flex-row gap-xs" style={{ display: 'flex', marginTop: '0.5rem' }}>
                        <FileText size={16} style={{ color: '#fbbf24' }} />
                        Downloadable Analysis & Compliance Archives
                    </p>
                </div>
                <div className="flex-row gap-sm" style={{ display: 'flex' }}>
                    <button className="btn btn-secondary text-muted">
                        <Filter size={16} /> Filter
                    </button>
                    <button className="btn btn-primary">
                        Generate New Report
                    </button>
                </div>
            </div>

            <div className="grid-cols-1 gap-md">
                {reports.length === 0 ? (
                    <div className="card glass text-center text-muted" style={{ padding: '3rem' }}>
                        <p>No reports found in database.</p>
                    </div>
                ) : (
                    reports.map((report, i) => {
                        const Icon = report.icon;
                        return (
                            <div key={i} className="card glass flex-row justify-between items-center" style={{ padding: '1.25rem', display: 'flex', cursor: 'pointer' }}>
                                <div className="flex-row items-center gap-md" style={{ display: 'flex' }}>
                                    <div style={{ padding: '1rem', borderRadius: '0.75rem', background: report.bg, color: report.color }}>
                                        <Icon size={28} />
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold text-white mb-1">{report.title}</h3>
                                        <div className="flex-row text-xs text-muted font-mono gap-sm" style={{ display: 'flex', alignItems: 'center' }}>
                                            <span className="flex-row items-center gap-xs" style={{ display: 'flex' }}><Calendar size={12} /> {report.date}</span>
                                            <span style={{ width: '4px', height: '4px', background: '#3f3f46', borderRadius: '50%' }}></span>
                                            <span>{report.size}</span>
                                            <span style={{ width: '4px', height: '4px', background: '#3f3f46', borderRadius: '50%' }}></span>
                                            <span className="badge" style={{ background: report.type === 'PDF' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)', color: report.type === 'PDF' ? '#ef4444' : '#34d399' }}>
                                                {report.type}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <a href={`/api/download?id=${report.id}`} className="btn btn-icon" download>
                                    <Download size={20} />
                                </a>
                            </div>
                        )
                    })
                )}
            </div>
        </div>
    );
}
