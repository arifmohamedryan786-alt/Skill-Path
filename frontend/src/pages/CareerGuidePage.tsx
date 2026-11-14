import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import {
  BookOpen, Download, RefreshCw, Calendar, CheckCircle2,
  ExternalLink, Sparkles
} from 'lucide-react';

export const CareerGuidePage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [guide, setGuide] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadGuide();
  }, []);

  const loadGuide = async () => {
    setLoading(true);
    try {
      const data = await api.getCareerGuide();
      setGuide(data);
    } catch (err: any) {
      showToast(err.message || 'Failed to load guide', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = async () => {
    try {
      const updated = await api.regenerateCareerGuide();
      setGuide(updated);
      showToast('Career Guide re-analyzed and updated!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Regeneration failed', 'error');
    }
  };

  const handleDownloadPdf = async () => {
    try {
      const blob = await api.downloadGuidePdf();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `SkillPath_Guide_${guide?.target_career?.replace(/[\s\/]+/g, '_') || 'Career_Guide'}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      showToast('Guide PDF downloaded!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Download failed', 'error');
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Compiling comprehensive Career Guide...</div>;
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="w-5 h-5 text-primary" />
            <h1 className="font-serif text-2xl font-bold text-ink">
              Comprehensive Career Guide: {guide?.target_career}
            </h1>
          </div>
          <p className="text-xs text-ink-secondary">
            Generated on {guide?.generated_at} · Version {guide?.version}. Complete start-to-finish gameplan tailored to your current year and skills.
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleRegenerate}
            className="px-3.5 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Regenerate</span>
          </button>
          <button
            onClick={handleDownloadPdf}
            className="px-4 py-2 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export PDF</span>
          </button>
        </div>
      </div>

      {/* Guide Content Sections */}
      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card space-y-8 text-xs text-ink">
        {/* Section 1: Where You Stand Today */}
        <section className="space-y-2">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">1</span>
            <span>Where You Stand Today</span>
          </h2>
          <p className="text-ink-secondary leading-relaxed pl-7">
            {guide?.where_you_stand}
          </p>
        </section>

        {/* Section 2: Recommended Careers */}
        <section className="space-y-2">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">2</span>
            <span>Top Recommended Careers for Your Background</span>
          </h2>
          <p className="text-ink-secondary leading-relaxed pl-7">
            {guide?.top_careers_summary}
          </p>
        </section>

        {/* Section 3: Skills Sequence */}
        <section className="space-y-2">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">3</span>
            <span>Essential Skills in Order of Learning</span>
          </h2>
          <p className="text-ink-secondary leading-relaxed pl-7">
            {guide?.skills_sequence}
          </p>
        </section>

        {/* Section 4: Recommended Courses */}
        <section className="space-y-3">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">4</span>
            <span>Curated Online Courses (Verified Reputable)</span>
          </h2>
          <div className="grid sm:grid-cols-2 gap-3 pl-7">
            {guide?.recommended_courses?.map((c: any, idx: number) => (
              <a
                key={idx}
                href={c.url}
                target="_blank"
                rel="noreferrer"
                className="p-3 rounded border border-border bg-bg/50 hover:border-primary transition-colors block"
              >
                <div className="font-semibold text-ink flex items-center justify-between">
                  <span>{c.title}</span>
                  <ExternalLink className="w-3.5 h-3.5 text-ink-muted" />
                </div>
                <div className="text-[11px] text-ink-muted mt-1">
                  {c.provider} · {c.duration} {c.free && '· Free Audit'}
                </div>
              </a>
            ))}
          </div>
        </section>

        {/* Section 5: Projects Plan */}
        <section className="space-y-3">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">5</span>
            <span>Projects & Portfolio Blueprint</span>
          </h2>
          <div className="space-y-2.5 pl-7">
            <div className="p-3 bg-bg rounded border border-border">
              <span className="font-bold text-primary">Beginner Project: </span>
              <span className="text-ink-secondary">{guide?.projects_plan?.beginner}</span>
            </div>
            <div className="p-3 bg-bg rounded border border-border">
              <span className="font-bold text-primary">Intermediate Project: </span>
              <span className="text-ink-secondary">{guide?.projects_plan?.intermediate}</span>
            </div>
            <div className="p-3 bg-bg rounded border border-border">
              <span className="font-bold text-primary">Production Capstone: </span>
              <span className="text-ink-secondary">{guide?.projects_plan?.capstone}</span>
            </div>
          </div>
        </section>

        {/* Section 6: Internship Strategy */}
        <section className="space-y-2">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">6</span>
            <span>Internship & Job Search Strategy</span>
          </h2>
          <p className="text-ink-secondary leading-relaxed pl-7">
            {guide?.internship_strategy}
          </p>
        </section>

        {/* Section 7: 12-Month Progression Plan */}
        <section className="space-y-3">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">7</span>
            <span>12-Month Milestone Roadmap</span>
          </h2>
          <div className="space-y-2 pl-7">
            {guide?.twelve_month_plan?.map((m: any, idx: number) => (
              <div key={idx} className="p-3 rounded bg-bg/40 border border-border flex items-start gap-4">
                <span className="font-bold text-primary shrink-0 w-24">{m.months}</span>
                <div>
                  <div className="font-semibold text-ink">{m.focus}</div>
                  <div className="text-[11px] text-ink-secondary mt-0.5">{m.milestone}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Section 8: Next 7 Days */}
        <section className="space-y-3">
          <h2 className="font-serif text-lg font-bold text-ink border-b border-border/80 pb-1.5 flex items-center gap-2">
            <span className="w-5 h-5 rounded-full bg-primary-tint text-primary font-sans text-xs flex items-center justify-center font-bold">8</span>
            <span>Next 7 Days: Where to Start Today</span>
          </h2>
          <div className="grid sm:grid-cols-2 gap-2.5 pl-7">
            {guide?.next_7_days?.map((d: any, idx: number) => (
              <div key={idx} className="p-2.5 bg-bg rounded border border-border flex items-center gap-2.5">
                <span className="font-bold text-primary text-[11px] px-2 py-0.5 bg-primary-tint rounded">{d.day}</span>
                <span className="text-ink text-xs">{d.action}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

