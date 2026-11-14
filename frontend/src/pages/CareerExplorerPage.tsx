import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import { CareerDetail } from '../types';
import {
  Layers, Code, Star, CheckCircle, ArrowRight, X,
  Clock, Check, Sparkles, HelpCircle, Columns
} from 'lucide-react';
import { GlossaryTooltip } from '../components/common/GlossaryTooltip';

export const CareerExplorerPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [careers, setCareers] = useState<any[]>([]);
  const [selectedCareer, setSelectedCareer] = useState<CareerDetail | null>(null);
  const [compareList, setCompareList] = useState<number[]>([]);
  const [compareData, setCompareData] = useState<any | null>(null);
  const [tryItData, setTryItData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCareers() {
      try {
        const list = await api.getCareers();
        setCareers(list);
        if (list.length > 0) {
          const detail = await api.getCareerDetails(list[0].id);
          setSelectedCareer(detail);
        }
      } catch (err) {
        // fallback
      } finally {
        setLoading(false);
      }
    }
    loadCareers();
  }, []);

  const handleSelectCareer = async (id: number) => {
    try {
      const detail = await api.getCareerDetails(id);
      setSelectedCareer(detail);
      setTryItData(null);
    } catch (err) {
      // ignore
    }
  };

  const handleToggleCompare = (id: number) => {
    if (compareList.includes(id)) {
      setCompareList(compareList.filter((x) => x !== id));
    } else {
      if (compareList.length >= 3) {
        showToast('You can compare at most 3 careers side by side', 'warning');
        return;
      }
      setCompareList([...compareList, id]);
    }
  };

  const handleRunCompare = async () => {
    if (compareList.length < 2) {
      showToast('Please select at least 2 careers to compare', 'warning');
      return;
    }
    try {
      const res = await api.compareCareers(compareList);
      setCompareData(res);
    } catch (err: any) {
      showToast(err.message || 'Comparison failed', 'error');
    }
  };

  const handleLoadTryIt = async (id: number) => {
    try {
      const task = await api.getTryItTask(id);
      setTryItData(task);
    } catch (err: any) {
      showToast(err.message || 'Failed to load mini project', 'error');
    }
  };

  const handleCommitCareer = async (careerName: string) => {
    try {
      await api.updateProfile({ career_goal: careerName, goal_status: 'known' });
      showToast(`Committed to ${careerName}! Roadmap adapted.`, 'success');
      onNavigate('/roadmap');
    } catch (err: any) {
      showToast(err.message || 'Failed to set career', 'error');
    }
  };

  const handleShortlist = async (careerId: number) => {
    try {
      await api.addToShortlist(careerId, false, 'Saved from explorer');
      showToast('Added to your shortlisted careers!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Failed to shortlist', 'error');
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Loading careers directory...</div>;
  }

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Layers className="w-5 h-5 text-primary" />
            <h1 className="font-serif text-2xl font-bold text-ink">Career Explorer</h1>
          </div>
          <p className="text-xs text-ink-secondary">
            Explore 13 curated industry careers. See real days in the life, typical tasks, salary notes, and test 1-hour mini projects.
          </p>
        </div>

        {compareList.length > 0 && (
          <div className="flex items-center gap-2 bg-primary-tint/50 border border-primary/20 px-3 py-1.5 rounded-md text-xs">
            <span className="font-semibold text-primary">{compareList.length} selected</span>
            <button
              onClick={handleRunCompare}
              className="px-2.5 py-1 bg-primary text-white rounded text-[11px] font-semibold hover:bg-primary-hover transition-colors"
            >
              Compare Side-by-Side
            </button>
            <button
              onClick={() => setCompareList([])}
              className="text-ink-muted hover:text-ink text-[11px]"
            >
              Clear
            </button>
          </div>
        )}
      </div>

      {/* Side-by-Side Comparison Modal */}
      {compareData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-xs animate-in fade-in duration-150">
          <div className="bg-surface border border-border rounded-lg max-w-5xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-drawer">
            <div className="flex items-center justify-between pb-4 border-b border-border mb-6">
              <h2 className="font-serif text-xl font-bold text-ink flex items-center gap-2">
                <Columns className="w-5 h-5 text-primary" />
                <span>Side-by-Side Career Comparison</span>
              </h2>
              <button
                onClick={() => setCompareData(null)}
                className="p-1 rounded-md text-ink-muted hover:text-ink hover:bg-bg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {compareData.careers.map((c: any) => (
                <div key={c.id} className="border border-border rounded-md p-5 bg-bg/50 flex flex-col justify-between">
                  <div className="space-y-3">
                    <div className="font-serif font-bold text-lg text-ink">{c.name}</div>
                    <div className="text-xs text-status-success font-semibold px-2 py-0.5 bg-status-success/10 rounded w-fit">
                      {c.demand_level} Demand
                    </div>
                    <p className="text-xs text-ink-secondary">{c.plain_description}</p>
                    <div className="text-[11px] text-ink-muted border-t border-border pt-2">
                      <b>Salary Note:</b> {c.salary_range_note}
                    </div>

                    <div className="text-xs">
                      <b>Required Skills:</b>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {c.skills.slice(0, 6).map((sk: any) => (
                          <span key={sk.skill_id} className="text-[10px] px-2 py-0.5 rounded bg-surface border border-border">
                            {sk.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => {
                      handleCommitCareer(c.name);
                      setCompareData(null);
                    }}
                    className="w-full mt-6 py-2 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover shadow-soft"
                  >
                    Commit to {c.name}
                  </button>
                </div>
              ))}
            </div>

            {compareData.common_skills.length > 0 && (
              <div className="mt-6 p-4 bg-primary-tint/30 border border-primary/20 rounded-md">
                <div className="text-xs font-bold text-primary mb-1">
                  Shared Overlapping Skills Between Selected Roles:
                </div>
                <div className="text-xs text-ink">
                  {compareData.common_skills.join(', ')} — learning these prepares you for multiple careers simultaneously!
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Main Explorer View: List + Details */}
      <div className="grid lg:grid-cols-12 gap-6">
        {/* Left List of Careers */}
        <div className="lg:col-span-4 space-y-2.5">
          {careers.map((c) => {
            const isSelected = selectedCareer?.id === c.id;
            const inCompare = compareList.includes(c.id);

            return (
              <div
                key={c.id}
                onClick={() => handleSelectCareer(c.id)}
                className={`p-4 rounded-md border cursor-pointer transition-all ${
                  isSelected
                    ? 'border-primary bg-primary-tint/40 shadow-soft'
                    : 'border-border bg-surface hover:border-primary/40'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="font-serif font-bold text-sm text-ink">{c.name}</div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleToggleCompare(c.id);
                    }}
                    className={`text-[10px] px-2 py-0.5 rounded border transition-colors ${
                      inCompare
                        ? 'bg-primary text-white border-primary'
                        : 'border-border text-ink-muted hover:border-primary'
                    }`}
                  >
                    {inCompare ? '✓ Compare' : '+ Compare'}
                  </button>
                </div>
                <p className="text-xs text-ink-secondary line-clamp-2 mt-1">
                  {c.plain_description}
                </p>
                <div className="flex items-center gap-2 mt-2.5 text-[10px] text-ink-muted">
                  <span className="font-semibold text-status-success">{c.demand_level}</span>
                  <span>•</span>
                  <span>{c.suits_who.slice(0, 35)}...</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right Active Career Detail */}
        {selectedCareer && (
          <div className="lg:col-span-8 bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card space-y-6">
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-border">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h2 className="font-serif text-2xl font-bold text-ink">{selectedCareer.name}</h2>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-status-success/10 text-status-success">
                    {selectedCareer.demand_level} Demand
                  </span>
                </div>
                <p className="text-xs text-ink-secondary">{selectedCareer.plain_description}</p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleCommitCareer(selectedCareer.name)}
                  className="px-4 py-2 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center gap-1.5"
                >
                  <span>Choose This Role</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => handleShortlist(selectedCareer.id)}
                  className="px-3 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
                  title="Shortlist"
                >
                  <Star className="w-4 h-4 text-accent" />
                </button>
              </div>
            </div>

            {/* Day in the Life */}
            <div className="p-4 bg-bg rounded-md border border-border">
              <div className="text-xs font-bold text-ink mb-1 flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-primary" />
                <span>A Typical Day in the Life</span>
              </div>
              <p className="text-xs text-ink-secondary leading-relaxed">
                {selectedCareer.day_in_life}
              </p>
            </div>

            {/* Typical Tasks & Growth Path */}
            <div className="grid sm:grid-cols-2 gap-6">
              <div>
                <h4 className="text-xs font-bold text-ink mb-2">Typical Everyday Tasks</h4>
                <ul className="space-y-1.5 text-xs text-ink-secondary">
                  {selectedCareer.typical_tasks?.map((t: string, idx: number) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="text-xs font-bold text-ink mb-2">Career Growth Path</h4>
                <div className="space-y-2 text-xs">
                  {selectedCareer.growth_path?.map((step: string, idx: number) => (
                    <div key={idx} className="flex items-center gap-2">
                      <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-bold text-[10px] flex items-center justify-center shrink-0">
                        {idx + 1}
                      </span>
                      <span className="text-ink font-medium">{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Salary Note & Who It Suits */}
            <div className="p-4 rounded-md border border-border/80 bg-surface text-xs space-y-1.5">
              <div>
                <b>Approximate Salary Range:</b> {selectedCareer.salary_range_note}
              </div>
              <div className="text-ink-secondary">
                <b>Who It Best Suits:</b> {selectedCareer.suits_who}
              </div>
            </div>

            {/* Try Before You Choose Mini-Project */}
            <div className="p-5 border border-accent/40 bg-accent-tint/30 rounded-lg space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Code className="w-4 h-4 text-accent" />
                  <span className="font-serif font-bold text-sm text-ink">
                    Try Before You Choose (1-Hour Mini Project)
                  </span>
                </div>
                <span className="text-[11px] font-semibold text-accent-hover bg-accent-tint px-2 py-0.5 rounded">
                  {selectedCareer.mini_project?.duration || '1 hour'}
                </span>
              </div>

              <div className="font-semibold text-xs text-ink">
                {selectedCareer.mini_project?.title}
              </div>
              <p className="text-xs text-ink-secondary leading-relaxed">
                {selectedCareer.mini_project?.description}
              </p>

              <div className="space-y-1 text-xs text-ink">
                <b>Action Steps:</b>
                {selectedCareer.mini_project?.steps?.map((st: string, idx: number) => (
                  <div key={idx} className="text-xs text-ink-secondary pl-3">
                    {idx + 1}. {st}
                  </div>
                ))}
              </div>

              {selectedCareer.mini_project?.starter_code && (
                <pre className="p-3 bg-ink text-surface rounded text-[11px] font-mono overflow-x-auto">
                  {selectedCareer.mini_project.starter_code}
                </pre>
              )}

              <div className="text-[11px] text-status-success font-medium">
                ✓ Expected outcome: {selectedCareer.mini_project?.expected_outcome}
              </div>
            </div>

            {/* Core Required Skills */}
            <div>
              <h4 className="text-xs font-bold text-ink mb-3">Required Skills for this Role</h4>
              <div className="grid sm:grid-cols-2 gap-2.5">
                {selectedCareer.skills?.map((sk: any) => (
                  <div key={sk.skill_id} className="p-2.5 border border-border rounded bg-bg text-xs flex flex-col justify-between">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-semibold text-ink">
                        <GlossaryTooltip term={sk.name}>{sk.name}</GlossaryTooltip>
                      </span>
                      <span className="text-[10px] text-ink-muted">Target: Level {sk.target_level}</span>
                    </div>
                    <div className="text-[11px] text-ink-secondary line-clamp-2">
                      {sk.plain_explanation}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

