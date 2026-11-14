import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { ShieldCheck, Award, CheckCircle2, Lock, ArrowLeft } from 'lucide-react';
import { PassportBadgeIllustration } from '../components/illustrations/LineArtIllustrations';

export const PublicPassportPage: React.FC<{ slug: string; onNavigate: (path: string) => void }> = ({ slug, onNavigate }) => {
  const [data, setData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadPublic() {
      setLoading(true);
      try {
        const res = await api.getPublicPassport(slug);
        setData(res);
      } catch (err: any) {
        setError(err.message || 'Public profile not found or is set to private.');
      } finally {
        setLoading(false);
      }
    }
    loadPublic();
  }, [slug]);

  if (loading) {
    return <div className="p-12 text-center text-sm text-ink-secondary animate-pulse">Verifying cryptographic passport credentials...</div>;
  }

  if (error || !data) {
    return (
      <div className="max-w-md mx-auto my-12 p-8 bg-surface border border-border rounded-lg shadow-card text-center space-y-4">
        <Lock className="w-10 h-10 text-status-warning mx-auto" />
        <h2 className="font-serif text-xl font-bold text-ink">Passport Unavailable</h2>
        <p className="text-xs text-ink-secondary">{error}</p>
        <button
          onClick={() => onNavigate('/dashboard')}
          className="px-4 py-2 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover"
        >
          Return to SkillPath
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-8 space-y-8">
      {/* Back button */}
      <button
        onClick={() => onNavigate('/dashboard')}
        className="flex items-center gap-1.5 text-xs text-ink-secondary hover:text-ink font-medium"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Platform</span>
      </button>

      {/* Main Certificate Card */}
      <div className="bg-surface border-2 border-primary/20 rounded-lg p-8 shadow-card space-y-6 relative overflow-hidden">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pb-6 border-b border-border text-center sm:text-left">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-status-success-tint text-status-success border border-status-success/30 mb-2">
              <ShieldCheck className="w-4 h-4" />
              <span>SkillPath Cryptographically Verified Record</span>
            </div>
            <h1 className="font-serif text-3xl font-bold text-ink">{data.full_name}</h1>
            <p className="text-xs text-ink-secondary mt-1">
              {data.education} in {data.branch} · Target Role: <b>{data.target_career}</b>
            </p>
          </div>

          <div className="w-20 h-20 rounded-full border-4 border-primary flex flex-col items-center justify-center text-primary shrink-0 shadow-soft">
            <span className="text-lg font-bold font-serif leading-none">{data.readiness_pct}%</span>
            <span className="text-[9px] uppercase tracking-wider font-semibold">Ready</span>
          </div>
        </div>

        {/* Verified Skills Grid */}
        <div className="space-y-4">
          <h3 className="font-serif text-lg font-bold text-ink">
            Verified Competencies ({data.verified_count})
          </h3>

          <div className="grid sm:grid-cols-2 gap-4">
            {data.verified_skills.map((vs: any) => (
              <div
                key={vs.id}
                className="p-4 bg-bg rounded-md border border-border space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-ink">{vs.skill_name}</span>
                  <span className="text-[10px] font-bold text-status-success uppercase bg-status-success-tint px-2 py-0.5 rounded">
                    Level {vs.verified_level}
                  </span>
                </div>
                {vs.score_pct > 0 && (
                  <div className="text-[11px] text-ink-secondary">
                    Assessment Score: <b>{vs.score_pct}%</b>
                  </div>
                )}
                <div className="p-2 bg-surface rounded border border-border text-[9px] font-mono text-ink-muted break-all">
                  SHA-256: {vs.verification_hash}
                </div>
                <div className="text-[10px] text-status-success font-medium flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" />
                  <span>Verified on {vs.verified_at}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-4 bg-primary-tint/30 rounded-md border border-primary/20 text-xs text-ink text-center">
          This record was generated directly by SkillPath. Each verified badge has been mathematically proven by primary exam logs.
        </div>
      </div>
    </div>
  );
};

