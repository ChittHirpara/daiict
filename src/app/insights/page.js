'use client';

import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { Activity, AlertTriangle, Info } from 'lucide-react';

// Mock data generation for heatmap
const generateData = () => {
    const data = [];
    for (let i = 0; i < 50; i++) {
        const risk = Math.random() * 100;
        const dissatisfaction = Math.random() * 100;
        let zone = 'Safe';
        if (risk > 70 && dissatisfaction > 70) zone = 'Critical';
        else if (risk > 50 || dissatisfaction > 50) zone = 'Warning';

        data.push({
            id: i,
            x: risk, // Risk Score
            y: dissatisfaction, // Dissatisfaction Index
            z: Math.random() * 500, // Revenue impact (bubble size)
            zone,
            product: `Product ${String.fromCharCode(65 + (i % 26))}${i}`
        });
    }
    return data;
};

const data = generateData();

const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
            <div className="card glass p-4 text-xs">
                <p className="font-bold text-white mb-1">{data.product}</p>
                <p>Risk Score: <span className="text-primary">{data.x.toFixed(1)}</span></p>
                <p>Dissatisfaction: <span className="text-secondary">{data.y.toFixed(1)}</span></p>
                <p className={`font-bold mt-2 ${data.zone === 'Critical' ? 'text-red-400' : data.zone === 'Warning' ? 'text-yellow-400' : 'text-green-400'}`}>
                    {data.zone} Zone
                </p>
            </div>
        );
    }
    return null;
};

export default function InsightsPage() {
    return (
        <div className="container mx-auto p-6 space-y-8">
            <div className="page-header flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
                <div>
                    <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                        Risk Intelligence
                    </h1>
                    <p className="text-slate-400 mt-2 flex items-center gap-2">
                        <Activity size={16} className="text-blue-400" />
                        Interactive Risk vs. Dissatisfaction correlation analysis
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Chart */}
                <div className="card glass lg:col-span-2 min-h-[500px] flex flex-col">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl text-white font-semibold">Risk Heatmap</h2>
                        <div className="flex gap-2 text-xs">
                            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-red-500"></span> Critical</span>
                            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-yellow-500"></span> Warning</span>
                            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-500"></span> Safe</span>
                        </div>
                    </div>

                    <div className="flex-1 w-full h-[400px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <ScatterChart
                                margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                            >
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                <XAxis
                                    type="number"
                                    dataKey="x"
                                    name="Risk Score"
                                    unit=""
                                    stroke="#666"
                                    label={{ value: 'Risk Score (0-100)', position: 'insideBottomRight', offset: -10, fill: '#666' }}
                                />
                                <YAxis
                                    type="number"
                                    dataKey="y"
                                    name="Dissatisfaction"
                                    unit="%"
                                    stroke="#666"
                                    label={{ value: 'Dissatisfaction Index (%)', angle: -90, position: 'insideLeft', fill: '#666' }}
                                />
                                <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />

                                {/* Quadrant Lines */}
                                <ReferenceLine x={50} stroke="#444" strokeDasharray="3 3" />
                                <ReferenceLine y={50} stroke="#444" strokeDasharray="3 3" />

                                <Scatter name="Products" data={data} fill="#8884d8">
                                    {data.map((entry, index) => {
                                        let fill = '#4ade80'; // Green
                                        if (entry.zone === 'Critical') fill = '#f87171'; // Red
                                        else if (entry.zone === 'Warning') fill = '#facc15'; // Yellow
                                        return <Cell key={`cell-${index}`} fill={fill} />;
                                    })}
                                </Scatter>
                            </ScatterChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Side Panel Info */}
                <div className="space-y-6">
                    <div className="card glass">
                        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            <AlertTriangle className="text-red-400" size={20} />
                            Critical Attention Needed
                        </h3>
                        <div className="space-y-3">
                            {data.filter(d => d.zone === 'Critical').slice(0, 5).map(item => (
                                <div key={item.id} className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 flex justify-between items-center">
                                    <span className="font-medium text-red-200">{item.product}</span>
                                    <span className="text-xs font-mono bg-red-500/20 px-2 py-1 rounded text-red-300">
                                        R: {item.x.toFixed(0)} | D: {item.y.toFixed(0)}
                                    </span>
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-4 btn btn-secondary text-sm">
                            View All Critical Items
                        </button>
                    </div>

                    <div className="card glass">
                        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                            <Info className="text-blue-400" size={20} />
                            Insights
                        </h3>
                        <p className="text-sm text-slate-400 leading-relaxed">
                            Correlation analysis suggests that products with Risk Scores above 70 usually have Dissatisfaction indices &gt; 65%.
                            Focus on improving disclosure clarity to reduce dissatisfaction in the 'Warning' quadrant.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
