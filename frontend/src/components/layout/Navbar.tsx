import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Bot, Globe, ChevronDown, UserCheck, Shield } from 'lucide-react';

interface NavbarProps {
  onToggleMentor: () => void;
  currentLanguage: string;
  onLanguageChange: (lang: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onToggleMentor, currentLanguage, onLanguageChange }) => {
  const { user, switchDemoUser, logout } = useAuth();
  const [showDemoMenu, setShowDemoMenu] = useState(false);
  const [showLangMenu, setShowLangMenu] = useState(false);

  const demoAccounts = [
    { name: 'Arif Mohamed', branch: 'AI & Data Science (3rd yr)', email: 'arif@skillpath.dev' },
    { name: 'Priya Sharma', branch: '1st Year Beginner (No skills)', email: 'priya@skillpath.dev' },
    { name: 'Rohan Patel', branch: 'Full Stack Goal (Self-taught)', email: 'rohan@skillpath.dev' },
    { name: 'Ananya Sen', branch: 'Career Switcher (Data Analyst)', email: 'ananya@skillpath.dev' },
    { name: 'Admin Portal', branch: 'College / Company Admin', email: 'admin@skillpath.dev' },
  ];

  return (
    <header className="sticky top-0 z-30 h-16 bg-surface/95 backdrop-blur-sm border-b border-border px-4 lg:px-8 flex items-center justify-between">
      {/* Brand & Goal Badge */}
      <div className="flex items-center gap-3">
        <a href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-md bg-primary flex items-center justify-center text-white font-serif font-bold text-lg shadow-soft group-hover:bg-primary-hover transition-colors">
            S
          </div>
          <span className="font-serif font-bold text-xl text-ink tracking-tight">
            Skill<span className="text-primary">Path</span>
          </span>
        </a>

        {user?.career_goal && (
          <div className="hidden sm:flex items-center gap-2 pl-3 ml-3 border-l border-border">
            <span className="text-xs text-ink-secondary">Target Goal:</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary-tint text-primary border border-primary/20">
              {user.career_goal}
            </span>
          </div>
        )}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Language selector */}
        <div className="relative">
          <button
            onClick={() => {
              setShowLangMenu(!showLangMenu);
              setShowDemoMenu(false);
            }}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-border text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
          >
            <Globe className="w-3.5 h-3.5 text-primary" />
            <span className="uppercase">{currentLanguage}</span>
            <ChevronDown className="w-3 h-3 text-ink-muted" />
          </button>

          {showLangMenu && (
            <div className="absolute right-0 mt-1 w-36 bg-surface rounded-md border border-border shadow-card py-1 z-40">
              <button
                onClick={() => { onLanguageChange('en'); setShowLangMenu(false); }}
                className={`w-full text-left px-3 py-1.5 text-xs hover:bg-bg ${currentLanguage === 'en' ? 'font-bold text-primary' : 'text-ink'}`}
              >
                English
              </button>
              <button
                onClick={() => { onLanguageChange('hi'); setShowLangMenu(false); }}
                className={`w-full text-left px-3 py-1.5 text-xs hover:bg-bg ${currentLanguage === 'hi' ? 'font-bold text-primary' : 'text-ink'}`}
              >
                हिन्दी (Hindi)
              </button>
              <button
                onClick={() => { onLanguageChange('ta'); setShowLangMenu(false); }}
                className={`w-full text-left px-3 py-1.5 text-xs hover:bg-bg ${currentLanguage === 'ta' ? 'font-bold text-primary' : 'text-ink'}`}
              >
                தமிழ் (Tamil)
              </button>
            </div>
          )}
        </div>

        {/* Demo Switcher */}
        <div className="relative">
          <button
            onClick={() => {
              setShowDemoMenu(!showDemoMenu);
              setShowLangMenu(false);
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-border bg-bg text-xs font-medium text-ink hover:border-primary/40 transition-colors"
          >
            {user?.role === 'admin' ? (
              <Shield className="w-3.5 h-3.5 text-status-warning" />
            ) : (
              <UserCheck className="w-3.5 h-3.5 text-primary" />
            )}
            <span className="truncate max-w-[100px] sm:max-w-[130px]">{user?.full_name || 'Switch Learner'}</span>
            <ChevronDown className="w-3 h-3 text-ink-muted" />
          </button>

          {showDemoMenu && (
            <div className="absolute right-0 mt-1 w-72 bg-surface rounded-md border border-border shadow-card p-2 z-40">
              <div className="text-[11px] font-semibold text-ink-muted px-2 py-1 uppercase tracking-wider">
                Switch Demo Persona
              </div>
              {demoAccounts.map((acct) => (
                <button
                  key={acct.email}
                  onClick={() => {
                    switchDemoUser(acct.email);
                    setShowDemoMenu(false);
                  }}
                  className={`w-full text-left p-2 rounded-sm text-xs hover:bg-bg transition-colors flex flex-col gap-0.5 ${
                    user?.email === acct.email ? 'bg-primary-tint/60 font-semibold text-primary' : 'text-ink'
                  }`}
                >
                  <span className="font-medium text-ink">{acct.name}</span>
                  <span className="text-[11px] text-ink-secondary">{acct.branch}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* AI Mentor slide-over toggle button */}
        <button
          onClick={onToggleMentor}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-primary text-white text-xs font-medium hover:bg-primary-hover shadow-soft transition-colors"
        >
          <Bot className="w-4 h-4" />
          <span className="hidden sm:inline">AI Mentor</span>
        </button>
      </div>
    </header>
  );
};

