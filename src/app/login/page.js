'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Lock, Mail, ScanFace, ArrowRight, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

export default function LoginPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [faceIdLoading, setFaceIdLoading] = useState(false);

    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { type, value } = e.target;
        setFormData(prev => ({ ...prev, [type]: value }));
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await res.json();

            if (!res.ok) throw new Error(data.message || 'Login failed');

            // Store user info if needed or just redirect
            // localStorage.setItem('user', JSON.stringify(data.user));

            router.push('/');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleFaceId = () => {
        setFaceIdLoading(true);
        // Mock Face ID
        setTimeout(() => {
            setFaceIdLoading(false);
            router.push('/');
        }, 2000);
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden bg-[#0a0a0a]">
            {/* Background gradients */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 rounded-full blur-[120px]"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/20 rounded-full blur-[120px]"></div>
            </div>

            <div className="card glass w-full max-w-md p-8 relative z-10 border border-white/10 shadow-2xl">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 mb-4 shadow-lg shadow-purple-500/20">
                        <ShieldCheck size={32} className="text-white" />
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
                    <p className="text-slate-400">Sign in to Veritas Finance Dashboard</p>
                </div>

                {error && (
                    <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleLogin} className="space-y-5">
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Email</label>
                        <div className="input-group">
                            <input
                                type="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            />
                            <Mail className="input-icon" size={18} />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between items-center ml-1">
                            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Password</label>
                            <Link href="#" className="text-xs text-blue-400 hover:text-blue-300">Forgot?</Link>
                        </div>
                        <div className="input-group">
                            <input
                                type="password"
                                value={formData.password}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            />
                            <Lock className="input-icon" size={18} />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading || faceIdLoading}
                        className="w-full btn btn-primary py-3 rounded-xl flex items-center justify-center gap-2 mt-2 group"
                    >
                        {loading ? 'Authenticating...' : (
                            <>
                                Sign In <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>
                </form>

                <div className="relative my-8">
                    <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-700/50"></div></div>
                    <div className="relative flex justify-center text-xs uppercase"><span className="bg-[#0a0a0a] px-4 text-slate-500 font-medium">Or continue with</span></div>
                </div>

                <button
                    type="button"
                    onClick={handleFaceId}
                    disabled={loading || faceIdLoading}
                    className={`w-full py-3 rounded-xl border border-slate-700/50 bg-white/5 text-white hover:bg-white/10 transition-all flex items-center justify-center gap-3 relative overflow-hidden ${faceIdLoading ? 'border-purple-500/50 text-purple-400' : ''}`}
                >
                    {faceIdLoading && (
                        <div className="absolute inset-0 bg-purple-500/10 flex items-center justify-center">
                            <div className="w-full h-0.5 bg-purple-500/50 absolute top-0 animate-[scan_2s_ease-in-out_infinite]"></div>
                        </div>
                    )}
                    <ScanFace size={20} />
                    {faceIdLoading ? 'Scanning Face...' : 'Face ID Verification'}
                </button>

                <p className="text-center mt-8 text-sm text-slate-500">
                    Don't have an account? <Link href="/signup" className="text-blue-400 hover:text-blue-300 font-medium">Sign Up</Link>
                </p>

                {/* Global CSS for custom animations inside this page if needed, normally goes in globals.css but for quick prototyping inline styles works or style tag */}
                <style jsx>{`
            @keyframes scan {
                0% { top: 0; opacity: 1; }
                50% { top: 100%; opacity: 1; }
                51% { top: 100%; opacity: 0; }
                100% { top: 0; opacity: 0; }
            }
        `}</style>
            </div>
        </div>
    );
}
