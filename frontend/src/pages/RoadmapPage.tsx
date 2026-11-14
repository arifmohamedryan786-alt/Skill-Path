import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import { RoadmapData, RoadmapStage, RoadmapItem, HowToLearnCard } from '../types';
import {
  Map, CheckCircle2, Lock, Play, X, ExternalLink,
  Clock, ArrowRight, BookOpen, AlertCircle, Award, Check
} from 'lucide-react';
import { GlossaryTooltip } from '../components/common/GlossaryTooltip';

export const RoadmapPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [roadmap, setRoadmap] = useState<RoadmapData | null>(null);
  const [activeTab, setActiveTab] = useState<'roadmap' | 'firstWeek'>('roadmap');
  const [firstWeek, setFirstWeek] = useState<any | null>(null);
  const [activeDrawerSkill, setActiveDrawerSkill] = useState<HowToLearnCard | null>(null);
  const [drawerLoading, setDrawerLoading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [rmData, fwData] = await Promise.all([
        api.getRoadmap(),
        api.getFirstWeekPlan()
      ]);
      setRoadmap(rmData);
      setFirstWeek(fwData);
    } catch (err: any) {
      showToast(err.message || 'Failed to load roadmap', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenHowToLearn = async (skillId: number | null | undefined) => {
    if (!skillId) return;
    setDrawerLoading(true);
    try {
      const card = await api.getHowToLearn(skillId);
      setActiveDrawerSkill(card);
    } catch (err: any) {
      showToast(err.message || 'Failed to load skill guide', 'error');
    } finally {
      setDrawerLoading(false);
    }
  };

  const handleToggleTask = async (itemId: number, currentStatus: string) => {
    const nextStatus = currentStatus === 'completed' ? 'pending' : 'completed';
    try {
      await api.updateItemStatus(itemId, nextStatus);
      showToast(`Task marked as ${nextStatus}`, 'success');
      // refresh roadmap data locally
      if (roadmap) {
        const updatedStages = roadmap.stages.map((stg) => ({
          ...stg,
          items: stg.items.map((it) => (it.id === itemId ? { ...it, status: nextStatus as any } : it))
        }));
        setRoadmap({ ...roadmap, stages: updatedStages });
      }
    } catch (err: any) {
      showToast(err.message || 'Failed to update task', 'error');
    }
  };

  const handleRegenerate = async () => {
    try {
      const updated = await api.regenerateRoadmap();
      setRoadmap(updated);
      showToast('Roadmap successfully adapted and rebuilt!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Failed to rebuild roadmap', 'error');
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Building your 7-stage roadmap...</div>;
  }

  return (
    <div className="space-y-8 relative">
      {/* Header */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Map className="w-5 h-5 text-primary" />
            <h1 className="font-serif text-2xl font-bold text-ink">
              {roadmap?.career_goal || 'Your'} Career Roadmap
            </h1>
          </div>
          <p className="text-xs text-ink-secondary">
            7 structured stages from zero to job-ready. Adjusted for Year {roadmap?.adjusted_for_year || 3} student timeline.
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <div className="flex p-0.5 bg-bg border border-border rounded-md text-xs">
            <button
              onClick={() => setActiveTab('roadmap')}
              className={`px-3 py-1.5 rounded text-xs font-semibold transition-colors ${
                activeTab === 'roadmap' ? 'bg-surface text-primary shadow-soft' : 'text-ink-secondary hover:text-ink'
              }`}
            >
              7-Stage Journey
            </button>
            <button
              onClick={() => setActiveTab('firstWeek')}
              className={`px-3 py-1.5 rounded text-xs font-semibold transition-colors ${
                activeTab === 'firstWeek' ? 'bg-surface text-primary shadow-soft' : 'text-ink-secondary hover:text-ink'
              }`}
            >
              Your First Week
            </button>
          </div>

          <button
            onClick={handleRegenerate}
            className="px-3 py-1.5 border border-border text-xs rounded-md text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
          >
            Rebuild
          </button>
        </div>
      </div>

      {/* VIEW 1: 7-Stage Journey Map */}
      {activeTab === 'roadmap' && (
        <div className="space-y-6">
          {roadmap?.stages.map((stage) => {
            const isCompleted = stage.status === 'completed';
            const isCurrent = stage.status === 'current';
            const isLocked = stage.status === 'locked';

            return (
              <div
                key={stage.id}
                className={`bg-surface border rounded-lg p-6 shadow-card transition-all ${
                  isCurrent
                    ? 'border-primary ring-1 ring-primary/40'
                    : isCompleted
                    ? 'border-status-success/30'
                    : 'border-border opacity-85'
                }`}
              >
                {/* Stage Header */}
                <div className="flex items-start justify-between gap-4 pb-4 border-b border-border/60">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-sm shrink-0 ${
                        isCompleted
                          ? 'bg-status-success text-white'
                          : isCurrent
                          ? 'bg-primary text-white shadow-soft ring-4 ring-primary-tint'
                          : 'bg-bg border border-border text-ink-muted'
                      }`}
                    >
                      {isCompleted ? <CheckCircle2 className="w-5 h-5" /> : stage.stage_number}
                    </div>

                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-serif text-lg font-bold text-ink">{stage.title}</h3>
                        <span
                          className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                            isCompleted
                              ? 'bg-status-success/10 text-status-success'
                              : isCurrent
                              ? 'bg-primary-tint text-primary'
                              : 'bg-bg text-ink-muted border border-border'
                          }`}
                        >
                          {stage.status}
                        </span>
                      </div>
                      <p className="text-xs text-ink-secondary mt-0.5">{stage.description}</p>
                    </div>
                  </div>

                  <div className="text-[11px] font-semibold text-ink-muted shrink-0 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    <span>~{stage.est_weeks} weeks</span>
                  </div>
                </div>

                {/* Items in Stage */}
                <div className="mt-4 space-y-2.5">
                  {stage.items.map((item) => {
                    const itemDone = item.status === 'completed';
                    const itemInProgress = item.status === 'in_progress';

                    return (
                      <div
                        key={item.id}
                        className={`p-3.5 rounded-md border flex flex-col sm:flex-row sm:items-center justify-between gap-3 transition-colors ${
                          itemDone
                            ? 'bg-bg/40 border-border/60'
                            : itemInProgress
                            ? 'bg-primary-tint/20 border-primary/40'
                            : 'bg-surface border-border hover:border-primary/30'
                        }`}
                      >
                        <div className="flex items-start gap-3 flex-1 min-w-0">
                          <button
                            type="button"
                            onClick={() => handleToggleTask(item.id, item.status)}
                            className={`w-5 h-5 rounded border mt-0.5 flex items-center justify-center shrink-0 transition-colors ${
                              itemDone
                                ? 'bg-status-success border-status-success text-white'
                                : 'border-border hover:border-primary bg-surface'
                            }`}
                          >
                            {itemDone && <Check className="w-3.5 h-3.5 stroke-[3]" />}
                          </button>

                          <div className="min-w-0">
                            <div className="flex items-center gap-2">
                              <span className={`text-xs font-semibold ${itemDone ? 'line-through text-ink-muted' : 'text-ink'}`}>
                                <GlossaryTooltip term={item.title}>{item.title}</GlossaryTooltip>
                              </span>
                              <span className="text-[10px] px-1.5 py-0.2 rounded bg-bg text-ink-muted border border-border capitalize">
                                {item.item_type}
                              </span>
                            </div>
                            <p className="text-[11px] text-ink-secondary leading-relaxed mt-0.5 line-clamp-1">
                              {item.description}
                            </p>
                          </div>
                        </div>

                        {/* Action buttons on task */}
                        <div className="flex items-center gap-2 shrink-0 self-end sm:self-center">
                          {item.skill_id && (
                            <button
                              onClick={() => handleOpenHowToLearn(item.skill_id)}
                              className="px-2.5 py-1 text-[11px] font-semibold text-primary bg-primary-tint hover:bg-primary-light rounded transition-colors flex items-center gap-1"
                            >
                              <BookOpen className="w-3 h-3" />
                              <span>How to learn</span>
                            </button>
                          )}

                          {item.skill_id && (
                            <button
                              onClick={() => onNavigate(`/assessments`)}
                              className="px-2.5 py-1 text-[11px] font-semibold text-ink-secondary hover:text-ink border border-border rounded hover:bg-bg transition-colors"
                            >
                              Quiz
                            </button>
                          )}

                          <span className="text-[10px] text-ink-muted">
                            Week {item.due_week}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* VIEW 2: Your First Week Day-by-Day Plan */}
      {activeTab === 'firstWeek' && firstWeek && (
        <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card space-y-6">
          <div className="pb-4 border-b border-border">
            <span className="text-xs font-bold uppercase tracking-wider text-primary">Day-by-Day Sprint</span>
            <h2 className="font-serif text-2xl font-bold text-ink mt-0.5">
              Your First 7 Days: {firstWeek.focus_topic}
            </h2>
            <p className="text-xs text-ink-secondary mt-1">{firstWeek.why_it_matters}</p>
          </div>

          <div className="space-y-3">
            {firstWeek.tasks?.map((t: any, idx: number) => (
              <div
                key={idx}
                className="p-4 rounded-md border border-border bg-bg/40 flex items-start justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-primary px-2 py-0.5 bg-primary-tint rounded">
                      {t.day}
                    </span>
                    <span className="font-semibold text-xs text-ink">{t.title}</span>
                    <span className="text-[11px] text-ink-muted">({t.duration_mins} mins)</span>
                  </div>
                  <p className="text-xs text-ink-secondary leading-relaxed pl-1">
                    {t.description}
                  </p>
                </div>

                {t.action_url && (
                  <a
                    href={t.action_url}
                    target="_blank"
                    rel="noreferrer"
                    className="shrink-0 p-2 text-xs font-semibold text-primary hover:underline flex items-center gap-1"
                  >
                    <span>Start</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* "HOW TO LEARN THIS" DRAWER */}
      {activeDrawerSkill && (
        <div className="fixed inset-0 z-50 flex justify-end bg-ink/30 backdrop-blur-xs animate-in fade-in duration-150">
          <div className="w-full max-w-xl bg-surface h-full flex flex-col shadow-drawer border-l border-border p-6 sm:p-8 overflow-y-auto animate-in slide-in-from-right duration-200">
            {/* Drawer Header */}
            <div className="flex items-start justify-between pb-4 border-b border-border">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-primary">How to learn this</span>
                <h2 className="font-serif text-2xl font-bold text-ink mt-0.5">{activeDrawerSkill.name}</h2>
                <div className="text-xs text-ink-secondary mt-1">
                  Estimated ~{activeDrawerSkill.estimated_hours} hours total ({activeDrawerSkill.estimated_weeks} weeks at {activeDrawerSkill.weekly_hours_assumed}h/wk)
                </div>
              </div>
              <button
                onClick={() => setActiveDrawerSkill(null)}
                className="p-1 rounded-md text-ink-muted hover:text-ink hover:bg-bg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-6 py-6 text-xs text-ink">
              {/* Plain Language Explanation */}
              <div className="p-4 rounded-md bg-bg border border-border">
                <div className="font-bold text-ink mb-1">What it is in plain language:</div>
                <p className="text-ink-secondary leading-relaxed">{activeDrawerSkill.plain_explanation}</p>
                <div className="mt-2 pt-2 border-t border-border/60 text-primary font-medium">
                  {activeDrawerSkill.why_it_matters}
                </div>
              </div>

              {/* Study Method (Watch vs Practice vs Build) */}
              <div>
                <div className="font-bold text-ink mb-2">Recommended Study Method:</div>
                <div className="h-3 rounded-full bg-border overflow-hidden flex mb-2">
                  <div
                    style={{ width: `${activeDrawerSkill.learning_method?.watch_pct || 25}%` }}
                    className="bg-accent"
                    title="Watch Theory"
                  />
                  <div
                    style={{ width: `${activeDrawerSkill.learning_method?.practice_pct || 55}%` }}
                    className="bg-primary"
                    title="Code Practice"
                  />
                  <div
                    style={{ width: `${activeDrawerSkill.learning_method?.build_pct || 20}%` }}
                    className="bg-status-success"
                    title="Build Project"
                  />
                </div>
                <div className="flex justify-between text-[11px] text-ink-secondary">
                  <span>{activeDrawerSkill.learning_method?.watch_pct || 25}% Watch</span>
                  <span>{activeDrawerSkill.learning_method?.practice_pct || 55}% Code Practice</span>
                  <span>{activeDrawerSkill.learning_method?.build_pct || 20}% Build Projects</span>
                </div>
                <p className="text-[11px] text-ink-muted italic mt-1.5">
                  💡 Tip: {activeDrawerSkill.learning_method?.tip}
                </p>
              </div>

              {/* Recommended First Step */}
              <div className="p-3.5 bg-primary-tint/30 border border-primary/20 rounded-md">
                <div className="font-bold text-primary mb-1">Recommended First Step:</div>
                <div className="text-ink">{activeDrawerSkill.recommended_first_step}</div>
              </div>

              {/* Curated Resources in Order */}
              <div>
                <div className="font-bold text-ink mb-2">Curated Reputable Resources (In Order):</div>
                <div className="space-y-2">
                  {activeDrawerSkill.resources.map((res) => (
                    <a
                      key={res.id}
                      href={res.url}
                      target="_blank"
                      rel="noreferrer"
                      className="p-3 rounded-md border border-border bg-surface hover:border-primary transition-colors flex items-center justify-between gap-3 group block"
                    >
                      <div>
                        <div className="font-semibold text-ink group-hover:text-primary transition-colors">
                          {res.title}
                        </div>
                        <div className="text-[11px] text-ink-muted flex items-center gap-2 mt-0.5">
                          <span>{res.provider}</span>
                          <span>•</span>
                          <span>{res.duration}</span>
                          <span>•</span>
                          <span className="capitalize">{res.type}</span>
                          {res.free && <span className="text-status-success font-semibold">FREE</span>}
                        </div>
                      </div>
                      <ExternalLink className="w-4 h-4 text-ink-muted group-hover:text-primary shrink-0" />
                    </a>
                  ))}
                </div>
              </div>

              {/* Common Mistakes */}
              {activeDrawerSkill.common_mistakes.length > 0 && (
                <div>
                  <div className="font-bold text-ink mb-2 flex items-center gap-1.5 text-status-danger">
                    <AlertCircle className="w-3.5 h-3.5" />
                    <span>Common Beginner Mistakes to Avoid:</span>
                  </div>
                  <ul className="space-y-1 text-ink-secondary pl-3">
                    {activeDrawerSkill.common_mistakes.map((m, idx) => (
                      <li key={idx}>• {m}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Done Criteria */}
              {activeDrawerSkill.done_criteria.length > 0 && (
                <div>
                  <div className="font-bold text-ink mb-2 text-status-success flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>How to Know You've Learned It (Done Criteria):</span>
                  </div>
                  <ul className="space-y-1 text-ink-secondary pl-3">
                    {activeDrawerSkill.done_criteria.map((c, idx) => (
                      <li key={idx}>✓ {c}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Checkpoint CTA */}
              <div className="pt-4 border-t border-border">
                <button
                  onClick={() => {
                    setActiveDrawerSkill(null);
                    onNavigate('/assessments');
                  }}
                  className="w-full py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center justify-center gap-2"
                >
                  <Award className="w-4 h-4" />
                  <span>Take Checkpoint Test to Earn Verified Badge</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

