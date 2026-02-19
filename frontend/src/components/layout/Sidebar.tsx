import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Search,
  Network,
  FileCheck,
  TrendingUp,
  Plug,
  Store,
  Globe2,
  Award,
} from 'lucide-react';
import { cn } from '@utils/cn';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Visibility Research', href: '/research', icon: Search },
  { name: 'Entity Graph', href: '/entity-graph', icon: Network },
  { name: 'Evaluation Protocol', href: '/evaluation', icon: FileCheck },
  { name: 'Business Impact', href: '/business-impact', icon: TrendingUp },
  { name: 'Integrations', href: '/integrations', icon: Plug },
  { name: 'Store Management', href: '/stores', icon: Store },
  { name: 'Geo Analysis', href: '/geo-analysis', icon: Globe2 },
  { name: 'Benchmark', href: '/benchmark', icon: Award },
];

const Sidebar = () => {
  return (
    <aside className="w-64 glass-card m-4 p-4 flex flex-col">
      {/* Logo */}
      <div className="mb-8 px-2">
        <h1 className="text-2xl font-bold text-gradient">
          智投
        </h1>
        <p className="text-xs text-neutral-500 mt-1">
          AI Search Visibility Platform
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors',
                'text-sm font-medium',
                isActive
                  ? 'bg-primary-500/10 text-primary-400'
                  : 'text-neutral-400 hover:bg-white/5 hover:text-neutral-200'
              )
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="mt-auto pt-4 border-t border-white/10">
        <div className="px-3 py-2 text-xs text-neutral-500">
          <p>Version 1.0.0</p>
          <p className="mt-1">© 2026 智投</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
