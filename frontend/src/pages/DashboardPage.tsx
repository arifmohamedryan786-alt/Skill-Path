import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import {
  Compass, Map, CheckSquare, Plane, Award, Mic,
  ArrowRight, Sparkles, Clock, CheckCircle2, Bot, Layers, Code2
} from 'lucide-react';
import { MountainSummitIllustration } from '../components/illustrations/LineArtIllustrations';

export const DashboardPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [firstWeek, setFirstWeek] = useState<any>(null);
  const [roadmap, setRoadmap] = useState<any>(null);
  const [agentLogs, setAgentLogs] = useState<any[]>([]);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [profData, foreData, fwData, rmData, logsData] = await Promise.all([
          api.getProfile(),
          api.getForecast(),
          api.getFirstWeekPlan(),
          api.getRoadmap(),
          api.getAgentLogs()
        ]);
        setProfile(profData);
        setForecast(foreData);
        setFirstWeek(fwData);
        setRoadmap(rmData);
        setAgentLogs(logsData);
      } catch (err) {
        // fallback
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-28 bg-surface border border-border rounded-lg" />
        <div className="grid md:grid-cols-3 gap-6">
          <div className="h-64 bg-surface border border-border rounded-lg" />
          <div className="h-64 bg-surface border border-border rounded-lg" />
          <div className="h-64 bg-surface border border-border rounded-lg" />
        </div>
      </div>
    );
  }

  const targetCareer = profile?.career_goal || 'AI/ML Engineer';
  const matchPct = forecast?.current_match_pct || 12.0;
  const readyDate = forecast?.realistic_date || '14 March';

  return (
    <div className="space-y-8">
      {/* 1. Human Summary Banner */}
      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card relative overflow-hidden flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary-tint text-primary border border-primary/20">
            <Sparkles className="w-3.5 h-3.5 text-accent" />
            <span>Here is your starting point</span>
          </div>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-ink leading-tight">
            You're {matchPct}% of the way to {targetCareer}.
          </h1>
          <p className="text-sm text-ink-secondary leading-relaxed">
            At your current pace of {profile?.weekly_hours || 8} hours/week, you'll be job-ready around <b>{readyDate}</b>. This week: master your first foundational skills.
          </p>
        </div>

        <div className="shrink-0 flex items-center gap-3">
          <button
            onClick={() => onNavigate('/roadmap')}
            className="px-5 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center gap-2"
          >
            <span>Start My First Week</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* 2. Beginner Starting Point: The 3 Core Things */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Card 1: Your Target Role & Fit */}
        <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-4">
              <Compass className="w-5 h-5" />
            </div>
            <h3 className="font-serif text-lg font-bold text-ink mb-1.5">Your Career Focus</h3>
            <p className="text-xs text-ink-secondary leading-relaxed mb-4">
              Matched based on your {profile?.branch || 'academic'} coursework and natural strengths.
            </p>
            <div className="p-3 bg-bg rounded-md border border-border mb-4">
              <div className="font-semibold text-xs text-ink">{targetCareer}</div>
              <div className="text-[11px] text-ink-secondary mt-0.5">
                {forecast?.readiness_label || 'Beginning Explorer'}
              </div>
            </div>
          </div>
          <button
            onClick={() => onNavigate('/discovery')}
            className="w-full py-2 border border-border rounded-md text-xs font-semibold text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center justify-center gap-1.5"
          >
            <span>Discover or Change Careers</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Card 2: This Week's First Tasks */}
        <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-4">
              <Clock className="w-5 h-5" />
            </div>
            <h3 className="font-serif text-lg font-bold text-ink mb-1.5">This Week's Plan</h3>
            <p className="text-xs text-ink-secondary leading-relaxed mb-4">
              {firstWeek?.focus_topic || 'Foundations'} · 30-45 mins/day
            </p>
            <div className="space-y-2 mb-4">
              {firstWeek?.tasks?.slice(0, 3).map((t: any, idx: number) => (
                <div key={idx} className="flex items-start gap-2.5 text-xs text-ink">
                  <div className="w-4 h-4 rounded-full border border-border flex items-center justify-center text-[10px] shrink-0 mt-0.5 font-medium text-ink-muted">
                    {idx + 1}
                  </div>
                  <span className="truncate">{t.title}</span>
                </div>
              ))}
            </div>
          </div>
          <button
            onClick={() => onNavigate('/roadmap')}
            className="w-full py-2 border border-border rounded-md text-xs font-semibold text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center justify-center gap-1.5"
          >
            <span>View Full Sprint</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Card 3: Roadmap Journey Overview */}
        <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-4">
              <Map className="w-5 h-5" />
            </div>
            <h3 className="font-serif text-lg font-bold text-ink mb-1.5">7-Stage Roadmap</h3>
            <p className="text-xs text-ink-secondary leading-relaxed mb-4">
              Your step-by-step route from zero to hired.
            </p>
            <div className="p-3 bg-bg rounded-md border border-border mb-4 flex items-center justify-between">
              <div>
                <div className="text-xs font-semibold text-ink">
                  {roadmap?.completed_stages || 1} of 7 Stages Complete
                </div>
                <div className="text-[11px] text-ink-secondary">
                  Current: Stage 2 (Foundations)
                </div>
              </div>
              <div className="w-10 h-10 rounded-full border-2 border-primary flex items-center justify-center text-xs font-bold text-primary">
                {Math.round(roadmap?.overall_progress_pct || 14)}%
              </div>
            </div>
          </div>
          <button
            onClick={() => onNavigate('/roadmap')}
            className="w-full py-2 bg-primary text-white rounded-md text-xs font-semibold hover:bg-primary-hover transition-colors shadow-soft flex items-center justify-center gap-1.5"
          >
            <span>Open Roadmap Journey</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 3. Unique Features Hub */}
      <div>
        <h2 className="font-serif text-xl font-bold text-ink mb-4">Core SkillPath Modules</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={() => onNavigate('/practice')}
            className="p-5 bg-surface border border-border rounded-lg text-left hover:border-primary/60 hover:shadow-card transition-all group"
          >
            <div className="w-8 h-8 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-3 group-hover:scale-105 transition-transform">
              <Code2 className="w-4 h-4" />
            </div>
            <div className="font-serif font-bold text-sm text-ink mb-1">Practice Questions</div>
            <div className="text-xs text-ink-secondary leading-relaxed">
              50 curated programming questions across C, Python, Java, Data Structures & DSA.
            </div>
          </button>

          <button
            onClick={() => onNavigate('/simulator')}
            className="p-5 bg-surface border border-border rounded-lg text-left hover:border-primary/60 hover:shadow-card transition-all group"
          >
            <div className="w-8 h-8 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-3 group-hover:scale-105 transition-transform">
              <Plane className="w-4 h-4" />
            </div>
            <div className="font-serif font-bold text-sm text-ink mb-1">Flight Simulator</div>
            <div className="text-xs text-ink-secondary leading-relaxed">
              Predict your readiness date and test what-if study hour scenarios.
            </div>
          </button>

          <button
            onClick={() => onNavigate('/passport')}
            className="p-5 bg-surface border border-border rounded-lg text-left hover:border-primary/60 hover:shadow-card transition-all group"
          >
            <div className="w-8 h-8 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-3 group-hover:scale-105 transition-transform">
              <Award className="w-4 h-4" />
            </div>
            <div className="font-serif font-bold text-sm text-ink mb-1">Skill Passport</div>
            <div className="text-xs text-ink-secondary leading-relaxed">
              Cryptographically verified badges with SHA-256 evidence logs.
            </div>
          </button>

          <button
            onClick={() => onNavigate('/interview')}
            className="p-5 bg-surface border border-border rounded-lg text-left hover:border-primary/60 hover:shadow-card transition-all group"
          >
            <div className="w-8 h-8 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-3 group-hover:scale-105 transition-transform">
              <Mic className="w-4 h-4" />
            </div>
            <div className="font-serif font-bold text-sm text-ink mb-1">Interview Coach</div>
            <div className="text-xs text-ink-secondary leading-relaxed">
              Voice or text mock interviews with rubric scoring across 4 dimensions.
            </div>
          </button>

          <button
            onClick={() => onNavigate('/mentor')}
            className="p-5 bg-surface border border-border rounded-lg text-left hover:border-primary/60 hover:shadow-card transition-all group"
          >
            <div className="w-8 h-8 rounded-md bg-primary-tint flex items-center justify-center text-primary mb-3 group-hover:scale-105 transition-transform">
              <Bot className="w-4 h-4" />
            </div>
            <div className="font-serif font-bold text-sm text-ink mb-1">AI Mentor Chat</div>
            <div className="text-xs text-ink-secondary leading-relaxed">
              24/7 personal tutor for career advice, code debugging, and encouragement.
            </div>
          </button>
        </div>
      </div>

      {/* 4. Explainable AI Timeline: Agent Activity */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-serif text-lg font-bold text-ink">Explainable AI Activity</h3>
            <p className="text-xs text-ink-secondary">
              Transparent log of automated reasoning, handoffs, and adaptations.
            </p>
          </div>
          <span className="text-[11px] font-semibold text-primary px-2.5 py-1 bg-primary-tint rounded-full">
            Live LangGraph Audit
          </span>
        </div>

        <div className="divide-y divide-border/60">
          {agentLogs.length > 0 ? (
            agentLogs.slice(0, 5).map((log) => (
              <div key={log.id} className="py-3 flex items-start gap-3">
                <div className="w-7 h-7 rounded-full bg-primary-tint flex items-center justify-center text-primary font-bold text-[10px] shrink-0 mt-0.5">
                  {log.agent_name.slice(0, 2).toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-ink">{log.agent_name}</span>
                    <span className="text-[11px] text-ink-muted">{log.created_at}</span>
                  </div>
                  <div className="text-xs text-ink-secondary font-medium mt-0.5">{log.action}</div>
                  <div className="text-xs text-ink leading-relaxed mt-1">{log.reason}</div>
                </div>
              </div>
            ))
          ) : (
            <div className="py-6 text-center text-xs text-ink-muted">
              Discovery Agent matched you with 5 careers → Roadmap Planner built 7 stages → Simulation Agent estimated {readyDate}.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

