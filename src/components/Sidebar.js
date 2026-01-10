'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, FileText, AlertTriangle, PieChart, ShieldAlert } from 'lucide-react';

const NAV_ITEMS = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Expectation Engine', href: '/engine/expectation', icon: FileText },
    { name: 'Reality Engine', href: '/engine/reality', icon: PieChart },
    { name: 'Risk Analysis', href: '/risk', icon: ShieldAlert },
    { name: 'Reports', href: '/reports', icon: AlertTriangle },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="sidebar">
            <div className="logo-container">
                <h1 className="logo-text">
                    VERITAS
                </h1>
                <p className="text-xs font-bold text-muted uppercase tracking-wider">Finance Guard AI</p>
            </div>

            <nav className="nav-menu">
                {NAV_ITEMS.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`nav-item ${isActive ? 'active' : ''}`}
                        >
                            <Icon size={18} />
                            <span>{item.name}</span>
                        </Link>
                    );
                })}
            </nav>

            <div className="sidebar-footer">
                <div className="user-profile">
                    <div className="avatar"></div>
                    <div>
                        <p className="text-sm font-bold text-white">Admin User</p>
                        <p className="text-xs text-muted">Regulator Access</p>
                    </div>
                </div>
            </div>
        </aside>
    );
}
