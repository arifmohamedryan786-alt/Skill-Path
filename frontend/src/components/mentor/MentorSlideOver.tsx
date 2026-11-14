import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Bot, Sparkles, RefreshCw, ThumbsUp, ThumbsDown, AlertCircle } from 'lucide-react';
import { api } from '../../api/client';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

interface MentorSlideOverProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MentorSlideOver: React.FC<MentorSlideOverProps> = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  const { showToast } = useToast();
  const [messages, setMessages] = useState<Array<{ id?: number; role: string; content: string; time?: string; chips?: string[] }>>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiBusy, setAiBusy] = useState(false);
  const [chips, setChips] = useState<string[]>([
    "I don't know what career to choose",
    "Where should I start this week?",
    "When will I be job-ready?",
    "Build me a 12-month plan"
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const loadHistory = async () => {
    try {
      const history = await api.getMentorHistory();
      if (history.length > 0) {
        setMessages(history.map((m: any) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          time: m.created_at,
          chips: m.metadata?.suggested_chips
        })));
      } else {
        setMessages([
          {
            role: 'assistant',
            content: `Hello ${user?.full_name || 'there'}! I am your SkillPath AI Career Mentor. I'm here to guide your studies, answer technical questions in plain English, and keep you on track to getting hired. What would you like to explore today?`,
            chips: chips
          }
        ]);
      }
    } catch {
      // fallback
    }
  };

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || input;
    if (!text.trim() || loading) return;

    const userMsg = { role: 'user', content: text, time: 'Just now' };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.sendMentorMessage(text);
      if (res.ai_busy || (res.content && res.content.includes('AI is busy')) || (res.reply && res.reply.includes('AI is busy'))) {
        setAiBusy(true);
        setTimeout(() => setAiBusy(false), 9000);
      } else {
        setAiBusy(false);
      }
      const asstMsg = {
        role: 'assistant',
        content: res.content || res.reply || "I'm here to guide you step-by-step.",
        time: 'Just now',
        chips: res.suggested_chips
      };
      setMessages((prev) => [...prev, asstMsg]);
      if (res.suggested_chips && res.suggested_chips.length > 0) {
        setChips(res.suggested_chips);
      }
    } catch (err: any) {
      if (err.message && err.message.toLowerCase().includes('busy')) {
        setAiBusy(true);
        setTimeout(() => setAiBusy(false), 9000);
      }
      showToast(err.message || 'AI is busy, try again shortly', 'warning');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (msgId: number | undefined, type: 'helpful' | 'unhelpful') => {
    if (!msgId) return;
    try {
      await api.submitMentorFeedback(msgId, type);
      showToast('Thank you for the feedback!', 'success');
    } catch {
      // ignore
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-ink/20 backdrop-blur-xs transition-opacity animate-in fade-in duration-200">
      <div className="w-full max-w-md bg-surface h-full flex flex-col shadow-drawer border-l border-border animate-in slide-in-from-right duration-200">
        {/* Header */}
        <div className="h-16 px-4 border-b border-border flex items-center justify-between bg-surface">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-primary-tint flex items-center justify-center text-primary">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="font-serif font-bold text-sm text-ink flex items-center gap-1.5">
                AI Career Mentor
                <span className="w-2 h-2 rounded-full bg-status-success inline-block" />
              </div>
              <div className="text-[11px] text-ink-secondary">Personalized to your background & goal</div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-ink-muted hover:text-ink hover:bg-bg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-bg/50">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-md p-3 text-xs leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-primary text-white rounded-br-none shadow-soft'
                    : 'bg-surface text-ink border border-border rounded-bl-none shadow-soft'
                }`}
              >
                <div className="whitespace-pre-wrap">{m.content}</div>
                {m.role === 'assistant' && m.id && (
                  <div className="mt-2 pt-2 border-t border-border/50 flex items-center justify-between text-[10px] text-ink-muted">
                    <span>SkillPath Guidance</span>
                    <div className="flex items-center gap-1.5">
                      <button
                        onClick={() => handleFeedback(m.id, 'helpful')}
                        className="hover:text-status-success transition-colors p-0.5"
                        title="Helpful"
                      >
                        <ThumbsUp className="w-3 h-3" />
                      </button>
                      <button
                        onClick={() => handleFeedback(m.id, 'unhelpful')}
                        className="hover:text-status-danger transition-colors p-0.5"
                        title="Needs improvement"
                      >
                        <ThumbsDown className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 p-3 bg-surface border border-border rounded-md w-fit text-xs text-ink-secondary shadow-soft">
              <RefreshCw className="w-3.5 h-3.5 animate-spin text-primary" />
              <span>AI Mentor is thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Chips */}
        {chips.length > 0 && (
          <div className="px-4 py-2 border-t border-border/60 bg-surface flex flex-wrap gap-1.5">
            {chips.map((chip, cIdx) => (
              <button
                key={cIdx}
                onClick={() => handleSend(chip)}
                disabled={loading}
                className="text-[11px] px-2.5 py-1 rounded-full bg-bg hover:bg-primary-tint hover:text-primary text-ink-secondary border border-border transition-colors text-left"
              >
                {chip}
              </button>
            ))}
          </div>
        )}

        {/* Input */}
        <div className="p-3 border-t border-border bg-surface">
          {aiBusy && (
            <div className="mb-2 p-2 rounded-md bg-accent-tint border border-accent/40 text-ink text-[11px] flex items-center justify-between shadow-soft">
              <div className="flex items-center gap-1.5">
                <AlertCircle className="w-3.5 h-3.5 text-accent shrink-0" />
                <span className="font-semibold text-accent">AI is busy, try again shortly.</span>
              </div>
              <span className="text-[10px] text-ink-muted">Offline mode</span>
            </div>
          )}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything: study pacing, interview prep, career fit..."
              className="flex-1 text-xs px-3 py-2 rounded-md border border-border bg-bg text-ink focus:outline-none focus:border-primary transition-colors"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-2 rounded-md bg-primary text-white hover:bg-primary-hover disabled:opacity-40 transition-colors shrink-0 shadow-soft"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

