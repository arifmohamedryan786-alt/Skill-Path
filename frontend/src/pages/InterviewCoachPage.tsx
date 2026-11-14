import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import {
  Mic, MicOff, Play, CheckCircle2, ArrowRight,
  Sparkles, Award, RefreshCw, BarChart2, BookOpen
} from 'lucide-react';

export const InterviewCoachPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();

  const [role, setRole] = useState('AI/ML Engineer');
  const [difficulty, setDifficulty] = useState('Junior');
  const [session, setSession] = useState<any | null>(null);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [isRecording, setIsRecording] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState<any | null>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const h = await api.getInterviewHistory();
      setHistory(h);
    } catch {
      // ignore
    }
  };

  const handleStartSession = async () => {
    try {
      const data = await api.startInterview(role, difficulty);
      setSession(data);
      setCurrentQIndex(0);
      setAnswers({});
      setEvaluationResult(null);
      showToast(`Started ${difficulty} Mock Interview for ${role}`, 'success');
    } catch (err: any) {
      showToast(err.message || 'Failed to start interview', 'error');
    }
  };

  const handleSpeechInput = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      showToast('Speech recognition not supported in this browser. Please type your answer.', 'warning');
      return;
    }

    if (isRecording) {
      setIsRecording(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsRecording(true);
      recognition.onend = () => setIsRecording(false);
      recognition.onerror = () => setIsRecording(false);

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        if (session) {
          const qId = session.questions[currentQIndex]?.id;
          if (qId) {
            setAnswers((prev) => ({
              ...prev,
              [qId]: (prev[qId] ? prev[qId] + ' ' : '') + transcript
            }));
          }
        }
      };

      recognition.start();
    } catch {
      setIsRecording(false);
    }
  };

  const handleFinish = async () => {
    if (!session) return;
    setEvaluating(true);
    try {
      // Submit all answers
      for (const q of session.questions) {
        const text = answers[q.id] || '';
        await api.submitInterviewAnswer(session.session_id, q.id, text);
      }
      const graded = await api.finishInterview(session.session_id);
      setEvaluationResult(graded);
      showToast('Interview graded with rubric analysis!', 'success');
      loadHistory();
    } catch (err: any) {
      showToast(err.message || 'Grading failed', 'error');
    } finally {
      setEvaluating(false);
    }
  };

  const currentQ = session?.questions[currentQIndex];

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Mic className="w-5 h-5 text-primary" />
            <h1 className="font-serif text-2xl font-bold text-ink">Mock Interview Coach</h1>
          </div>
          <p className="text-xs text-ink-secondary">
            Practice technical and behavioral questions tailored to your gaps. Answer by voice or text and receive 4D rubric scoring.
          </p>
        </div>

        {!session && (
          <div className="flex flex-wrap items-center gap-2">
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="text-xs p-2 border border-border rounded bg-bg text-ink"
            >
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="Data Analyst">Data Analyst</option>
              <option value="Full Stack Developer">Full Stack Developer</option>
            </select>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="text-xs p-2 border border-border rounded bg-bg text-ink"
            >
              <option value="Intern">Intern</option>
              <option value="Junior">Junior</option>
              <option value="Mid-level">Mid-level</option>
            </select>
            <button
              onClick={handleStartSession}
              className="px-4 py-2 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover shadow-soft"
            >
              Start Session
            </button>
          </div>
        )}
      </div>

      {/* EVALUATION RESULTS VIEW */}
      {evaluationResult ? (
        <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-border">
            <div>
              <span className="text-xs font-bold text-primary uppercase tracking-wider">Evaluation Rubric</span>
              <h2 className="font-serif text-2xl font-bold text-ink mt-0.5">Interview Performance Report</h2>
            </div>
            <div className="text-right">
              <span className="text-2xl font-serif font-bold text-primary">
                {evaluationResult.rubric_scores?.overall || 3.5} / 5.0
              </span>
              <div className="text-[10px] text-ink-muted">Overall Score</div>
            </div>
          </div>

          {/* 4D Rubric Breakdown */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3 bg-bg rounded border border-border">
              <div className="text-[10px] text-ink-muted uppercase">Correctness</div>
              <div className="text-lg font-bold text-ink mt-0.5">{evaluationResult.rubric_scores?.correctness} / 5</div>
            </div>
            <div className="p-3 bg-bg rounded border border-border">
              <div className="text-[10px] text-ink-muted uppercase">Depth</div>
              <div className="text-lg font-bold text-ink mt-0.5">{evaluationResult.rubric_scores?.depth} / 5</div>
            </div>
            <div className="p-3 bg-bg rounded border border-border">
              <div className="text-[10px] text-ink-muted uppercase">Clarity</div>
              <div className="text-lg font-bold text-ink mt-0.5">{evaluationResult.rubric_scores?.clarity} / 5</div>
            </div>
            <div className="p-3 bg-bg rounded border border-border">
              <div className="text-[10px] text-ink-muted uppercase">Examples</div>
              <div className="text-lg font-bold text-ink mt-0.5">{evaluationResult.rubric_scores?.examples} / 5</div>
            </div>
          </div>

          {/* Strengths & Mistakes */}
          <div className="grid sm:grid-cols-2 gap-4 text-xs">
            <div className="p-4 bg-status-success-tint/40 border border-status-success/20 rounded-md space-y-1.5">
              <div className="font-bold text-status-success flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>What You Did Well:</span>
              </div>
              <ul className="space-y-1 text-ink-secondary pl-3">
                {evaluationResult.strengths?.map((s: string, idx: number) => (
                  <li key={idx}>• {s}</li>
                ))}
              </ul>
            </div>

            <div className="p-4 bg-status-warning-tint/40 border border-status-warning/20 rounded-md space-y-1.5">
              <div className="font-bold text-status-warning flex items-center gap-1.5">
                <Sparkles className="w-4 h-4" />
                <span>Areas to Polish:</span>
              </div>
              <ul className="space-y-1 text-ink-secondary pl-3">
                {evaluationResult.mistakes?.map((m: string, idx: number) => (
                  <li key={idx}>• {m}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Adaptive Feedback */}
          {evaluationResult.adaptation_note && (
            <div className="p-3.5 bg-primary-tint/30 border border-primary/20 rounded text-xs text-primary font-medium">
              💡 <b>Roadmap Adapted:</b> {evaluationResult.adaptation_note}
            </div>
          )}

          {/* Sample Answers */}
          <div className="space-y-3">
            <h3 className="font-serif font-bold text-sm text-ink">Ideal Sample Answers</h3>
            {evaluationResult.sample_answers?.map((sa: any, idx: number) => (
              <div key={idx} className="p-3.5 bg-bg rounded border border-border text-xs space-y-1">
                <div className="font-semibold text-ink">{sa.question}</div>
                <div className="text-ink-secondary leading-relaxed pl-2 border-l-2 border-primary">
                  {sa.ideal_answer}
                </div>
              </div>
            ))}
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-border">
            <button
              onClick={() => {
                setSession(null);
                setEvaluationResult(null);
              }}
              className="px-4 py-2 border border-border rounded text-xs font-semibold hover:bg-bg"
            >
              New Interview
            </button>
            <button
              onClick={() => onNavigate('/roadmap')}
              className="px-5 py-2 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover shadow-soft"
            >
              View Updated Roadmap
            </button>
          </div>
        </div>
      ) : session ? (
        /* ACTIVE SESSION INTERVIEW PLAYER */
        <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card space-y-6">
          <div className="flex items-center justify-between text-xs font-semibold text-ink-secondary">
            <span>Question {currentQIndex + 1} of {session.questions.length}</span>
            <span>Role: {session.role} ({session.difficulty})</span>
          </div>

          <div className="space-y-2">
            <span className="text-[11px] font-bold text-primary uppercase bg-primary-tint px-2 py-0.5 rounded">
              {currentQ?.topic}
            </span>
            <h2 className="font-serif text-xl sm:text-2xl font-bold text-ink leading-snug">
              {currentQ?.question}
            </h2>
            {currentQ?.hint && (
              <p className="text-xs text-ink-muted italic">Hint: {currentQ.hint}</p>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="text-xs font-semibold text-ink">Your Answer:</label>
              <button
                type="button"
                onClick={handleSpeechInput}
                className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-semibold transition-colors ${
                  isRecording
                    ? 'bg-status-danger text-white animate-pulse'
                    : 'bg-bg border border-border text-ink-secondary hover:text-ink'
                }`}
              >
                {isRecording ? <MicOff className="w-3.5 h-3.5" /> : <Mic className="w-3.5 h-3.5 text-primary" />}
                <span>{isRecording ? 'Listening (Speak now)...' : 'Use Voice Input'}</span>
              </button>
            </div>

            <textarea
              rows={6}
              value={answers[currentQ?.id] || ''}
              onChange={(e) => setAnswers({ ...answers, [currentQ?.id]: e.target.value })}
              placeholder="Speak or type your answer here using the STAR method (Situation, Task, Action, Result)..."
              className="w-full text-xs p-3 rounded-md bg-bg border border-border text-ink focus:outline-none focus:border-primary leading-relaxed"
            />
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-border">
            {currentQIndex > 0 ? (
              <button
                onClick={() => setCurrentQIndex(currentQIndex - 1)}
                className="px-4 py-2 border border-border rounded text-xs font-medium text-ink-secondary hover:text-ink"
              >
                Previous
              </button>
            ) : <div />}

            {currentQIndex < session.questions.length - 1 ? (
              <button
                onClick={() => setCurrentQIndex(currentQIndex + 1)}
                className="px-5 py-2.5 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover shadow-soft flex items-center gap-1.5"
              >
                <span>Next Question</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                onClick={handleFinish}
                disabled={evaluating}
                className="px-6 py-2.5 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover shadow-soft disabled:opacity-50"
              >
                {evaluating ? 'Grading Rubric...' : 'Complete & Grade Interview'}
              </button>
            )}
          </div>
        </div>
      ) : (
        /* EMPTY STATE / HISTORY */
        <div className="space-y-6">
          <div className="bg-surface border border-border rounded-lg p-8 text-center space-y-4">
            <Mic className="w-12 h-12 text-primary mx-auto" />
            <h2 className="font-serif text-2xl font-bold text-ink">Ready for your Mock Interview?</h2>
            <p className="text-xs text-ink-secondary max-w-md mx-auto leading-relaxed">
              SkillPath generates 5 targeted technical and behavioral questions based on your recent skill gaps. Use voice input or text to build interview confidence.
            </p>
            <button
              onClick={handleStartSession}
              className="px-6 py-2.5 bg-primary text-white text-xs font-semibold rounded hover:bg-primary-hover shadow-soft"
            >
              Start Junior {role} Interview
            </button>
          </div>

          {/* Past History */}
          {history.length > 0 && (
            <div className="bg-surface border border-border rounded-lg p-6 shadow-card">
              <h3 className="font-serif text-base font-bold text-ink mb-3">Past Session History</h3>
              <div className="divide-y divide-border/60">
                {history.map((h) => (
                  <div key={h.id} className="py-3 flex items-center justify-between text-xs">
                    <div>
                      <div className="font-semibold text-ink">{h.role} ({h.difficulty})</div>
                      <div className="text-[11px] text-ink-muted">{h.created_at}</div>
                    </div>
                    <div className="text-right">
                      <span className="font-bold text-primary">{h.overall_score} / 5.0</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

