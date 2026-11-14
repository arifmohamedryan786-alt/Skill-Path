import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import { AssessmentOut } from '../types';
import {
  CheckSquare, Award, ArrowRight, ArrowLeft,
  CheckCircle2, AlertCircle, RefreshCw, Code, Sparkles
} from 'lucide-react';

export const AssessmentsPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [assessment, setAssessment] = useState<AssessmentOut | null>(null);
  const [selectedSkillSlug, setSelectedSkillSlug] = useState('python-basics');
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [mcqAnswers, setMcqAnswers] = useState<Record<number, number>>({});
  const [practicalCode, setPracticalCode] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<any | null>(null);

  const availableSkills = [
    { slug: 'python-basics', name: 'Python Basics' },
    { slug: 'statistics-probability', name: 'Statistics & Probability' },
    { slug: 'sql-basics', name: 'SQL Basics' }
  ];

  useEffect(() => {
    loadAssessment(selectedSkillSlug);
  }, [selectedSkillSlug]);

  const loadAssessment = async (slug: string) => {
    setLoading(true);
    setResult(null);
    setCurrentQIndex(0);
    setMcqAnswers({});
    try {
      const data = await api.generateAssessment(slug);
      setAssessment(data);
      setPracticalCode(data.practical_task?.starter_code || '');
    } catch (err: any) {
      showToast(err.message || 'Failed to load assessment', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (optIndex: number) => {
    if (!assessment) return;
    const q = assessment.questions[currentQIndex];
    if (q) {
      setMcqAnswers((prev) => ({ ...prev, [q.id]: optIndex }));
    }
  };

  const handleSubmit = async () => {
    if (!assessment) return;
    setSubmitting(true);
    try {
      const res = await api.submitAssessment({
        assessment_id: assessment.id,
        mcq_answers: mcqAnswers,
        practical_code: practicalCode
      });
      setResult(res);
      if (res.passed) {
        showToast(`Passed with ${res.score_pct}%! Verified credential badge unlocked.`, 'success');
      } else {
        showToast(`Scored ${res.score_pct}%. Remedial recommendations have been added.`, 'warning');
      }
    } catch (err: any) {
      showToast(err.message || 'Evaluation failed', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Generating skill assessment...</div>;
  }

  // RESULT VIEW
  if (result) {
    const passed = result.passed;
    return (
      <div className="max-w-2xl mx-auto py-6 space-y-6">
        <div className={`bg-surface border rounded-lg p-6 sm:p-8 shadow-card text-center ${
          passed ? 'border-status-success' : 'border-status-warning'
        }`}>
          <div className={`w-14 h-14 rounded-full mx-auto flex items-center justify-center mb-4 ${
            passed ? 'bg-status-success-tint text-status-success' : 'bg-status-warning-tint text-status-warning'
          }`}>
            {passed ? <Award className="w-8 h-8" /> : <AlertCircle className="w-8 h-8" />}
          </div>

          <h2 className="font-serif text-2xl font-bold text-ink mb-1">
            {passed ? 'Assessment Mastered!' : 'Checkpoint Completed'}
          </h2>
          <div className="text-3xl font-serif font-bold text-primary mb-2">
            {result.score_pct}%
          </div>
          <p className="text-xs text-ink-secondary max-w-md mx-auto mb-6 leading-relaxed">
            {result.feedback_summary}
          </p>

          {passed && result.verification_hash && (
            <div className="p-4 bg-primary-tint/30 border border-primary/20 rounded-md text-left mb-6 space-y-1">
              <div className="text-[11px] font-bold text-primary uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                <span>SHA-256 Tamper-Evident Fingerprint</span>
              </div>
              <div className="text-[11px] font-mono text-ink-muted break-all">
                {result.verification_hash}
              </div>
              <div className="text-[11px] text-status-success font-semibold pt-1">
                ✓ Recorded to your Skill Passport with level promotion!
              </div>
            </div>
          )}

          <div className="flex items-center justify-center gap-3">
            <button
              onClick={() => onNavigate('/passport')}
              className="px-5 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center gap-1.5"
            >
              <span>View in Skill Passport</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => loadAssessment(selectedSkillSlug)}
              className="px-4 py-2.5 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
            >
              Retake Checkpoint
            </button>
          </div>
        </div>
      </div>
    );
  }

  // PLAYER VIEW
  const questions = assessment?.questions || [];
  const currentQ = questions[currentQIndex];
  const isPracticalStep = currentQIndex === questions.length;
  const currentSelection = currentQ ? mcqAnswers[currentQ.id] : undefined;

  return (
    <div className="max-w-2xl mx-auto py-4 space-y-6">
      {/* Skill Selector Switcher */}
      <div className="flex items-center justify-between bg-surface border border-border p-3 rounded-md shadow-soft">
        <span className="text-xs font-semibold text-ink-secondary">Select Skill Checkpoint:</span>
        <div className="flex gap-2">
          {availableSkills.map((sk) => (
            <button
              key={sk.slug}
              onClick={() => setSelectedSkillSlug(sk.slug)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                selectedSkillSlug === sk.slug
                  ? 'bg-primary text-white shadow-soft font-semibold'
                  : 'bg-bg text-ink-secondary hover:text-ink border border-border'
              }`}
            >
              {sk.name}
            </button>
          ))}
        </div>
      </div>

      {/* Progress Bar */}
      <div>
        <div className="flex items-center justify-between text-xs font-semibold text-ink-secondary mb-2">
          <span>{isPracticalStep ? 'Practical Task' : `Question ${currentQIndex + 1} of ${questions.length}`}</span>
          <span>Target: Level {assessment?.target_level} Badge</span>
        </div>
        <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-200 rounded-full"
            style={{ width: `${((currentQIndex + 1) / (questions.length + 1)) * 100}%` }}
          />
        </div>
      </div>

      {/* Main Question / Practical Card */}
      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card">
        {!isPracticalStep && currentQ ? (
          <div>
            <h2 className="font-serif text-xl font-bold text-ink mb-6 leading-snug">
              {currentQ.question}
            </h2>

            <div className="space-y-3 mb-8">
              {currentQ.options.map((opt: string, oIdx: number) => {
                const isSelected = currentSelection === oIdx;
                return (
                  <button
                    key={oIdx}
                    onClick={() => handleSelectOption(oIdx)}
                    className={`w-full p-4 rounded-md border text-left text-xs sm:text-sm font-medium transition-all flex items-start gap-3 ${
                      isSelected
                        ? 'border-primary bg-primary-tint/40 ring-1 ring-primary'
                        : 'border-border hover:bg-bg'
                    }`}
                  >
                    <div className={`w-5 h-5 rounded-full border mt-0.5 flex items-center justify-center shrink-0 ${
                      isSelected ? 'border-primary bg-primary text-white' : 'border-border'
                    }`}>
                      {isSelected && <CheckCircle2 className="w-3.5 h-3.5" />}
                    </div>
                    <span className="text-ink leading-relaxed">{opt}</span>
                  </button>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-primary font-bold text-xs uppercase tracking-wider">
              <Code className="w-4 h-4" />
              <span>Practical Hands-on Task</span>
            </div>
            <h3 className="font-serif text-lg font-bold text-ink">
              {assessment?.practical_task?.prompt}
            </h3>
            {assessment?.practical_task?.hint && (
              <p className="text-xs text-ink-secondary bg-primary-tint/30 p-3 rounded border border-primary/20">
                💡 <b>Hint:</b> {assessment.practical_task.hint}
              </p>
            )}

            <div>
              <label className="block text-xs font-semibold text-ink mb-1">Your Code Submission:</label>
              <textarea
                rows={7}
                value={practicalCode}
                onChange={(e) => setPracticalCode(e.target.value)}
                className="w-full text-xs font-mono p-3 rounded-md bg-ink text-surface border border-border focus:outline-none focus:ring-1 focus:ring-primary"
                placeholder="# Write your Python or SQL code here"
              />
            </div>
          </div>
        )}

        {/* Footer Navigation */}
        <div className="flex items-center justify-between pt-4 border-t border-border">
          {currentQIndex > 0 ? (
            <button
              onClick={() => setCurrentQIndex(currentQIndex - 1)}
              className="flex items-center gap-1 px-4 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back</span>
            </button>
          ) : (
            <div />
          )}

          {!isPracticalStep ? (
            <button
              onClick={() => setCurrentQIndex(currentQIndex + 1)}
              disabled={currentSelection === undefined}
              className="flex items-center gap-1.5 px-6 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors disabled:opacity-40"
            >
              <span>{currentQIndex === questions.length - 1 ? 'Go to Practical Task' : 'Next Question'}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="flex items-center gap-1.5 px-6 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors disabled:opacity-40"
            >
              <span>{submitting ? 'Evaluating...' : 'Submit & Grade Checkpoint'}</span>
              <Award className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
