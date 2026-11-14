import React, { useState, useEffect } from 'react';
import {
  User,
  Mail,
  GraduationCap,
  Clock,
  Compass,
  FileText,
  UploadCloud,
  CheckCircle2,
  Sparkles,
  Save,
  Plus,
  Trash2,
  AlertCircle
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export const ProfilePage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { user, refreshUser } = useAuth();
  const { addToast } = useToast();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [education, setEducation] = useState('');
  const [branch, setBranch] = useState('');
  const [year, setYear] = useState<number | string>(3);
  const [institution, setInstitution] = useState('');
  const [weeklyHours, setWeeklyHours] = useState(10);
  const [careerGoal, setCareerGoal] = useState('');
  const [language, setLanguage] = useState('en');

  // Resume parser state
  const [resumeText, setResumeText] = useState('');
  const [isParsingResume, setIsParsingResume] = useState(false);
  const [parsedData, setParsedData] = useState<any>(null);

  // Saving state
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (user) {
      setName(user.profile?.full_name || user.full_name || '');
      setEmail(user.email || '');
      setEducation(user.profile?.education || 'B.Tech');
      setBranch(user.profile?.branch || '');
      setYear(user.profile?.year || 3);
      setInstitution(user.profile?.institution || '');
      setWeeklyHours(user.profile?.weekly_hours || 10);
      setCareerGoal(user.profile?.career_goal || user.career_goal || '');
      setLanguage(user.profile?.language || 'en');
    }
  }, [user]);

  const handleSaveProfile = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setIsSaving(true);
    try {
      await api.updateProfile({
        name,
        education,
        branch,
        year: Number(year),
        institution,
        weekly_hours: Number(weeklyHours),
        career_goal: careerGoal,
        language
      });
      await refreshUser();
      addToast('Profile updated successfully!', 'success');
    } catch (err: any) {
      addToast(err.message || 'Failed to update profile', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  const handleParseResume = async () => {
    if (!resumeText.trim()) {
      addToast('Please enter or paste your resume text first.', 'warning');
      return;
    }
    setIsParsingResume(true);
    try {
      const res = await api.parseResume(resumeText);
      setParsedData(res);
      addToast('Resume analyzed! Check the extracted skills below.', 'success');
    } catch (err: any) {
      addToast(err.message || 'Could not parse resume', 'error');
    } finally {
      setIsParsingResume(false);
    }
  };

  const handleApplyParsedData = async () => {
    if (!parsedData) return;
    setIsSaving(true);
    try {
      // Auto-update profile with parsed education/branch/skills if available
      const updates: any = {};
      if (parsedData.extracted_profile?.education) updates.education = parsedData.extracted_profile.education;
      if (parsedData.extracted_profile?.branch) {
        updates.branch = parsedData.extracted_profile.branch;
        setBranch(parsedData.extracted_profile.branch);
      }
      if (parsedData.recommended_goal && !careerGoal) {
        updates.career_goal = parsedData.recommended_goal;
        setCareerGoal(parsedData.recommended_goal);
      }
      await api.updateProfile(updates);
      await refreshUser();
      addToast('Extracted skills and details saved to your profile!', 'success');
      setParsedData(null);
    } catch (err: any) {
      addToast(err.message || 'Failed to save parsed details', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="font-serif text-2xl md:text-3xl font-bold text-ink">
          Learner Profile & Preferences
        </h1>
        <p className="text-sm text-ink-secondary mt-1">
          Your background, current studies, and available weekly study hours power your personalized roadmap.
        </p>
      </div>

      {/* Main Profile Form */}
      <form onSubmit={handleSaveProfile} className="bg-surface border border-border rounded-lg p-5 md:p-6 shadow-soft space-y-6">
        <div className="flex items-center gap-3 pb-4 border-b border-border/70">
          <div className="w-12 h-12 rounded-full bg-primary-tint text-primary flex items-center justify-center font-bold text-lg">
            {name ? name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div>
            <h2 className="font-semibold text-ink text-base">{name || 'Your Name'}</h2>
            <p className="text-xs text-ink-muted">{email}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">
              Full Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-bg border border-border rounded-md px-3 py-2 text-sm text-ink focus:outline-none focus:border-primary"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              disabled
              className="w-full bg-border/20 border border-border rounded-md px-3 py-2 text-sm text-ink-muted cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">
              Degree / Program
            </label>
            <input
              type="text"
              value={education}
              onChange={(e) => setEducation(e.target.value)}
              placeholder="e.g. B.Tech, B.Sc, BCA, High School"
              className="w-full bg-bg border border-border rounded-md px-3 py-2 text-sm text-ink focus:outline-none focus:border-primary"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">
              Branch / Major
            </label>
            <input
              type="text"
              value={branch}
              onChange={(e) => setBranch(e.target.value)}
              placeholder="e.g. Artificial Intelligence and Data Science"
              className="w-full bg-bg border border-border rounded-md px-3 py-2 text-sm text-ink focus:outline-none focus:border-primary"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">
              Current Year of Study
            </label>
            <select
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="w-full bg-bg border border-border rounded-md px-3 py-2 text-sm text-ink focus:outline-none focus:border-primary"
            >
              <option value={1}>1st Year (Exploring & Foundations)</option>
              <option value={2}>2nd Year (Core Skills)</option>
              <option value={3}>3rd Year (Projects & Internships)</option>
              <option value={4}>4th Year / Final Year (Job Placement)</option>
              <option value={5}>Graduated / Working Professional</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">
              College / University
            </label>
            <input
              type="text"
              value={institution}
              onChange={(e) => setInstitution(e.target.value)}
              placeholder="e.g. Anna University, IIT, BITS"
              className="w-full bg-bg border border-border rounded-md px-3 py-2 text-sm text-ink focus:outline-none focus:border-primary"
            />
          </div>
        </div>

        {/* Weekly Hours Slider */}
        <div className="pt-2">
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-semibold text-ink flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-primary" />
              Available Weekly Study Hours
            </label>
            <span className="text-sm font-bold text-primary px-2.5 py-0.5 rounded bg-primary-tint">
              {weeklyHours} hrs / week (~{Math.round((weeklyHours / 7) * 10) / 10}h daily)
            </span>
          </div>
          <input
            type="range"
            min={4}
            max={35}
            step={1}
            value={weeklyHours}
            onChange={(e) => setWeeklyHours(Number(e.target.value))}
            className="w-full accent-primary cursor-pointer"
          />
          <div className="flex justify-between text-[11px] text-ink-muted mt-1">
            <span>4 hrs (Casual)</span>
            <span>10 hrs (Standard student pace)</span>
            <span>20 hrs (Intensive)</span>
            <span>35 hrs (Full-time)</span>
          </div>
        </div>

        {/* Career Goal */}
        <div className="pt-2">
          <label className="block text-xs font-semibold text-ink mb-1.5">
            Primary Career Goal
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={careerGoal}
              onChange={(e) => setCareerGoal(e.target.value)}
              placeholder="e.g. AI/ML Engineer, Data Analyst, Full Stack Developer"
              className="flex-1 bg-bg border border-border rounded-md px-3 py-2 text-sm text-ink focus:outline-none focus:border-primary"
            />
            <button
              type="button"
              onClick={() => onNavigate('/discovery')}
              className="px-3 py-2 bg-accent-tint text-accent hover:bg-accent/20 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <Compass className="w-4 h-4" />
              <span>Discover</span>
            </button>
          </div>
          <p className="text-[11px] text-ink-muted mt-1">
            Changing this goal recalculates your roadmap, skill gaps, and flight simulator readiness date.
          </p>
        </div>

        {/* Preferred Language */}
        <div>
          <label className="block text-xs font-semibold text-ink mb-1.5">
            Preferred Language for AI Guidance & Explanations
          </label>
          <div className="grid grid-cols-3 gap-2">
            {[
              { code: 'en', label: 'English (Default)' },
              { code: 'hi', label: 'Hindi (हिंदी)' },
              { code: 'ta', label: 'Tamil (தமிழ்)' }
            ].map((lang) => (
              <button
                key={lang.code}
                type="button"
                onClick={() => setLanguage(lang.code)}
                className={`py-2 px-3 rounded-md text-xs font-medium border text-center transition-colors ${
                  language === lang.code
                    ? 'border-primary bg-primary-tint text-primary font-bold'
                    : 'border-border bg-bg text-ink-secondary hover:text-ink'
                }`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>

        {/* Save Button */}
        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="inline-flex items-center gap-2 bg-primary hover:bg-primary-hover disabled:opacity-50 text-white px-5 py-2.5 rounded-md font-semibold text-sm transition-colors shadow-sm"
          >
            <Save className="w-4 h-4" />
            <span>{isSaving ? 'Saving Changes...' : 'Save Profile Changes'}</span>
          </button>
        </div>
      </form>

      {/* AI Resume Analyzer Module */}
      <div className="bg-surface border border-border rounded-lg p-5 md:p-6 shadow-soft space-y-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-md bg-accent-tint text-accent">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-serif text-lg font-bold text-ink">
              AI Resume & Profile Importer
            </h2>
            <p className="text-xs text-ink-secondary">
              Paste your resume or bio text below. Our Profile Agent extracts skills, education, and projects automatically.
            </p>
          </div>
        </div>

        <div>
          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            rows={5}
            placeholder="Paste your resume contents, LinkedIn 'About' summary, or list of coursework and projects here..."
            className="w-full bg-bg border border-border rounded-md p-3 text-xs md:text-sm text-ink focus:outline-none focus:border-primary font-mono placeholder:font-sans"
          />
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3">
          <button
            type="button"
            onClick={() => {
              setResumeText(
                "Arif Mohamed\nB.Tech Artificial Intelligence and Data Science - 3rd Year\nCourses: Python Programming, Data Structures, Basic Probability & Statistics, SQL Basics.\nProjects: Built a simple Python script for web scraping student marks.\nInterests: Machine learning, pattern analysis, automating workflows."
              );
            }}
            className="text-xs text-primary hover:underline font-medium"
          >
            Fill sample resume (Arif)
          </button>

          <button
            type="button"
            onClick={handleParseResume}
            disabled={isParsingResume || !resumeText.trim()}
            className="inline-flex items-center gap-2 bg-ink hover:bg-ink/90 disabled:opacity-50 text-white px-4 py-2 rounded-md text-xs font-semibold transition-colors"
          >
            <Sparkles className="w-4 h-4 text-accent" />
            <span>{isParsingResume ? 'Analyzing Resume...' : 'Analyze with AI Agent'}</span>
          </button>
        </div>

        {/* Parsed Output Display */}
        {parsedData && (
          <div className="mt-4 p-4 rounded-lg bg-bg border border-border space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-ink flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-status-success" />
              Extraction Results
            </h3>

            {parsedData.extracted_skills && parsedData.extracted_skills.length > 0 && (
              <div>
                <span className="text-xs font-medium text-ink-muted">Detected Skills:</span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {parsedData.extracted_skills.map((sk: any, idx: number) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-full text-xs font-medium bg-primary-tint text-primary"
                    >
                      {sk.name || sk} {sk.level ? `(L${sk.level})` : ''}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {parsedData.recommended_goal && (
              <p className="text-xs text-ink">
                <span className="font-semibold">Recommended Career Fit:</span> {parsedData.recommended_goal}
              </p>
            )}

            <div className="pt-2 flex justify-end">
              <button
                type="button"
                onClick={handleApplyParsedData}
                disabled={isSaving}
                className="bg-primary hover:bg-primary-hover text-white px-4 py-1.5 rounded-md text-xs font-semibold transition-colors"
              >
                Apply & Save Extracted Details
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
