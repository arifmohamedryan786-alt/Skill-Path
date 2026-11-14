import React, { useState, useEffect, useRef } from 'react';
import {
  Bot,
  User,
  Send,
  Sparkles,
  ThumbsUp,
  ThumbsDown,
  Copy,
  Check,
  Compass,
  Map,
  BookOpen,
  Calendar,
  AlertCircle
} from 'lucide-react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

interface ChatMessage {
  id: number;
  sender: 'user' | 'assistant';
  content: string;
  created_at: string;
  feedback?: string;
}

const STARTER_PROMPTS = [
  "Explain what an API is in plain language without jargon",
  "I'm feeling overwhelmed by learning to code. Where should I start?",
  "What is the difference between a Data Analyst and Data Scientist?",
  "How should I organize my 10 hours of study this week?",
  "Can you review my study goals and give me one mini project idea?"
];

export const MentorPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { user } = useAuth();
  const { addToast } = useToast();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiBusy, setAiBusy] = useState(false);
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const loadChatHistory = async () => {
    try {
      const res = await api.getMentorHistory();
      if (res && res.history && res.history.length > 0) {
        setMessages(res.history);
      } else {
        // Initial friendly greeting
        setMessages([
          {
            id: 1,
            sender: 'assistant',
            content: `Hello ${user?.profile?.full_name || user?.full_name || 'there'}! 👋 I am your personal SkillPath AI Mentor. My only goal is to guide you step-by-step from zero to job-ready.\n\nWhether you have never written a line of code, don't know what tech career fits you, or feel stuck on a tough concept — ask me anything. There are no silly questions here!`,
            created_at: new Date().toISOString()
          }
        ]);
      }
    } catch {
      // Fallback greeting if fetch fails
      setMessages([
        {
          id: 1,
          sender: 'assistant',
          content: `Hi ${user?.profile?.full_name || user?.full_name || 'there'}! 👋 I'm your AI Mentor. Ask me anything about skills, roadmaps, job roles, or getting unstuck.`,
          created_at: new Date().toISOString()
        }
      ]);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputText).trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now(),
      sender: 'user',
      content: text,
      created_at: new Date().toISOString()
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res = await api.sendMentorMessage(text);
      if (res.ai_busy || (res.reply && res.reply.includes('AI is busy')) || (res.content && res.content.includes('AI is busy'))) {
        setAiBusy(true);
        setTimeout(() => setAiBusy(false), 9000);
      } else {
        setAiBusy(false);
      }
      const assistantMsg: ChatMessage = {
        id: res.message_id || Date.now() + 1,
        sender: 'assistant',
        content: res.reply || res.content || "I'm here to support your learning journey. Let's keep making progress!",
        created_at: new Date().toISOString()
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      if (err.message && err.message.toLowerCase().includes('busy')) {
        setAiBusy(true);
        setTimeout(() => setAiBusy(false), 9000);
      }
      addToast(err.message || 'AI is busy, try again shortly.', 'warning');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id: number, content: string) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    addToast('Copied to clipboard', 'info');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleFeedback = async (msgId: number, feedback: 'helpful' | 'not_helpful') => {
    try {
      await api.submitMentorFeedback(msgId, feedback);
      setMessages((prev) =>
        prev.map((m) => (m.id === msgId ? { ...m, feedback } : m))
      );
      addToast(feedback === 'helpful' ? 'Thank you for your feedback!' : 'Feedback noted. We will improve!', 'success');
    } catch {
      // ignore
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-5xl mx-auto">
      {/* Top Header Card */}
      <div className="bg-surface border border-border rounded-lg p-4 md:p-5 mb-4 shadow-soft shrink-0">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-primary-tint flex items-center justify-center text-primary shrink-0">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h1 className="font-serif text-xl font-bold text-ink">SkillPath AI Mentor</h1>
              <p className="text-xs text-ink-secondary">
                Always available, patient guide • Ask in English, Hindi, or Tamil
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 text-xs">
            {(user?.profile?.career_goal || user?.career_goal) ? (
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-tint text-primary font-medium">
                <Compass className="w-3.5 h-3.5" />
                Target: {user?.profile?.career_goal || user?.career_goal}
              </span>
            ) : (
              <button
                onClick={() => onNavigate('/discovery')}
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-accent-tint text-accent font-medium hover:underline"
              >
                <Compass className="w-3.5 h-3.5" />
                Find My Career Goal
              </button>
            )}

            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-bg border border-border text-ink-secondary">
              <Calendar className="w-3.5 h-3.5" />
              {user?.profile?.weekly_hours || 10} hrs/week
            </span>
          </div>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 bg-surface border border-border rounded-lg p-4 md:p-6 overflow-y-auto space-y-4 shadow-soft">
        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          return (
            <div
              key={msg.id}
              className={`flex gap-3 max-w-[85%] ${
                isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-xs font-semibold ${
                  isUser
                    ? 'bg-primary text-white'
                    : 'bg-primary-tint text-primary'
                }`}
              >
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`group relative rounded-lg p-3.5 text-sm leading-relaxed ${
                  isUser
                    ? 'bg-primary text-white rounded-br-none'
                    : 'bg-bg text-ink border border-border/80 rounded-bl-none'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Assistant message action controls */}
                {!isUser && (
                  <div className="mt-3 pt-2 border-t border-border/60 flex items-center justify-between text-xs text-ink-muted">
                    <span className="text-[11px]">
                      {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleCopy(msg.id, msg.content)}
                        className="hover:text-ink transition-colors p-1 rounded"
                        title="Copy text"
                      >
                        {copiedId === msg.id ? (
                          <Check className="w-3.5 h-3.5 text-status-success" />
                        ) : (
                          <Copy className="w-3.5 h-3.5" />
                        )}
                      </button>
                      <button
                        onClick={() => handleFeedback(msg.id, 'helpful')}
                        className={`hover:text-status-success transition-colors p-1 rounded ${
                          msg.feedback === 'helpful' ? 'text-status-success font-bold' : ''
                        }`}
                        title="Helpful"
                      >
                        <ThumbsUp className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleFeedback(msg.id, 'not_helpful')}
                        className={`hover:text-status-danger transition-colors p-1 rounded ${
                          msg.feedback === 'not_helpful' ? 'text-status-danger font-bold' : ''
                        }`}
                        title="Not helpful"
                      >
                        <ThumbsDown className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex gap-3 max-w-[85%] mr-auto">
            <div className="w-8 h-8 rounded-full bg-primary-tint text-primary flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-bg border border-border/80 rounded-lg p-3.5 text-xs text-ink-secondary flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse delay-100" />
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse delay-200" />
              <span>AI Mentor is thinking and reviewing your career context...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Starter Chips */}
      {messages.length <= 2 && (
        <div className="mt-3 overflow-x-auto pb-1 flex gap-2 shrink-0">
          {STARTER_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(prompt)}
              className="text-xs bg-surface border border-border hover:border-primary text-ink-secondary hover:text-primary px-3 py-1.5 rounded-full whitespace-nowrap transition-colors flex items-center gap-1.5 shadow-sm"
            >
              <Sparkles className="w-3 h-3 text-accent" />
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* AI Busy Visible Alert Banner */}
      {aiBusy && (
        <div className="mt-3 p-2.5 rounded-lg bg-accent-tint border border-accent/40 text-ink text-xs flex items-center justify-between shadow-soft animate-in fade-in shrink-0">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-accent shrink-0" />
            <span className="font-semibold text-accent">AI is busy, try again shortly.</span>
            <span className="text-ink-secondary text-[11px] hidden sm:inline">Offline instant guidance is currently active.</span>
          </div>
          <span className="text-[10px] text-ink-muted">Retrying...</span>
        </div>
      )}

      {/* Chat Input Bar */}
      <div className="mt-3 bg-surface border border-border rounded-lg p-2.5 shadow-soft shrink-0">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Ask anything... 'What is SQL?', 'How do I start Python?', 'Am I on track?'"
            className="flex-1 bg-transparent px-3 py-2 text-sm text-ink placeholder:text-ink-muted focus:outline-none"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!inputText.trim() || loading}
            className="bg-primary hover:bg-primary-hover disabled:opacity-50 text-white px-4 py-2 rounded-md font-medium text-sm flex items-center gap-1.5 transition-colors"
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Send</span>
          </button>
        </form>
      </div>
    </div>
  );
};
