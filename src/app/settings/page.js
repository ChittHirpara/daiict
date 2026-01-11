'use client';

import { Settings as SettingsIcon, User, Shield, Bell, Moon, Sun, Smartphone, LogOut, Trash2 } from 'lucide-react';
export default function SettingsPage() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const res = await fetch('/api/users');
            if (res.ok) {
                const data = await res.json();
                setUsers(data);
            }
        } catch (error) {
            console.error('Failed to fetch users', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteUser = async (id) => {
        if (!confirm('Are you sure you want to delete this user?')) return;

        try {
            const res = await fetch(`/api/users?id=${id}`, {
                method: 'DELETE',
            });

            if (res.ok) {
                setUsers(users.filter(u => u._id !== id));
            } else {
                alert('Failed to delete user');
            }
        } catch (error) {
            console.error('Delete error', error);
        }
    };

    return (
        <div className="container mx-auto p-6 space-y-8">
            <div className="page-header mb-8">
                <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
                    Settings
                </h1>
                <p className="text-slate-400 mt-2 flex items-center gap-2">
                    <SettingsIcon size={16} className="text-blue-400" />
                    Manage system preferences and user access controls.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Left Column */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="card glass p-0 overflow-hidden">
                        <div className="p-4 bg-white/5 border-b border-white/5 font-bold text-white">System Settings</div>
                        <div className="flex flex-col">
                            <button className="flex items-center gap-3 p-4 text-left text-blue-400 bg-blue-500/10 border-l-2 border-blue-500 transition-colors">
                                <User size={18} /> User Management
                            </button>
                            <button className="flex items-center gap-3 p-4 text-left text-slate-400 hover:bg-white/5 hover:text-white transition-colors">
                                <Shield size={18} /> Security & Face ID
                            </button>
                            <button className="flex items-center gap-3 p-4 text-left text-slate-400 hover:bg-white/5 hover:text-white transition-colors">
                                <Bell size={18} /> Notifications
                            </button>
                            <button className="flex items-center gap-3 p-4 text-left text-slate-400 hover:bg-white/5 hover:text-white transition-colors">
                                <Smartphone size={18} /> API & Integrations
                            </button>
                        </div>
                    </div>

                    <div className="card glass p-6">
                        <h3 className="font-bold text-white mb-4">Appearance</h3>
                        <div className="flex items-center justify-between p-3 bg-black/20 rounded-lg">
                            <div className="flex items-center gap-2 text-sm text-slate-300">
                                <Moon size={16} /> Dark Mode
                            </div>
                            <div className="w-10 h-6 bg-blue-600 rounded-full relative cursor-pointer">
                                <div className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full shadow-sm"></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column */}
                <div className="lg:col-span-2 space-y-6">
                    {/* User Management Section */}
                    <div className="card glass">
                        <div className="flex justify-between items-center mb-6">
                            <div>
                                <h2 className="text-xl font-bold text-white">User Management</h2>
                                <p className="text-sm text-slate-400">View and manage authorized users.</p>
                            </div>
                            <button className="btn btn-primary text-sm">+ Add User</button>
                        </div>

                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="border-b border-slate-700/50 text-slate-500 text-xs uppercase tracking-wider">
                                        <th className="p-3">User</th>
                                        <th className="p-3">Role</th>
                                        <th className="p-3">Status</th>
                                        <th className="p-3 text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800/50">
                                    {users.map(user => (
                                        <tr key={user._id} className="group hover:bg-white/5 transition-colors">
                                            <td className="p-3">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold text-white">
                                                        {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                                                    </div>
                                                    <div>
                                                        <div className="text-sm font-medium text-white">{user.name}</div>
                                                        <div className="text-xs text-slate-500">{user.email}</div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="p-3">
                                                <span className="text-sm text-slate-300 capitalize">{user.role}</span>
                                            </td>
                                            <td className="p-3">
                                                <span className="text-xs px-2 py-1 rounded-full border bg-green-500/10 text-green-400 border-green-500/20">
                                                    Active
                                                </span>
                                            </td>
                                            <td className="p-3 text-right">
                                                <button
                                                    onClick={() => handleDeleteUser(user._id)}
                                                    className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors"
                                                    title="Delete User"
                                                >
                                                    <Trash2 size={16} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                    {users.length === 0 && !loading && (
                                        <tr>
                                            <td colSpan="4" className="p-4 text-center text-muted">No users found.</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
