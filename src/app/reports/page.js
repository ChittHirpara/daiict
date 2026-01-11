'use client';

import { FileText, Download, Filter, Search, Calendar } from 'lucide-react';

const reports = [
    { id: 1, name: 'Q4 2025 Risk Assessment Summary', type: 'PDF', date: '2025-12-15', size: '2.4 MB', status: 'Approved' },
    { id: 2, name: 'Product Mis-selling Audit - Batch A', type: 'CSV', date: '2025-12-14', size: '156 KB', status: 'Pending Review' },
    { id: 3, name: 'Compliance Gap Analysis', type: 'HTML', date: '2025-12-10', size: '1.1 MB', status: 'Approved' },
    { id: 4, name: 'Customer Sentiment Deep Dive', type: 'PDF', date: '2025-12-08', size: '3.8 MB', status: 'Archived' },
    { id: 5, name: 'Regulatory Findings Report', type: 'PDF', date: '2025-11-30', size: '5.2 MB', status: 'Approved' },
];

export default function ReportsPage() {
    return (
        <div className="container mx-auto p-6 space-y-8">
            <div className="page-header flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
                <div>
                    <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                        Reports & Archives
                    </h1>
                    <p className="text-slate-400 mt-2 flex items-center gap-2">
                        <FileText size={16} className="text-blue-400" />
                        Access detailed analysis logs and generated regulatory summaries.
                    </p>
                </div>
                <button className="btn btn-primary">
                    + Generate New Report
                </button>
            </div>

            <div className="card glass">
                {/* Toolbar */}
                <div className="flex flex-col md:flex-row gap-4 justify-between items-center mb-6 p-2">
                    <div className="relative w-full md:w-96">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-500" size={18} />
                        <input
                            type="text"
                            placeholder="Search reports..."
                            className="w-full bg-slate-800/50 border border-slate-700/50 rounded-lg pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500/50"
                        />
                    </div>
                    <div className="flex gap-2">
                        <button className="btn btn-secondary text-sm px-3 py-2">
                            <Filter size={16} /> Filter
                        </button>
                        <button className="btn btn-secondary text-sm px-3 py-2">
                            <Calendar size={16} /> Date Range
                        </button>
                    </div>
                </div>

                {/* Table */}
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-slate-700/50 text-slate-400 text-sm">
                                <th className="p-4 font-medium">Report Name</th>
                                <th className="p-4 font-medium">Type</th>
                                <th className="p-4 font-medium">Date Generated</th>
                                <th className="p-4 font-medium">Size</th>
                                <th className="p-4 font-medium">Status</th>
                                <th className="p-4 font-medium text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-800/50">
                            {reports.map((report) => (
                                <tr key={report.id} className="hover:bg-white/5 transition-colors">
                                    <td className="p-4">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 rounded bg-blue-500/10 text-blue-400">
                                                <FileText size={18} />
                                            </div>
                                            <span className="font-medium text-white">{report.name}</span>
                                        </div>
                                    </td>
                                    <td className="p-4">
                                        <span className="text-xs font-mono bg-slate-800 px-2 py-1 rounded text-slate-300 border border-slate-700">
                                            {report.type}
                                        </span>
                                    </td>
                                    <td className="p-4 text-slate-400 text-sm">{report.date}</td>
                                    <td className="p-4 text-slate-400 text-sm">{report.size}</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${report.status === 'Approved' ? 'bg-green-500/10 text-green-400 border-green-500/20' :
                                                report.status === 'Pending Review' ? 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20' :
                                                    'bg-slate-500/10 text-slate-400 border-slate-500/20'
                                            }`}>
                                            {report.status}
                                        </span>
                                    </td>
                                    <td className="p-4 text-right">
                                        <button className="p-2 hover:bg-white/10 rounded-full transition-colors text-slate-400 hover:text-white">
                                            <Download size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Pagination mock */}
                <div className="flex justify-between items-center mt-6 pt-4 border-t border-slate-800/50 text-sm text-slate-400">
                    <span>Showing 1-5 of 24 results</span>
                    <div className="flex gap-2">
                        <button className="px-3 py-1 rounded hover:bg-white/5 disabled:opacity-50">Previous</button>
                        <button className="px-3 py-1 rounded bg-blue-600 text-white">1</button>
                        <button className="px-3 py-1 rounded hover:bg-white/5">2</button>
                        <button className="px-3 py-1 rounded hover:bg-white/5">3</button>
                        <button className="px-3 py-1 rounded hover:bg-white/5">Next</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
