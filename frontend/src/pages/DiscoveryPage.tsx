import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../context/AuthContext';
import { CareerMatch } from '../types';
import { CompassIllustration } from '../components/illustrations/LineArtIllustrations';
import {
  Compass, CheckCircle2, ArrowRight, ArrowLeft,
  Sparkles, Star, Eye, Code, RefreshCw
} from 'lucide-react';

export const DiscoveryPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { user } = useAuth();
  const { showToast } = useToast();

  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [results, setResults] = useState<{
    top_careers: CareerMatch[];
    aptitude_scores: Record<string, number>;
    summary_message: string;
  } | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [qList, resData] = await Promise.all([
          api.getDiscoveryQuestions(),
          api.getDiscoveryResults()
        ]);
        setQuestions(qList);
        if (resData && resData.top_careers && resData.top_careers.length > 0) {
          setResults(resData);
        }
      } catch (err) {
        // fallback
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleSelectOption = (value: string) => {
    if (!questions[currentIdx]) return;
    const qId = questions[currentIdx].id.toString();
    setAnswers((prev) => ({ ...prev, [qId]: value }));
  };

  const handleNext = async () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(currentIdx + 1);
    } else {
      // Submit
      setSubmitting(true);
      try {
        const res = await api.submitDiscoveryAnswers(answers);
        setResults(res);
        showToast('Assessment evaluated! Your top matching careers are ready.', 'success');
      } catch (err: any) {
        showToast(err.message || 'Submission failed', 'error');
      } finally {
        setSubmitting(false);
      }
    }
  };

  const handleSelectPrimaryCareer = async (career: CareerMatch) => {
    try {
      await api.updateProfile({ career_goal: career.name, goal_status: 'known' });
      showToast(`Selected ${career.name} as your primary goal! Roadmap regenerated.`, 'success');
      onNavigate('/roadmap');
    } catch (err: any) {
      showToast(err.message || 'Failed to update goal', 'error');
    }
  };

  const handleShortlist = async (career: CareerMatch) => {
    try {
      await api.addToShortlist(career.career_id, false, 'Saved from Discovery Assessment');
      showToast(`Added ${career.name} to your shortlist.`, 'success');
    } catch (err: any) {
      showToast(err.message || 'Failed to shortlist', 'error');
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Loading Career Discovery questions...</div>;
  }

  // View Results Screen
  if (results) {
    return (
      <div className="space-y-8 max-w-4xl mx-auto">
        {/* Results Banner */}
        <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-primary-tint text-primary border border-primary/20">
              <Sparkles className="w-3.5 h-3.5 text-accent" />
              <span>Assessment Completed</span>
            </div>
            <h1 className="font-serif text-2xl sm:text-3xl font-bold text-ink">
              Your Top 5 Career Matches
            </h1>
            <p className="text-sm text-ink-secondary leading-relaxed">
              {results.summary_message}
            </p>
          </div>

          <div className="shrink-0 flex items-center gap-2">
            <button
              onClick={() => {
                setResults(null);
                setCurrentIdx(0);
                setAnswers({});
              }}
              className="px-3.5 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retake Assessment</span>
            </button>
          </div>
        </div>

        {/* Aptitude Radar Summary Pills */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {Object.entries(results.aptitude_scores).map(([trait, score]) => (
            <div key={trait} className="bg-surface border border-border rounded-md p-3 text-center shadow-soft">
              <div className="text-[11px] font-semibold text-ink-muted uppercase tracking-wider">{trait} Aptitude</div>
              <div className="text-xl font-serif font-bold text-primary mt-0.5">{score}%</div>
            </div>
          ))}
        </div>

        {/* Ranked Career Cards */}
        <div className="space-y-4">
          {results.top_careers.map((career, idx) => (
            <div
              key={career.career_id}
              className={`bg-surface border rounded-lg p-6 shadow-card transition-all ${
                idx === 0 ? 'border-primary ring-1 ring-primary/30' : 'border-border'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                <div className="space-y-2 flex-1">
                  <div className="flex items-center gap-2.5">
                    <span className="w-6 h-6 rounded-full bg-primary-tint text-primary font-bold text-xs flex items-center justify-center shrink-0">
                      #{idx + 1}
                    </span>
                    <h3 className="font-serif text-xl font-bold text-ink">{career.name}</h3>
                    <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-status-success/10 text-status-success">
                      {career.match_pct}% Match
                    </span>
                    <span className="text-[11px] text-ink-muted px-2 py-0.5 bg-bg border border-border rounded-md">
                      {career.demand_level} Demand
                    </span>
                  </div>

                  <p className="text-xs text-ink leading-relaxed">
                    <b>Why it fits you:</b> {career.plain_reason}
                  </p>

                  <p className="text-xs text-ink-secondary">
                    <b>Who it suits:</b> {career.suits_who}
                  </p>

                  <div className="text-[11px] text-ink-muted pt-1">
                    Entry titles: {career.entry_titles.slice(0, 3).join(', ')}
                  </div>
                </div>

                <div className="flex sm:flex-col gap-2 shrink-0">
                  <button
                    onClick={() => handleSelectPrimaryCareer(career)}
                    className="flex-1 sm:flex-none px-4 py-2 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center justify-center gap-1.5"
                  >
                    <span>Choose This Career</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>

                  <button
                    onClick={() => onNavigate(`/careers`)}
                    className="flex-1 sm:flex-none px-4 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center justify-center gap-1.5"
                  >
                    <Code className="w-3.5 h-3.5 text-accent" />
                    <span>Try 1-Hr Mini Project</span>
                  </button>

                  <button
                    onClick={() => handleShortlist(career)}
                    className="flex-1 sm:flex-none px-4 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors flex items-center justify-center gap-1.5"
                  >
                    <Star className="w-3.5 h-3.5 text-accent" />
                    <span>Shortlist</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Active Questions Assessment View
  const currentQ = questions[currentIdx];
  const selectedAnswer = currentQ ? answers[currentQ.id.toString()] : null;

  return (
    <div className="max-w-2xl mx-auto py-4">
      {/* Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs font-semibold text-ink-secondary mb-2">
          <span>Question {currentIdx + 1} of {questions.length}</span>
          <span className="uppercase text-[11px] tracking-wider text-primary font-bold">{currentQ?.category}</span>
        </div>
        <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-200 rounded-full"
            style={{ width: `${((currentIdx + 1) / questions.length) * 100}%` }}
          />
        </div>
      </div>

      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card">
        <h2 className="font-serif text-xl sm:text-2xl font-bold text-ink mb-2 leading-snug">
          {currentQ?.question}
        </h2>
        {currentQ?.help_text && (
          <p className="text-xs text-ink-secondary mb-6">{currentQ.help_text}</p>
        )}

        <div className="space-y-3 mb-8">
          {currentQ?.options?.map((opt: any) => {
            const isSelected = selectedAnswer === opt.value;
            return (
              <button
                key={opt.value}
                type="button"
                onClick={() => handleSelectOption(opt.value)}
                className={`w-full p-4 rounded-md border text-left transition-all flex items-start gap-3.5 ${
                  isSelected
                    ? 'border-primary bg-primary-tint/40 ring-1 ring-primary'
                    : 'border-border hover:bg-bg'
                }`}
              >
                <div
                  className={`w-5 h-5 rounded-full border mt-0.5 flex items-center justify-center shrink-0 ${
                    isSelected ? 'border-primary bg-primary text-white' : 'border-border'
                  }`}
                >
                  {isSelected && <CheckCircle2 className="w-3.5 h-3.5" />}
                </div>
                <div className="text-xs sm:text-sm font-medium text-ink leading-relaxed">
                  {opt.label}
                </div>
              </button>
            );
          })}
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-border">
          {currentIdx > 0 ? (
            <button
              onClick={() => setCurrentIdx(currentIdx - 1)}
              className="flex items-center gap-1 px-4 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Previous</span>
            </button>
          ) : (
            <div />
          )}

          <button
            onClick={handleNext}
            disabled={!selectedAnswer || submitting}
            className="flex items-center gap-1.5 px-6 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors disabled:opacity-40"
          >
            <span>{currentIdx === questions.length - 1 ? 'Evaluate My Results' : 'Next Question'}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};

