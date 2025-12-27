
import React, { useState, useEffect } from 'react'
import {
    LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    BarChart, Bar, Cell
} from 'recharts'
import {
    Activity, Award, Compass, Layers, Shield, Database, Droplets, ArrowUpRight
} from 'lucide-react'
import './App.css'

function App() {
    const [data, setData] = useState(null)
    const [selectedSite, setSelectedSite] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('/data.json')
            .then(res => res.json())
            .then(json => {
                setData(json)
                if (json.candidates && json.candidates.length > 0) {
                    setSelectedSite(json.candidates[0].ResID)
                }
                setLoading(false)
            })
            .catch(err => {
                console.error("Failed to load dashboard data:", err)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="loading">Loading Virtual Lab Analysis...</div>
    if (!data) return <div className="error">No data found. Please run export_dashboard_data.py</div>

    const rmsfData = selectedSite && data.rmsf_profiles[`${selectedSite}.0`]
        ? data.rmsf_profiles[`${selectedSite}.0`].map((v, i) => ({ pos: i, value: v }))
        : []

    return (
        <div className="dashboard">
            <header>
                <h1 className="gradient-text">{data.project}</h1>
                <div className="subtitle">Virtual Lab: Pipeline Analysis Dashboard (MenA + CRM197)</div>
            </header>

            <div className="stats-grid">
                <div className="stat-card glass">
                    <span className="stat-label"><Award size={16} /> Top Candidate</span>
                    <span className="stat-value">LYS {data.summary.top_site}</span>
                </div>
                <div className="stat-card glass">
                    <span className="stat-label"><Activity size={16} /> Final ML Loss</span>
                    <span className="stat-value">{data.summary.final_loss?.toFixed(4)}</span>
                </div>
                <div className="stat-card glass">
                    <span className="stat-label"><Droplets size={16} /> Mean SASA</span>
                    <span className="stat-value">
                        {(data.candidates.reduce((acc, c) => acc + c.SASA, 0) / data.candidates.length).toFixed(1)} Å²
                    </span>
                </div>
                <div className="stat-card glass">
                    <span className="stat-label"><Shield size={16} /> Status</span>
                    <span className="stat-value" style={{ color: '#4ade80' }}>{data.summary.status}</span>
                </div>
            </div>

            <div className="main-grid">
                <div className="card glass chart-container">
                    <div className="chart-title"><Database size={20} color="#818cf8" /> Training Convergence</div>
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data.training_history}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                            <XAxis dataKey="Epoch" stroke="#71717a" fontSize={12} tickLine={false} axisLine={false} />
                            <YAxis stroke="#71717a" fontSize={12} tickLine={false} axisLine={false} />
                            <Tooltip
                                contentStyle={{ background: '#18181b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                itemStyle={{ color: '#818cf8' }}
                            />
                            <Line
                                type="monotone"
                                dataKey="Loss"
                                stroke="#818cf8"
                                strokeWidth={3}
                                dot={{ r: 4, fill: '#818cf8', strokeWidth: 0 }}
                                activeDot={{ r: 6, strokeWidth: 0 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </div>

                <div className="card glass chart-container">
                    <div className="chart-title">
                        <Droplets size={20} color="#22d3ee" />
                        RMSF Profile: LYS {selectedSite}
                        <span style={{ fontSize: '0.8rem', color: '#71717a', marginLeft: 'auto' }}>Phosphate Cloud Shielding</span>
                    </div>
                    <div className="site-selector">
                        {data.candidates.map(c => (
                            <button
                                key={c.Rank + c.ResID}
                                className={`site-btn ${selectedSite === c.ResID ? 'active' : ''}`}
                                onClick={() => setSelectedSite(c.ResID)}
                            >
                                K{c.ResID}
                            </button>
                        ))}
                    </div>
                    <ResponsiveContainer width="100%" height="80%">
                        <AreaChart data={rmsfData}>
                            <defs>
                                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                            <XAxis dataKey="pos" stroke="#71717a" fontSize={10} hide />
                            <YAxis stroke="#71717a" fontSize={12} tickLine={false} axisLine={false} />
                            <Tooltip
                                contentStyle={{ background: '#18181b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                            />
                            <Area
                                type="monotone"
                                dataKey="value"
                                stroke="#22d3ee"
                                fillOpacity={1}
                                fill="url(#colorValue)"
                                strokeWidth={2}
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="card glass" style={{ padding: '24px' }}>
                <div className="chart-title"><Compass size={20} color="#c084fc" /> Candidate Ranking (Tier 1 & 2)</div>
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Residue ID</th>
                                <th>SASA (Å²)</th>
                                <th>Min Dist to PPZ (Å)</th>
                                <th>Bio-Availability</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.candidates.map((c, i) => (
                                <tr key={i} onClick={() => setSelectedSite(c.ResID)} style={{ cursor: 'pointer' }}>
                                    <td><span className="rank-badge">#{c.Rank}</span></td>
                                    <td><strong>LYS {c.ResID}</strong></td>
                                    <td>{c.SASA.toFixed(2)}</td>
                                    <td>{c.Dist_to_PPZ.toFixed(2)}</td>
                                    <td>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                            <div style={{ height: '6px', width: '100px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px' }}>
                                                <div style={{ height: '100%', width: `${Math.min(100, c.SASA / 1.5)}%`, background: '#4ade80', borderRadius: '3px' }}></div>
                                            </div>
                                            <span style={{ fontSize: '0.75rem', color: '#a1a1aa' }}>High</span>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <footer style={{ marginTop: '40px', textAlign: 'center', color: '#3f3f46', fontSize: '0.875rem' }}>
                &copy; 2025 Glyco-Immunology Virtual Lab • Powered by Gemini Agentic AI
            </footer>
        </div>
    )
}

export default App
