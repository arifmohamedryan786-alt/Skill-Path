import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import { PassportData } from '../types';
import QRCode from 'qrcode';
import {
  Award, ShieldCheck, Download, Share2, Copy,
  CheckCircle2, Lock, Eye, ExternalLink, QrCode as QrIcon, X
} from 'lucide-react';
import { PassportBadgeIllustration } from '../components/illustrations/LineArtIllustrations';

export const PassportPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [passport, setPassport] = useState<PassportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [verifyingId, setVerifyingId] = useState<number | null>(null);
  const [verificationModal, setVerificationModal] = useState<any | null>(null);
  const [showQrModal, setShowQrModal] = useState(false);
  const [qrCodeDataUrl, setQrCodeDataUrl] = useState('');

  useEffect(() => {
    loadPassport();
  }, []);

  const loadPassport = async () => {
    setLoading(true);
    try {
      const data = await api.getPassport();
      setPassport(data);
      // Generate QR code
      const publicLink = `${window.location.origin}/passport/${data.slug}`;
      const qrUrl = await QRCode.toDataURL(publicLink, { width: 220, margin: 2 });
      setQrCodeDataUrl(qrUrl);
    } catch (err: any) {
      showToast(err.message || 'Failed to load passport', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePrivacy = async (field: 'is_public' | 'show_scores' | 'show_evidence') => {
    if (!passport) return;
    try {
      const updatePayload = { [field]: !passport[field] };
      const updated = await api.updatePassport(updatePayload);
      setPassport(updated);
      showToast('Passport privacy settings updated', 'success');
    } catch (err: any) {
      showToast(err.message || 'Failed to update settings', 'error');
    }
  };

  const handleVerifyHash = async (skillId: number) => {
    setVerifyingId(skillId);
    try {
      const res = await api.verifySkillHash(skillId);
      setVerificationModal(res);
    } catch (err: any) {
      showToast(err.message || 'Verification failed', 'error');
    } finally {
      setVerifyingId(null);
    }
  };

  const handleCopyLink = () => {
    if (!passport) return;
    const url = `${window.location.origin}/passport/${passport.slug}`;
    navigator.clipboard.writeText(url);
    showToast('Public Passport link copied to clipboard!', 'success');
  };

  const handleDownloadPdf = async () => {
    try {
      const blob = await api.downloadPassportPdf();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `SkillPath_Passport_${passport?.slug || 'certificate'}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      showToast('Skill Passport PDF downloaded!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Download failed', 'error');
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Loading verified credentials...</div>;
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header Banner */}
      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 text-center md:text-left">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-status-success-tint text-status-success border border-status-success/20">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Cryptographically Verified Credential</span>
          </div>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-ink">
            {passport?.full_name}'s Skill Passport
          </h1>
          <p className="text-xs text-ink-secondary leading-relaxed">
            Target Career: <b>{passport?.target_career}</b> ({passport?.readiness_pct}% job-ready).
            Each verified badge is cryptographically anchored by a SHA-256 immutable assessment hash.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 shrink-0">
          <button
            onClick={handleCopyLink}
            className="px-3.5 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center gap-1.5"
          >
            <Copy className="w-3.5 h-3.5" />
            <span>Copy Link</span>
          </button>
          <button
            onClick={() => setShowQrModal(true)}
            className="px-3.5 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center gap-1.5"
          >
            <QrIcon className="w-3.5 h-3.5 text-primary" />
            <span>QR Code</span>
          </button>
          <button
            onClick={handleDownloadPdf}
            className="px-4 py-2 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center gap-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>PDF Export</span>
          </button>
        </div>
      </div>

      {/* Privacy Toggles Bar */}
      <div className="bg-surface border border-border rounded-lg p-4 shadow-soft flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-ink">Public URL:</span>
          <code className="px-2 py-0.5 bg-bg border border-border rounded text-[11px] text-primary">
            /passport/{passport?.slug}
          </code>
        </div>

        <div className="flex items-center gap-6">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={passport?.is_public}
              onChange={() => handleTogglePrivacy('is_public')}
              className="accent-primary rounded"
            />
            <span className="text-ink-secondary">Publicly Searchable</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={passport?.show_scores}
              onChange={() => handleTogglePrivacy('show_scores')}
              className="accent-primary rounded"
            />
            <span className="text-ink-secondary">Display Test Scores</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={passport?.show_evidence}
              onChange={() => handleTogglePrivacy('show_evidence')}
              className="accent-primary rounded"
            />
            <span className="text-ink-secondary">Show SHA-256 Hashes</span>
          </label>
        </div>
      </div>

      {/* Verified Badges Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-serif text-xl font-bold text-ink">
            Verified Badges ({passport?.verified_skills.length || 0})
          </h2>
          <span className="text-xs text-ink-muted">Requires 70%+ score on practical checkpoints</span>
        </div>

        {passport?.verified_skills && passport.verified_skills.length > 0 ? (
          <div className="grid md:grid-cols-2 gap-4">
            {passport.verified_skills.map((vs) => (
              <div
                key={vs.id}
                className="bg-surface border border-status-success/30 rounded-lg p-5 shadow-soft space-y-3 relative overflow-hidden"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-full bg-status-success/10 text-status-success flex items-center justify-center shrink-0">
                      <ShieldCheck className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-ink">{vs.skill_name}</h3>
                      <div className="text-[11px] text-ink-secondary">Level {vs.verified_level} Mastery</div>
                    </div>
                  </div>

                  {passport.show_scores && (
                    <span className="px-2 py-0.5 rounded bg-status-success text-white font-bold text-xs">
                      {vs.score_pct}% Score
                    </span>
                  )}
                </div>

                {passport.show_evidence && (
                  <div className="p-2.5 bg-bg border border-border rounded text-[10px] space-y-1 font-mono text-ink-muted break-all">
                    <div className="font-sans font-semibold text-ink">Cryptographic Proof:</div>
                    <div>Hash: {vs.verification_hash}</div>
                    <div className="font-sans text-ink-secondary">Issued: {vs.verified_at} · Ref: {vs.evidence_ref}</div>
                  </div>
                )}

                <div className="pt-2 border-t border-border/60 flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-status-success flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Verified Authenticated</span>
                  </span>

                  <button
                    onClick={() => handleVerifyHash(vs.skill_id)}
                    disabled={verifyingId === vs.skill_id}
                    className="px-2.5 py-1 text-[11px] font-semibold text-primary bg-primary-tint hover:bg-primary-light rounded transition-colors"
                  >
                    {verifyingId === vs.skill_id ? 'Verifying...' : 'Verify Cryptographic Hash'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-surface border border-border rounded-lg p-8 text-center space-y-3">
            <PassportBadgeIllustration className="w-20 h-24 mx-auto" />
            <div className="font-serif font-bold text-lg text-ink">No Verified Badges Yet</div>
            <p className="text-xs text-ink-secondary max-w-sm mx-auto">
              Score 70% or higher on any SkillPath checkpoint test to earn your first tamper-evident verified credential badge.
            </p>
            <button
              onClick={() => onNavigate('/assessments')}
              className="px-5 py-2 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors"
            >
              Take a Checkpoint Test
            </button>
          </div>
        )}
      </div>

      {/* Cryptographic Verification Modal */}
      {verificationModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-xs animate-in fade-in duration-150">
          <div className="bg-surface border border-border rounded-lg max-w-md w-full p-6 shadow-drawer space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <div className="flex items-center gap-2 text-status-success font-bold text-sm">
                <ShieldCheck className="w-5 h-5" />
                <span>SHA-256 Tamper Verification</span>
              </div>
              <button
                onClick={() => setVerificationModal(null)}
                className="p-1 rounded text-ink-muted hover:text-ink"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-2 text-xs">
              <div className="font-semibold text-ink">Skill: {verificationModal.skill_name}</div>
              <div className="p-3 bg-bg border border-border rounded font-mono text-[11px] break-all space-y-1">
                <div><b>Stored Hash:</b> {verificationModal.stored_hash}</div>
                <div><b>Recomputed:</b> {verificationModal.recomputed_hash}</div>
              </div>
              <p className="text-xs text-status-success font-semibold pt-1">
                {verificationModal.details}
              </p>
            </div>

            <button
              onClick={() => setVerificationModal(null)}
              className="w-full py-2 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* QR Code Modal */}
      {showQrModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-xs animate-in fade-in duration-150">
          <div className="bg-surface border border-border rounded-lg max-w-sm w-full p-6 shadow-drawer text-center space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-border">
              <h3 className="font-serif font-bold text-sm text-ink">Public Passport QR Code</h3>
              <button onClick={() => setShowQrModal(false)} className="p-1 rounded text-ink-muted hover:text-ink">
                <X className="w-4 h-4" />
              </button>
            </div>

            {qrCodeDataUrl && (
              <img src={qrCodeDataUrl} alt="Passport QR" className="mx-auto rounded border border-border shadow-soft" />
            )}

            <p className="text-xs text-ink-secondary">
              Scan this code on any smartphone to open the verified employer view.
            </p>

            <button
              onClick={() => setShowQrModal(false)}
              className="w-full py-2 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover"
            >
              Done
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

