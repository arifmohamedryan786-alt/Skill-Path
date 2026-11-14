import React from 'react';
import {
  Compass,
  Map,
  BarChart3,
  CheckSquare,
  Plane,
  Award,
  Mic,
  BookOpen,
  Bot,
  TrendingUp,
  User,
  Shield,
  Layers,
  LayoutDashboard,
  BookMarked,
  Code2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface SidebarProps {
  currentPath: string;
  onNavigate: (path: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentPath, onNavigate }) => {
  const { user } = useAuth();

  const navLinks = [
    { label: 'Overview', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Career Discovery', path: '/discovery', icon: Compass },
    { label: 'Career Explorer', path: '/careers', icon: Layers },
    { label: 'My Roadmap', path: '/roadmap', icon: Map },
    { label: 'Skill Gap Analysis', path: '/skills', icon: BarChart3 },
    { label: 'Checkpoint Tests', path: '/assessments', icon: CheckSquare },
    { label: 'Practice Questions', path: '/practice', icon: Code2 },
    { label: 'Flight Simulator', path: '/simulator', icon: Plane },
    { label: 'Verified Passport', path: '/passport', icon: Award },
    { label: 'Mock Interview', path: '/interview', icon: Mic },
    { label: 'Career Guide', path: '/guide', icon: BookOpen },
    { label: 'AI Mentor', path: '/mentor', icon: Bot },
    { label: 'My Progress', path: '/progress', icon: TrendingUp },
    { label: 'Glossary Terms', path: '/glossary', icon: BookMarked },
    { label: 'Profile', path: '/profile', icon: User },
  ];

  if (user?.role === 'admin') {
    navLinks.push({ label: 'Admin Analytics', path: '/admin', icon: Shield });
  }

  return (
    <>
      {/* Desktop Left Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-surface border-r border-border shrink-0 min-h-[calc(100vh-4rem)]">
        <div className="p-4 flex-1 overflow-y-auto">
          <div className="text-[11px] font-semibold text-ink-muted px-3 mb-2 uppercase tracking-wider">
            Navigation
          </div>
          <nav className="space-y-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = currentPath === link.path;
              return (
                <button
                  key={link.path}
                  onClick={() => onNavigate(link.path)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors text-left ${
                    isActive
                      ? 'bg-primary-tint text-primary font-semibold'
                      : 'text-ink-secondary hover:text-ink hover:bg-bg'
                  }`}
                >
                  <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-primary' : 'text-ink-muted'}`} />
                  <span className="truncate">{link.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Footer note */}
        <div className="p-4 border-t border-border/60 text-[11px] text-ink-muted">
          SkillPath Zero-to-Job Platform<br />
          Built for clarity and focus.
        </div>
      </aside>

      {/* Mobile Bottom Tab Bar */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-surface border-t border-border z-40 flex items-center justify-around px-2 shadow-card">
        <button
          onClick={() => onNavigate('/dashboard')}
          className={`flex flex-col items-center gap-1 p-1 text-[10px] ${currentPath === '/dashboard' ? 'text-primary font-bold' : 'text-ink-secondary'}`}
        >
          <LayoutDashboard className="w-4 h-4" />
          <span>Home</span>
        </button>
        <button
          onClick={() => onNavigate('/roadmap')}
          className={`flex flex-col items-center gap-1 p-1 text-[10px] ${currentPath === '/roadmap' ? 'text-primary font-bold' : 'text-ink-secondary'}`}
        >
          <Map className="w-4 h-4" />
          <span>Roadmap</span>
        </button>
        <button
          onClick={() => onNavigate('/simulator')}
          className={`flex flex-col items-center gap-1 p-1 text-[10px] ${currentPath === '/simulator' ? 'text-primary font-bold' : 'text-ink-secondary'}`}
        >
          <Plane className="w-4 h-4" />
          <span>Simulator</span>
        </button>
        <button
          onClick={() => onNavigate('/passport')}
          className={`flex flex-col items-center gap-1 p-1 text-[10px] ${currentPath === '/passport' ? 'text-primary font-bold' : 'text-ink-secondary'}`}
        >
          <Award className="w-4 h-4" />
          <span>Passport</span>
        </button>
        <button
          onClick={() => onNavigate('/mentor')}
          className={`flex flex-col items-center gap-1 p-1 text-[10px] ${currentPath === '/mentor' ? 'text-primary font-bold' : 'text-ink-secondary'}`}
        >
          <Bot className="w-4 h-4" />
          <span>Mentor</span>
        </button>
      </nav>
    </>
  );
};

