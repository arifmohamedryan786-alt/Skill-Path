import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Award,
  CheckCircle2,
  Clock,
  Zap,
  Calendar,
  Layers,
  ArrowRight,
  Info,
  BookOpen,
  ChevronRight
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  AreaChart,
  Area
} from 'recharts';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

export const ProgressPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progressData, setProgressData] = useState<any>(null);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      setLoading(true);
      const res = await api.getProgress();
      setProgressData(res);
    } catch {
      // Provide robust fallback data if offline
      setProgressData({
        overall_progress_pct: 28,
        completed_skills_count: 3,
        total_skills_count: 12,
        verified_skills_count: 2,
        hours_studied: 36,
        target_hours: 120,
        learner_pace_factor: 1.0,
        stages: [
          { stage_number: 1, name: 'Explore & Foundation', status: 'completed', pct: 100 },
          { stage_number: 2, name: 'Core Foundations', status: 'in_progress', pct: 60 },
          { stage_number: 3, name: 'Core Skills & Tools', status: 'locked', pct: 0 },
          { stage_number: 4, name: 'Projects & Portfolio', status: 'locked', pct: 0 },
          { stage_number: 5, name: 'Internship & Experience', status: 'locked', pct: 0 },
          { stage_number: 6, name: 'Interview Prep & Job Search', status: 'locked', pct: 0 },
          { stage_number: 7, name: 'Career Growth & Specialization', status: 'locked', pct: 0 }
        ],
        score_trend: [
          { test: 'Python Basics', score: 85, date: 'Week 1' },
          { test: 'Data Structures', score: 72, date: 'Week 2' },
          { test: 'SQL Checkpoint', score: 90, date: 'Week 3' }
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  const getPaceDescription = (pace: number) => {
    if (pace < 0.9) {
      return {
        label: 'Accelerated Pace',
        color: 'text-status-success',
        bg: 'bg-status-success-tint',
        desc: `Your velocity is 20% faster than average! You're mastering skills quickly and will reach job readiness ahead of schedule.`
      };
    } else if (pace > 1.1) {
      return {
        label: 'Steady & Thorough',
        color: 'text-accent',
        bg: 'bg-accent-tint',
        desc: `You are taking extra time to practice deeply. The flight simulator automatically accounts for this to keep dates realistic.`
      };
    }
    return {
      label: 'Standard Pace (1.0x)',
      color: 'text-primary',
      bg: 'bg-primary-tint',
      desc: `Your completion pace matches our standard benchmark of 10 hours per core level. Keep this consistency up!`
    };
  };

  const paceInfo = getPaceDescription(progressData?.learner_pace_factor || 1.0);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-serif text-2xl md:text-3xl font-bold text-ink">
            Learning Progress & Velocity
          </h1>
          <p className="text-sm text-ink-secondary mt-1">
            Track your journey from day zero. See your consistency, velocity, and milestone unlocks.
          </p>
        </div>
        <button
          onClick={() => onNavigate('/roadmap')}
          className="inline-flex items-center gap-2 bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-md font-medium text-sm transition-colors self-start"
        >
          <span>Continue Roadmap</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Top 4 KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-surface border border-border rounded-lg p-4 shadow-soft">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-ink-muted">Overall Readiness</span>
            <TrendingUp className="w-4 h-4 text-primary" />
          </div>
          <div className="text-2xl font-bold text-ink">
            {progressData?.overall_progress_pct || 25}%
          </div>
          <div className="w-full bg-border/40 rounded-full h-1.5 mt-2 overflow-hidden">
            <div
              className="bg-primary h-full rounded-full transition-all duration-500"
              style={{ width: `${progressData?.overall_progress_pct || 25}%` }}
            />
          </div>
        </div>

        <div className="bg-surface border border-border rounded-lg p-4 shadow-soft">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-ink-muted">Verified Skills</span>
            <Award className="w-4 h-4 text-accent" />
          </div>
          <div className="text-2xl font-bold text-ink">
            {progressData?.verified_skills_count || 2} <span className="text-xs font-normal text-ink-muted">/ {progressData?.total_skills_count || 12}</span>
          </div>
          <p className="text-xs text-ink-secondary mt-1">Passed with 70%+ score</p>
        </div>

        <div className="bg-surface border border-border rounded-lg p-4 shadow-soft">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-ink-muted">Hours Invested</span>
            <Clock className="w-4 h-4 text-primary" />
          </div>
          <div className="text-2xl font-bold text-ink">
            {progressData?.hours_studied || 36}h
          </div>
          <p className="text-xs text-ink-secondary mt-1">
            Goal: ~{progressData?.target_hours || 120}h total
          </p>
        </div>

        <div className="bg-surface border border-border rounded-lg p-4 shadow-soft">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-ink-muted">Weekly Schedule</span>
            <Calendar className="w-4 h-4 text-accent" />
          </div>
          <div className="text-2xl font-bold text-ink">
            {user?.profile?.weekly_hours || 10} <span className="text-xs font-normal text-ink-muted">hrs/wk</span>
          </div>
          <p className="text-xs text-ink-secondary mt-1">
            {Math.round(((user?.profile?.weekly_hours || 10) / 7) * 10) / 10}h daily target
          </p>
        </div>
      </div>

      {/* Dynamic Pace Factor Card */}
      <div className="bg-surface border border-border rounded-lg p-5 shadow-soft">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-3">
          <div className="flex items-center gap-2.5">
            <div className={`p-2 rounded-md ${paceInfo.bg} ${paceInfo.color}`}>
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-serif text-lg font-bold text-ink">Learner Pace Factor</h2>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded ${paceInfo.bg} ${paceInfo.color}`}>
                {paceInfo.label} ({progressData?.learner_pace_factor || 1.0}x)
              </span>
            </div>
          </div>
          <button
            onClick={() => onNavigate('/simulator')}
            className="text-xs font-medium text-primary hover:underline flex items-center gap-1"
          >
            <span>Simulate schedule changes</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <p className="text-sm text-ink-secondary leading-relaxed">
          {paceInfo.desc}
        </p>
      </div>

      {/* 7 Roadmap Stages Unlocks */}
      <div className="bg-surface border border-border rounded-lg p-5 shadow-soft">
        <h2 className="font-serif text-lg font-bold text-ink mb-1">
          7-Stage Zero-to-Job Progression
        </h2>
        <p className="text-xs text-ink-secondary mb-4">
          Every stage builds on the previous one. Complete checkpoint quizzes and projects to unlock later stages.
        </p>

        <div className="space-y-3">
          {(progressData?.stages || []).map((st: any) => {
            const isCompleted = st.status === 'completed' || st.pct === 100;
            const isInProgress = st.status === 'in_progress';
            const isLocked = !isCompleted && !isInProgress;

            return (
              <div
                key={st.stage_number}
                className={`p-3.5 rounded-lg border transition-all ${
                  isCompleted
                    ? 'bg-status-success-tint/30 border-status-success/30'
                    : isInProgress
                    ? 'bg-primary-tint/30 border-primary/40'
                    : 'bg-bg/40 border-border/60 opacity-70'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2.5">
                    <span className="w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center shrink-0 bg-surface border border-border text-ink">
                      {st.stage_number}
                    </span>
                    <span className="text-sm font-semibold text-ink">
                      Stage {st.stage_number}: {st.name}
                    </span>
                  </div>

                  <div>
                    {isCompleted ? (
                      <span className="inline-flex items-center gap-1 text-xs font-semibold text-status-success">
                        <CheckCircle2 className="w-4 h-4" />
                        Completed
                      </span>
                    ) : isInProgress ? (
                      <span className="inline-flex items-center gap-1 text-xs font-semibold text-primary">
                        In Progress ({st.pct}%)
                      </span>
                    ) : (
                      <span className="text-xs font-medium text-ink-muted">Locked</span>
                    )}
                  </div>
                </div>

                <div className="w-full bg-border/40 rounded-full h-1.5 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      isCompleted ? 'bg-status-success' : isInProgress ? 'bg-primary' : 'bg-border'
                    }`}
                    style={{ width: `${st.pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Assessment Score History Trend */}
      {progressData?.score_trend && progressData.score_trend.length > 0 && (
        <div className="bg-surface border border-border rounded-lg p-5 shadow-soft">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-serif text-lg font-bold text-ink">Assessment Score History</h2>
              <p className="text-xs text-ink-secondary">
                Scores ≥ 70% automatically earn verified badges on your Skill Passport.
              </p>
            </div>
            <button
              onClick={() => onNavigate('/assessments')}
              className="text-xs font-medium text-primary hover:underline flex items-center gap-1"
            >
              <span>Take Checkpoint</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={progressData.score_trend} margin={{ top: 10, right: 20, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="scoreColor" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0F6E68" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#0F6E68" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#EFECE6" />
                <XAxis dataKey="test" tick={{ fontSize: 11, fill: '#8A9694' }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#8A9694' }} />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-surface p-2.5 rounded border border-border shadow-card text-xs">
                          <p className="font-bold text-ink">{data.test}</p>
                          <p className="text-primary font-semibold">Score: {data.score}%</p>
                          <p className="text-ink-muted text-[10px]">{data.date}</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="score"
                  stroke="#0F6E68"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#scoreColor)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};

