import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { CompassIllustration } from '../components/illustrations/LineArtIllustrations';
import {
  ArrowRight,
  Sparkles,
  UserCheck,
  Shield,
  GraduationCap,
  Briefcase,
  Compass,
  Mail,
  Lock,
  User as UserIcon,
  AlertCircle,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export const LoginPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { login, register, guestLogin, switchDemoUser } = useAuth();
  const { showToast } = useToast();

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Email/password form state (collapsible)
  const [showEmailAuth, setShowEmailAuth] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');

  // 1. Guest Journey: 1-click start without sign-up friction
  const handleStartJourney = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      await guestLogin();
      showToast('Welcome to SkillPath! Let’s explore careers tailored to you.', 'success');
      onNavigate('/onboarding');
    } catch (err: any) {
      const msg = err.message || 'Unable to start guest session. Please check your connection.';
      setErrorMessage(msg);
      showToast(msg, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 2. Demo Persona 1-Click Login (passwordless endpoint)
  const handleDemoLogin = async (personaName: string, displayName: string, targetPath: string = '/dashboard') => {
    setLoading(true);
    setErrorMessage(null);
    try {
      await switchDemoUser(personaName);
      showToast(`Logged in as ${displayName}`, 'success');
      onNavigate(targetPath);
    } catch (err: any) {
      const msg = err.message || `Failed to sign in as ${displayName}. Please ensure the backend is running.`;
      setErrorMessage(msg);
      showToast(msg, 'error');
    } finally {
      setLoading(false);
    }
  };

  // 3. Email & Password Form Submit
  const handleEmailAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setErrorMessage('Please enter both email and password.');
      showToast('Please enter both email and password.', 'warning');
      return;
    }
    setLoading(true);
    setErrorMessage(null);
    try {
      if (isRegister) {
        await register(email, password, fullName || 'Learner');
        showToast('Account created successfully! Welcome to SkillPath.', 'success');
        onNavigate('/onboarding');
      } else {
        await login(email, password);
        showToast('Signed in successfully!', 'success');
        onNavigate('/dashboard');
      }
    } catch (err: any) {
      const msg = err.message || 'Authentication failed. Please check your credentials.';
      setErrorMessage(msg);
      showToast(msg, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg flex flex-col justify-between p-4 sm:p-6 lg:p-8">
      <div className="max-w-5xl mx-auto w-full my-auto">
        {/* Brand Header */}
        <div className="flex items-center justify-between mb-8 pb-4 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center text-white font-serif font-bold text-xl shadow-soft">
              S
            </div>
            <div>
              <span className="font-serif text-xl font-bold text-ink">SkillPath</span>
              <span className="text-xs text-ink-muted ml-2 font-mono">v1.0 • Zero to Job-Ready</span>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-xs text-ink-secondary">
            <span className="inline-block w-2 h-2 rounded-full bg-status-success animate-pulse" />
            <span>AI Multi-Agent Engine Ready</span>
          </div>
        </div>

        {/* Global Error Message */}
        {errorMessage && (
          <div className="mb-6 p-4 rounded-lg bg-status-danger-tint border border-status-danger/30 text-status-danger text-xs flex items-start gap-2 shadow-xs">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span className="leading-relaxed font-medium">{errorMessage}</span>
          </div>
        )}

        {/* Hero Section */}
        <div className="bg-surface border border-border rounded-xl p-6 sm:p-10 shadow-card mb-8 grid md:grid-cols-5 gap-8 items-center">
          <div className="md:col-span-3 space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-tint/70 text-primary text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Personalized Career Roadmaps for Every Student</span>
            </div>
            <h1 className="font-serif text-3xl sm:text-4xl font-bold text-ink leading-tight">
              From Zero to Job-Ready.
            </h1>
            <p className="text-sm text-ink-secondary leading-relaxed">
              Never wonder what to do after college again. Discover careers that fit you, bridge your missing skills, know where to start this week, and walk a verified roadmap to employment.
            </p>

            {/* Primary Action Button */}
            <div className="pt-2 flex flex-col sm:flex-row gap-3">
              <button
                type="button"
                onClick={handleStartJourney}
                disabled={loading}
                className="inline-flex items-center justify-center gap-2 px-6 py-3.5 bg-primary text-white text-sm font-semibold rounded-lg hover:bg-primary-hover transition-colors shadow-soft hover:shadow-card cursor-pointer disabled:opacity-60"
              >
                <span>Start My Career Journey</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                type="button"
                onClick={() => handleDemoLogin('arif', 'Arif Mohamed (3rd Yr AI & DS)')}
                disabled={loading}
                className="inline-flex items-center justify-center gap-2 px-5 py-3.5 bg-surface border border-border text-ink hover:border-primary text-sm font-semibold rounded-lg hover:bg-primary-tint/20 transition-colors shadow-xs cursor-pointer disabled:opacity-60"
              >
                <UserCheck className="w-4 h-4 text-primary" />
                <span>Explore as Arif (AI Student)</span>
              </button>
            </div>

            <p className="text-[11px] text-ink-muted">
              ✨ Free instant exploration • No credit card required • Prior tech experience not required
            </p>
          </div>

          <div className="md:col-span-2 flex flex-col items-center justify-center bg-primary-tint/30 rounded-xl p-6 border border-border/50 text-center">
            <CompassIllustration className="w-36 h-36 mb-3" />
            <h3 className="font-serif font-bold text-ink text-sm mb-1">Adaptive Learning Engine</h3>
            <p className="text-xs text-ink-secondary leading-relaxed">
              Autonomous agents collaborate to discover careers, simulate job-ready dates, and verify skill evidence.
            </p>
          </div>
        </div>

        {/* Demo Personas Grid */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-serif text-lg font-bold text-ink">Explore Pre-loaded Demo Personas</h2>
              <p className="text-xs text-ink-secondary">
                Click any scenario below to evaluate SkillPath through real student journeys.
              </p>
            </div>
            <span className="text-[11px] font-semibold text-accent uppercase tracking-wider bg-accent/10 px-2.5 py-1 rounded-md">
              1-Click Evaluation
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Persona 1: Arif Mohamed */}
            <button
              type="button"
              onClick={() => handleDemoLogin('arif', 'Arif Mohamed')}
              disabled={loading}
              className="p-4 bg-surface border border-border rounded-lg text-left hover:border-primary hover:shadow-soft transition-all group cursor-pointer disabled:opacity-60 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-8 h-8 rounded-md bg-primary-tint flex items-center justify-center text-primary">
                    <Compass className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-primary bg-primary-tint/60 px-2 py-0.5 rounded">
                    Primary Persona
                  </span>
                </div>
                <h3 className="font-serif font-bold text-sm text-ink group-hover:text-primary transition-colors">
                  Arif Mohamed
                </h3>
                <div className="text-xs text-ink-secondary mt-0.5 font-medium">
                  B.Tech AI & Data Science, 3rd Year
                </div>
                <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                  "I don't know what to do after college." Evaluates ML Engineer vs Data Analyst roadmaps.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 flex items-center justify-between text-xs font-semibold text-primary">
                <span>Open Dashboard</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </div>
            </button>

            {/* Persona 2: Priya Sharma */}
            <button
              type="button"
              onClick={() => handleDemoLogin('priya', 'Priya Sharma')}
              disabled={loading}
              className="p-4 bg-surface border border-border rounded-lg text-left hover:border-primary hover:shadow-soft transition-all group cursor-pointer disabled:opacity-60 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-8 h-8 rounded-md bg-accent/15 flex items-center justify-center text-accent">
                    <GraduationCap className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-accent bg-accent/10 px-2 py-0.5 rounded">
                    Beginner
                  </span>
                </div>
                <h3 className="font-serif font-bold text-sm text-ink group-hover:text-primary transition-colors">
                  Priya Sharma
                </h3>
                <div className="text-xs text-ink-secondary mt-0.5 font-medium">
                  1st Year Student, No Direction
                </div>
                <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                  Zero prior skills. Friendly guided exploration of what a tech career actually is.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 flex items-center justify-between text-xs font-semibold text-primary">
                <span>Start Discovery</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </div>
            </button>

            {/* Persona 3: Rohan Patel */}
            <button
              type="button"
              onClick={() => handleDemoLogin('rohan', 'Rohan Patel')}
              disabled={loading}
              className="p-4 bg-surface border border-border rounded-lg text-left hover:border-primary hover:shadow-soft transition-all group cursor-pointer disabled:opacity-60 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-8 h-8 rounded-md bg-status-info-tint flex items-center justify-center text-status-info">
                    <Briefcase className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-status-info bg-status-info-tint px-2 py-0.5 rounded">
                    Goal-Oriented
                  </span>
                </div>
                <h3 className="font-serif font-bold text-sm text-ink group-hover:text-primary transition-colors">
                  Rohan Patel
                </h3>
                <div className="text-xs text-ink-secondary mt-0.5 font-medium">
                  Self-Taught Full Stack Developer
                </div>
                <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                  Knows Python, SQL & basic HTML. Skips discovery straight to gap analysis & projects.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 flex items-center justify-between text-xs font-semibold text-primary">
                <span>View Gap Analysis</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </div>
            </button>

            {/* Persona 4: Ananya Verma */}
            <button
              type="button"
              onClick={() => handleDemoLogin('ananya', 'Ananya Verma')}
              disabled={loading}
              className="p-4 bg-surface border border-border rounded-lg text-left hover:border-primary hover:shadow-soft transition-all group cursor-pointer disabled:opacity-60 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-8 h-8 rounded-md bg-status-warning-tint flex items-center justify-center text-status-warning">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-status-warning bg-status-warning-tint px-2 py-0.5 rounded">
                    Career Switcher
                  </span>
                </div>
                <h3 className="font-serif font-bold text-sm text-ink group-hover:text-primary transition-colors">
                  Ananya Verma
                </h3>
                <div className="text-xs text-ink-secondary mt-0.5 font-medium">
                  Electronics to Software Engineer
                </div>
                <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                  Transitioning from hardware to software. Accelerated roadmap with portfolio milestones.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 flex items-center justify-between text-xs font-semibold text-primary">
                <span>Open Roadmap</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </div>
            </button>

            {/* Persona 5: Institutional Admin */}
            <button
              type="button"
              onClick={() => handleDemoLogin('admin', 'NIT Admin', '/admin')}
              disabled={loading}
              className="p-4 bg-surface border border-border rounded-lg text-left hover:border-accent hover:shadow-soft transition-all group cursor-pointer disabled:opacity-60 flex flex-col justify-between sm:col-span-2 lg:col-span-2"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-8 h-8 rounded-md bg-accent/20 flex items-center justify-center text-accent">
                    <Shield className="w-4 h-4" />
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-accent bg-accent/10 px-2 py-0.5 rounded">
                    Institutional Portal
                  </span>
                </div>
                <h3 className="font-serif font-bold text-sm text-ink group-hover:text-accent transition-colors">
                  College & Enterprise Admin Dashboard
                </h3>
                <div className="text-xs text-ink-secondary mt-0.5 font-medium">
                  National Institute of Technology (NIT) • Cohort Skill Analytics
                </div>
                <p className="text-xs text-ink-muted mt-2 leading-relaxed">
                  Monitor institutional skill gaps across student batches, track curriculum alignment, and view live learner cohorts.
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-border/60 flex items-center justify-between text-xs font-semibold text-accent">
                <span>Access Admin Analytics</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </div>
            </button>
          </div>
        </div>

        {/* Expandable Email/Password Sign-In */}
        <div className="bg-surface border border-border rounded-xl p-5 shadow-card">
          <button
            type="button"
            onClick={() => setShowEmailAuth(!showEmailAuth)}
            className="w-full flex items-center justify-between text-left text-xs font-semibold text-ink-secondary hover:text-ink cursor-pointer"
          >
            <span>Have an existing email account or prefer signing in with password?</span>
            <div className="flex items-center gap-1 text-primary">
              <span>{showEmailAuth ? 'Hide form' : 'Sign in / Register with email'}</span>
              {showEmailAuth ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </div>
          </button>

          {showEmailAuth && (
            <div className="mt-5 pt-4 border-t border-border">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-serif text-sm font-bold text-ink">
                  {isRegister ? 'Create New Account' : 'Sign In with Email'}
                </h3>
                <button
                  type="button"
                  onClick={() => {
                    setIsRegister(!isRegister);
                    setErrorMessage(null);
                  }}
                  className="text-xs font-semibold text-primary hover:underline"
                >
                  {isRegister ? 'Already registered? Sign In' : 'New student? Register'}
                </button>
              </div>

              <form onSubmit={handleEmailAuthSubmit} className="grid sm:grid-cols-2 gap-3">
                {isRegister && (
                  <div className="sm:col-span-2">
                    <label className="block text-xs font-medium text-ink-secondary mb-1">Full Name</label>
                    <div className="relative">
                      <UserIcon className="w-4 h-4 text-ink-muted absolute left-3 top-2.5" />
                      <input
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="e.g. Arif Mohamed"
                        className="w-full text-xs pl-9 pr-3 py-2 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                      />
                    </div>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-medium text-ink-secondary mb-1">Email Address</label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-ink-muted absolute left-3 top-2.5" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="e.g. learner@example.com"
                      required
                      className="w-full text-xs pl-9 pr-3 py-2 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-ink-secondary mb-1">Password</label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-ink-muted absolute left-3 top-2.5" />
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      required
                      className="w-full text-xs pl-9 pr-3 py-2 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                    />
                  </div>
                </div>

                <div className="sm:col-span-2 pt-2">
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-2.5 px-4 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover transition-colors shadow-soft flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
                  >
                    <span>{isRegister ? 'Create Account & Continue' : 'Sign In'}</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-8 text-center text-xs text-ink-muted">
        SkillPath © 2026 • Built for Students, Universities & Enterprise Cohorts • Light Theme Design System
      </footer>
    </div>
  );
};
