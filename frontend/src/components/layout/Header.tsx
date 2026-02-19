import { Bell, Settings, User } from 'lucide-react';
import { Button } from '@components/ui/Button';

const Header = () => {
  return (
    <header className="h-16 glass-card m-4 mb-0 px-6 flex items-center justify-between">
      {/* Search Bar */}
      <div className="flex-1 max-w-xl">
        <div className="relative">
          <input
            type="text"
            placeholder="Search..."
            className="w-full px-4 py-2 bg-neutral-800/50 border border-neutral-700 rounded-lg text-neutral-50 placeholder-neutral-500 focus:outline-none focus:border-primary-500 transition-colors"
          />
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" className="relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-error-500 rounded-full"></span>
        </Button>
        
        <Button variant="ghost" size="sm">
          <Settings className="w-5 h-5" />
        </Button>

        <div className="h-8 w-px bg-white/10 mx-2"></div>

        <Button variant="ghost" size="sm" className="gap-2">
          <div className="w-8 h-8 rounded-full bg-primary-500/20 flex items-center justify-center">
            <User className="w-4 h-4 text-primary-400" />
          </div>
          <span className="text-sm font-medium">Admin</span>
        </Button>
      </div>
    </header>
  );
};

export default Header;
