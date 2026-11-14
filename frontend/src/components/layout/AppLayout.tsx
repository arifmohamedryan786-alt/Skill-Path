import React, { useState } from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { MentorSlideOver } from '../mentor/MentorSlideOver';

interface AppLayoutProps {
  currentPath: string;
  onNavigate: (path: string) => void;
  currentLanguage: string;
  onLanguageChange: (lang: string) => void;
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  currentPath,
  onNavigate,
  currentLanguage,
  onLanguageChange,
  children,
}) => {
  const [isMentorOpen, setIsMentorOpen] = useState(false);

  return (
    <div className="min-h-screen bg-bg text-ink flex flex-col font-sans">
      <Navbar
        onToggleMentor={() => setIsMentorOpen(!isMentorOpen)}
        currentLanguage={currentLanguage}
        onLanguageChange={onLanguageChange}
      />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar currentPath={currentPath} onNavigate={onNavigate} />
        <main className="flex-1 overflow-y-auto p-4 md:p-8 max-w-7xl mx-auto w-full pb-20 md:pb-8">
          {children}
        </main>
      </div>
      <MentorSlideOver isOpen={isMentorOpen} onClose={() => setIsMentorOpen(false)} />
    </div>
  );
};

