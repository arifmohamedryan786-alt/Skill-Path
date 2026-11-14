import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer
} from 'recharts';
import { BarChart3, TrendingUp, AlertCircle, CheckCircle2, ArrowRight } from 'lucide-react';
import { GlossaryTooltip } from '../components/common/GlossaryTooltip';

export const SkillAnalysisPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [analysis, setAnalysis] = useState<any | null>(null);
  const [matchData, setMatchData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [anData, mData] = await Promise.all([
          api.getSkillAnalysis(),
          api.getMatch()
        ]);
        setAnalysis(anData);
        setMatchData(mData);
      } catch (err: any) {
        showToast(err.message || 'Failed to load skill analysis', 'error');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Analyzing skill competencies...</div>;
  }

  const radarData = analysis?.radar_chart || [
    { subject: 'Programming', current: 40, target: 80 },
    { subject: 'Data', current: 30, target: 80 },
    { subject: 'AI', current: 20, target: 80 },
    { subject: 'Web', current: 15, target: 80 },
    { subject: 'Cloud', current: 10, target: 80 },
    { subject: 'Testing', current: 25, target: 80 },
    { subject: 'Design', current: 20, target: 80 },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <BarChart3 className="w-5 h-5 text-primary" />
            <h1 className="font-serif text-2xl font-bold text-ink">Skill Gap Analysis</h1>
          </div>
          <p className="text-xs text-ink-secondary">
            Evaluating your current competencies against target role requirements: <b>{matchData?.career_name || 'AI/ML Engineer'}</b>.
          </p>
        </div>

        <div className="flex items-center gap-3 bg-bg px-4 py-2 border border-border rounded-md">
          <div className="text-right">
            <div className="text-[11px] text-ink-muted">Overall Match</div>
            <div className="text-lg font-serif font-bold text-primary">{matchData?.match_pct || 0}%</div>
          </div>
          <div className="text-right pl-3 border-l border-border">
            <div className="text-[11px] text-ink-muted">Readiness Tier</div>
            <div className="text-xs font-semibold text-ink">{matchData?.readiness_label || 'Beginning'}</div>
          </div>
        </div>
      </div>

      {/* Top Section: Radar Chart + Key Strengths */}
      <div className="grid lg:grid-cols-12 gap-6">
        {/* Radar Chart */}
        <div className="lg:col-span-6 bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col items-center">
          <div className="w-full flex items-center justify-between mb-4">
            <h3 className="font-serif text-base font-bold text-ink">Competency Domain Radar</h3>
            <div className="flex items-center gap-4 text-xs font-medium">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-primary" />
                <span>Your Level</span>
              </div>
              <div className="flex items-center gap-1.5 text-ink-muted">
                <span className="w-2.5 h-2.5 rounded-full bg-border" />
                <span>Job Target</span>
              </div>
            </div>
          </div>

          <div className="w-full h-72">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#E3E1DA" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#5E6B69', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#8A9694', fontSize: 10 }} />
                <Radar
                  name="Target"
                  dataKey="target"
                  stroke="#E3E1DA"
                  fill="#E3E1DA"
                  fillOpacity={0.2}
                />
                <Radar
                  name="Current"
                  dataKey="current"
                  stroke="#0F6E68"
                  fill="#0F6E68"
                  fillOpacity={0.4}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Strengths & Immediate Blindspots */}
        <div className="lg:col-span-6 space-y-6">
          {/* Strengths */}
          <div className="bg-surface border border-border rounded-lg p-6 shadow-card">
            <h3 className="font-serif text-base font-bold text-ink mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-status-success" />
              <span>Proven Strengths</span>
            </h3>
            <div className="space-y-2.5">
              {analysis?.strengths?.length > 0 ? (
                analysis.strengths.slice(0, 4).map((s: any) => (
                  <div key={s.skill_id} className="p-3 bg-status-success-tint/40 border border-status-success/20 rounded-md flex items-center justify-between text-xs">
                    <div>
                      <div className="font-semibold text-ink">
                        <GlossaryTooltip term={s.name}>{s.name}</GlossaryTooltip>
                      </div>
                      <div className="text-[11px] text-ink-secondary capitalize">Category: {s.category}</div>
                    </div>
                    <span className="px-2 py-0.5 rounded bg-status-success text-white font-bold text-[10px]">
                      Level {s.level}
                    </span>
                  </div>
                ))
              ) : (
                <div className="p-4 bg-bg rounded text-xs text-ink-muted text-center">
                  Take your first checkpoint test in Python or Git to register your proven strengths!
                </div>
              )}
            </div>
          </div>

          {/* Critical Gaps for Career */}
          <div className="bg-surface border border-border rounded-lg p-6 shadow-card">
            <h3 className="font-serif text-base font-bold text-ink mb-3 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-status-warning" />
              <span>Priority Gap Skills to Bridge</span>
            </h3>
            <div className="space-y-2.5">
              {matchData?.gaps?.slice(0, 4).map((g: any) => (
                <div key={g.skill_id} className="p-3 bg-bg border border-border rounded-md flex items-center justify-between text-xs">
                  <div>
                    <div className="font-semibold text-ink">
                      <GlossaryTooltip term={g.name}>{g.name}</GlossaryTooltip>
                    </div>
                    <div className="text-[11px] text-ink-muted">Weight: Priority {g.weight}/5</div>
                  </div>
                  <div className="text-right">
                    <span className="text-[11px] text-status-danger font-semibold">
                      Gap: +{g.gap} level{g.gap > 1 ? 's' : ''}
                    </span>
                    <div className="text-[10px] text-ink-muted">Target: Level {g.target_level}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section: Horizontal Level Bars (Current vs Required Marker) */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card space-y-4">
        <div>
          <h3 className="font-serif text-lg font-bold text-ink">
            Skill Competency Bars (Current vs Target Requirement)
          </h3>
          <p className="text-xs text-ink-secondary">
            Horizontal levels: 0 (None) → 1 (Basic) → 2 (Working) → 3 (Proficient) → 4 (Advanced).
          </p>
        </div>

        <div className="grid sm:grid-cols-2 gap-4 pt-2">
          {matchData?.gaps?.map((g: any) => {
            const currentPct = (g.current_level / 4) * 100;
            const targetPct = (g.target_level / 4) * 100;

            return (
              <div key={g.skill_id} className="p-3.5 border border-border rounded-md bg-bg/30 space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-ink">
                    <GlossaryTooltip term={g.name}>{g.name}</GlossaryTooltip>
                  </span>
                  <span className="text-[11px] text-ink-muted">
                    Lvl {g.current_level} / Lvl {g.target_level}
                  </span>
                </div>

                {/* Progress bar with target marker */}
                <div className="relative h-2.5 bg-border rounded-full overflow-hidden">
                  <div
                    className="h-full bg-primary rounded-full transition-all duration-300"
                    style={{ width: `${currentPct}%` }}
                  />
                  {/* Target line */}
                  <div
                    className="absolute top-0 bottom-0 w-1 bg-accent shadow"
                    style={{ left: `calc(${targetPct}% - 2px)` }}
                    title={`Target: Level ${g.target_level}`}
                  />
                </div>

                <div className="flex items-center justify-between text-[10px] text-ink-muted pt-0.5">
                  <span>Current: Level {g.current_level}</span>
                  <span className="text-accent-hover font-semibold">Target: Level {g.target_level}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

