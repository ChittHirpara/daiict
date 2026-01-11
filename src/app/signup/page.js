'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Mail, Lock, User, ArrowRight, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

export default function SignupPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.type === 'text' && e.target.name === undefined ? 'name' : e.target.type]: e.target.value });
        // Fixing a small potential bug in handleChange above by being explicit below
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const res = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.message || 'Signup failed');
            }

            // Redirect to login or dashboard
            router.push('/login');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
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
                    <h1 className="text-3xl font-bold text-white mb-2">Create Account</h1>
                    <p className="text-slate-400">Join Veritas Finance Guard</p>
                </div>

                {error && (
                    <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSignup} className="space-y-5">
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Full Name</label>
                        <div className="input-group">
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            />
                            <User className="input-icon" size={18} />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Email</label>
                        <div className="input-group">
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                            />
                            <Mail className="input-icon" size={18} />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Password</label>
                        <div className="input-group">
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleInputChange}
                                className="input-field"
                                required
                                minLength={6}
                            />
                            <Lock className="input-icon" size={18} />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full btn btn-primary py-3 rounded-xl flex items-center justify-center gap-2 mt-4 group"
                    >
                        {loading ? 'Creating Account...' : (
                            <>
                                Sign Up <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>
                </form>

                <p className="text-center mt-8 text-sm text-slate-500">
                    Already have an account? <Link href="/login" className="text-blue-400 hover:text-blue-300 font-medium">Log In</Link>
                </p>
            </div>
        </div>
    );
}
