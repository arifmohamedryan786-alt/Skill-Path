import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
import { GlossaryProvider } from './context/GlossaryContext';
import { AppLayout } from './components/layout/AppLayout';
import i18n from './i18n';

// Pages
import { LoginPage } from './pages/LoginPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { DashboardPage } from './pages/DashboardPage';
import { DiscoveryPage } from './pages/DiscoveryPage';
import { CareerExplorerPage } from './pages/CareerExplorerPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { SkillAnalysisPage } from './pages/SkillAnalysisPage';
import { AssessmentsPage } from './pages/AssessmentsPage';
import { FlightSimulatorPage } from './pages/FlightSimulatorPage';
import { PassportPage } from './pages/PassportPage';
import { PublicPassportPage } from './pages/PublicPassportPage';
import { InterviewCoachPage } from './pages/InterviewCoachPage';
import { CareerGuidePage } from './pages/CareerGuidePage';
import { MentorPage } from './pages/MentorPage';
import { ProgressPage } from './pages/ProgressPage';
import { ProfilePage } from './pages/ProfilePage';
import { AdminPage } from './pages/AdminPage';
import { GlossaryPage } from './pages/GlossaryPage';
import { PracticeQuestionsPage } from './pages/PracticeQuestionsPage';

const AppContent: React.FC = () => {
  const { user, token, loading } = useAuth();
  const [currentPath, setCurrentPath] = useState<string>(() => {
    return window.location.pathname || '/dashboard';
  });
  const [currentLanguage, setCurrentLanguage] = useState<string>(() => {
    return localStorage.getItem('skillpath_language') || 'en';
  });

  // Sync browser back/forward buttons
  useEffect(() => {
    const handlePopState = () => {
      setCurrentPath(window.location.pathname || '/dashboard');
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (path: string) => {
    window.history.pushState({}, '', path);
    setCurrentPath(path);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleLanguageChange = (lang: string) => {
    setCurrentLanguage(lang);
    localStorage.setItem('skillpath_language', lang);
    i18n.changeLanguage(lang);
  };

  // 1. Check for public passport URL: /passport/public/:slug or /passport/:slug (not /passport)
  if (currentPath.startsWith('/passport/') && currentPath !== '/passport') {
    const slug = currentPath.replace('/passport/public/', '').replace('/passport/', '');
    return <PublicPassportPage slug={slug} onNavigate={navigate} />;
  }

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-bg flex items-center justify-center p-4">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-3 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="font-serif text-ink font-semibold text-sm">Loading SkillPath...</p>
        </div>
      </div>
    );
  }

  // Unauthenticated user -> Login
  if (!token || !user) {
    return <LoginPage onNavigate={navigate} />;
  }

  // If user hasn't selected goal or needs onboarding
  if (currentPath === '/onboarding') {
    return <OnboardingPage onNavigate={navigate} />;
  }

  // Render appropriate page content inside AppLayout
  const renderPage = () => {
    switch (currentPath) {
      case '/discovery':
        return <DiscoveryPage onNavigate={navigate} />;
      case '/careers':
        return <CareerExplorerPage onNavigate={navigate} />;
      case '/roadmap':
        return <RoadmapPage onNavigate={navigate} />;
      case '/skills':
        return <SkillAnalysisPage onNavigate={navigate} />;
      case '/assessments':
        return <AssessmentsPage onNavigate={navigate} />;
      case '/practice':
        return <PracticeQuestionsPage onNavigate={navigate} />;
      case '/simulator':
        return <FlightSimulatorPage onNavigate={navigate} />;
      case '/passport':
        return <PassportPage onNavigate={navigate} />;
      case '/interview':
        return <InterviewCoachPage onNavigate={navigate} />;
      case '/guide':
        return <CareerGuidePage onNavigate={navigate} />;
      case '/mentor':
        return <MentorPage onNavigate={navigate} />;
      case '/progress':
        return <ProgressPage onNavigate={navigate} />;
      case '/profile':
        return <ProfilePage onNavigate={navigate} />;
      case '/admin':
        return <AdminPage onNavigate={navigate} />;
      case '/glossary':
        return <GlossaryPage onNavigate={navigate} />;
      case '/dashboard':
      default:
        return <DashboardPage onNavigate={navigate} />;
    }
  };

  return (
    <AppLayout
      currentPath={currentPath}
      onNavigate={navigate}
      currentLanguage={currentLanguage}
      onLanguageChange={handleLanguageChange}
    >
      {renderPage()}
    </AppLayout>
  );
};

export const App: React.FC = () => {
  return (
    <ToastProvider>
      <AuthProvider>
        <GlossaryProvider>
          <AppContent />
        </GlossaryProvider>
      </AuthProvider>
    </ToastProvider>
  );
};

export default App;
