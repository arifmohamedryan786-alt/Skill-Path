import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import {
  PracticeCategory,
  PracticeQuestionSummary,
  PracticeQuestionDetail,
  PracticeStats
} from '../types';
import {
  Code2,
  Terminal,
  Coffee,
  Network,
  Cpu,
  CheckCircle2,
  Clock,
  Circle,
  Lightbulb,
  ArrowRight,
  ArrowLeft,
  ChevronDown,
  ChevronUp,
  Save,
  Check,
  Search,
  Filter,
  Sparkles,
  BookOpen,
  Copy,
  Flame,
  Award,
  Layers,
  HelpCircle,
  X
} from 'lucide-react';

const CATEGORY_ICONS: Record<string, React.ElementType> = {
  'c-programming': Terminal,
  'python': Code2,
  'java': Coffee,
  'data-structures': Network,
  'dsa': Cpu,
};

export const PracticeQuestionsPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();

  // Data states
  const [categories, setCategories] = useState<PracticeCategory[]>([]);
  const [questions, setQuestions] = useState<PracticeQuestionSummary[]>([]);
  const [stats, setStats] = useState<PracticeStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Filter states
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [selectedStatus, setSelectedStatus] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Practice modal/workspace view state
  const [activeQuestionId, setActiveQuestionId] = useState<number | null>(null);
  const [activeQuestion, setActiveQuestion] = useState<PracticeQuestionDetail | null>(null);
  const [questionLoading, setQuestionLoading] = useState<boolean>(false);
  const [showHint, setShowHint] = useState<boolean>(false);
  const [showSolution, setShowSolution] = useState<boolean>(false);
  const [workspaceCode, setWorkspaceCode] = useState<string>('');
  const [savingCode, setSavingCode] = useState<boolean>(false);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('python');
  const [copiedSolution, setCopiedSolution] = useState<boolean>(false);

  // Load categories and stats on mount
  useEffect(() => {
    loadInitialData();
  }, []);

  // Reload questions whenever filters change
  useEffect(() => {
    loadQuestions();
  }, [selectedCategory, selectedDifficulty, selectedStatus]);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [catsRes, statsRes] = await Promise.all([
        api.getPracticeCategories(),
        api.getPracticeStats()
      ]);
      setCategories(catsRes);
      setStats(statsRes);
    } catch (err: any) {
      showToast(err.message || 'Failed to load practice data', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadQuestions = async () => {
    try {
      const qs = await api.getPracticeQuestions({
        category: selectedCategory,
        difficulty: selectedDifficulty,
        status: selectedStatus
      });
      setQuestions(qs);
    } catch (err: any) {
      showToast('Could not filter practice questions', 'error');
    }
  };

  // Open Question Practice Experience
  const openQuestion = async (id: number) => {
    setActiveQuestionId(id);
    setQuestionLoading(true);
    setShowHint(false);
    setShowSolution(false);
    setCopiedSolution(false);

    try {
      const q = await api.getQuestionDetail(id);
      setActiveQuestion(q);
      setWorkspaceCode(q.user_solution_code || q.starter_code || '');

      // Set default language according to category
      if (q.category_slug === 'c-programming') setSelectedLanguage('c');
      else if (q.category_slug === 'java') setSelectedLanguage('java');
      else setSelectedLanguage('python');
    } catch (err: any) {
      showToast('Failed to load question details', 'error');
      setActiveQuestionId(null);
    } finally {
      setQuestionLoading(false);
    }
  };

  // Close Question Workspace
  const closeQuestion = () => {
    setActiveQuestionId(null);
    setActiveQuestion(null);
    // Refresh stats & question list
    loadInitialData();
    loadQuestions();
  };

  // Save code to backend
  const handleSaveCode = async () => {
    if (!activeQuestion) return;
    setSavingCode(true);
    try {
      await api.updateQuestionProgress(activeQuestion.id, {
        status: activeQuestion.user_status === 'completed' ? 'completed' : 'attempted',
        solution_code: workspaceCode
      });
      setActiveQuestion(prev => prev ? {
        ...prev,
        user_solution_code: workspaceCode,
        user_status: prev.user_status === 'completed' ? 'completed' : 'attempted'
      } : null);
      showToast('Solution code saved to Practice Workspace!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Failed to save code', 'error');
    } finally {
      setSavingCode(false);
    }
  };

  // Mark as completed
  const handleToggleComplete = async () => {
    if (!activeQuestion) return;
    const newStatus = activeQuestion.user_status === 'completed' ? 'attempted' : 'completed';
    try {
      await api.updateQuestionProgress(activeQuestion.id, {
        status: newStatus,
        solution_code: workspaceCode
      });

      setActiveQuestion(prev => prev ? {
        ...prev,
        user_status: newStatus,
        completed_at: newStatus === 'completed' ? 'Just now' : null
      } : null);

      if (newStatus === 'completed') {
        showToast(`🎉 Marked "${activeQuestion.title}" as Completed!`, 'success');
      } else {
        showToast('Question reset to In Progress', 'info');
      }

      // Refresh background stats
      loadInitialData();
    } catch (err: any) {
      showToast(err.message || 'Failed to update completion status', 'error');
    }
  };

  // Copy solution code
  const handleCopySolution = () => {
    if (!activeQuestion?.solution) return;
    navigator.clipboard.writeText(activeQuestion.solution);
    setCopiedSolution(true);
    showToast('Solution code copied to clipboard!', 'info');
    setTimeout(() => setCopiedSolution(false), 2500);
  };

  // Filtered list by search query
  const filteredQuestions = questions.filter(q => {
    if (!searchQuery.trim()) return true;
    const match = searchQuery.toLowerCase();
    return q.title.toLowerCase().includes(match) || q.description.toLowerCase().includes(match);
  });

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-status-success-tint text-status-success border border-status-success/30">
            <span className="w-1.5 h-1.5 rounded-full bg-status-success" />
            Beginner
          </span>
        );
      case 'Intermediate':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-status-warning-tint text-status-warning border border-status-warning/30">
            <span className="w-1.5 h-1.5 rounded-full bg-status-warning" />
            Intermediate
          </span>
        );
      case 'Advanced':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-status-danger-tint text-status-danger border border-status-danger/30">
            <span className="w-1.5 h-1.5 rounded-full bg-status-danger" />
            Advanced
          </span>
        );
      default:
        return null;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold text-status-success bg-status-success-tint">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Completed
          </span>
        );
      case 'attempted':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold text-status-warning bg-status-warning-tint">
            <Clock className="w-3.5 h-3.5" />
            In Progress
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium text-ink-muted bg-bg">
            <Circle className="w-3 h-3 text-ink-muted" />
            Not Started
          </span>
        );
    }
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Page Title & Subtitle */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-5">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-primary-tint/60 text-primary text-xs font-semibold mb-2">
            <Code2 className="w-3.5 h-3.5" />
            <span>Interactive Problem-Solving Bank</span>
          </div>
          <h1 className="font-serif text-3xl font-bold text-ink">Practice Questions</h1>
          <p className="text-sm text-ink-secondary mt-1">
            Strengthen your programming skills through hands-on practice.
          </p>
        </div>

        {/* Mentor Quick Link */}
        <button
          type="button"
          onClick={() => onNavigate('/mentor')}
          className="inline-flex items-center gap-2 px-4 py-2 bg-surface border border-border rounded-lg text-xs font-semibold text-ink hover:border-primary hover:text-primary transition-colors shadow-xs"
        >
          <Sparkles className="w-4 h-4 text-accent" />
          <span>Ask AI Mentor for Practice Tips</span>
        </button>
      </div>

      {/* Progress Summary Card */}
      {stats && (
        <div className="bg-surface border border-border rounded-xl p-6 shadow-card space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div className="text-xs font-semibold text-ink-muted uppercase tracking-wider">
                Practice Progress
              </div>
              <div className="flex items-baseline gap-3 mt-1">
                <span className="font-serif text-3xl font-bold text-ink">
                  {stats.total_completed}
                </span>
                <span className="text-sm text-ink-secondary font-medium">
                  of {stats.total_questions} Questions Completed
                </span>
                <span className="text-xs font-semibold text-primary bg-primary-tint/60 px-2 py-0.5 rounded-full">
                  {stats.completion_pct}% Mastered
                </span>
              </div>
            </div>

            {/* Streak & Velocity */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-accent/15 border border-accent/30 text-ink">
                <Flame className="w-4 h-4 text-accent fill-accent" />
                <span className="text-xs font-bold">{stats.current_streak} Day Practice Streak</span>
              </div>
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-primary-tint/40 border border-primary/20 text-ink">
                <Award className="w-4 h-4 text-primary" />
                <span className="text-xs font-semibold">{stats.total_attempted} Attempted</span>
              </div>
            </div>
          </div>

          {/* Overall Progress Bar */}
          <div className="w-full bg-bg rounded-full h-2.5 overflow-hidden border border-border/60">
            <div
              className="bg-primary h-full transition-all duration-500 rounded-full"
              style={{ width: `${Math.max(stats.completion_pct, 2)}%` }}
            />
          </div>

          {/* Category-Wise Progress Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 pt-2">
            {Object.entries(stats.by_category).map(([catName, cData]) => (
              <div
                key={catName}
                onClick={() => setSelectedCategory(cData.slug)}
                className={`p-3 rounded-lg border text-left cursor-pointer transition-all ${
                  selectedCategory === cData.slug
                    ? 'border-primary bg-primary-tint/30 shadow-xs'
                    : 'border-border bg-bg/50 hover:border-primary/50'
                }`}
              >
                <div className="text-[11px] font-semibold text-ink-secondary truncate">{catName}</div>
                <div className="flex items-baseline justify-between mt-1">
                  <span className="text-sm font-bold text-ink">{cData.completed} / {cData.total}</span>
                  <span className="text-[10px] font-semibold text-ink-muted">{cData.pct}%</span>
                </div>
                <div className="w-full bg-border/60 rounded-full h-1 mt-1.5 overflow-hidden">
                  <div
                    className="bg-primary h-full rounded-full"
                    style={{ width: `${cData.pct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 5 Interactive Category Cards */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="font-serif text-xl font-bold text-ink">Categories</h2>
            <p className="text-xs text-ink-secondary">Select a track to start focused problem-solving.</p>
          </div>
          {selectedCategory !== 'all' && (
            <button
              onClick={() => setSelectedCategory('all')}
              className="text-xs font-semibold text-primary hover:underline"
            >
              Show All Categories
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {categories.map((cat) => {
            const IconComponent = CATEGORY_ICONS[cat.slug] || Code2;
            const isSelected = selectedCategory === cat.slug;

            return (
              <div
                key={cat.id}
                className={`bg-surface border rounded-xl p-5 shadow-card flex flex-col justify-between transition-all ${
                  isSelected ? 'border-primary ring-2 ring-primary/20' : 'border-border hover:border-primary/50'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-10 h-10 rounded-lg bg-primary-tint flex items-center justify-center text-primary">
                      <IconComponent className="w-5 h-5" />
                    </div>
                    <span className="text-xs font-semibold text-ink bg-bg px-2.5 py-1 rounded-md border border-border/80">
                      {cat.total_questions} Questions
                    </span>
                  </div>

                  <h3 className="font-serif text-base font-bold text-ink mb-1">{cat.name}</h3>
                  <p className="text-xs text-ink-secondary leading-relaxed line-clamp-3 mb-4">
                    {cat.description}
                  </p>
                </div>

                <div className="space-y-4 pt-3 border-t border-border/60">
                  {/* Difficulty Breakdown Badges */}
                  <div className="flex items-center gap-1.5 text-[10px] text-ink-secondary">
                    <span className="font-medium">Levels:</span>
                    <span className="text-status-success font-semibold">🟢 {cat.beginner_count}</span>
                    <span className="text-status-warning font-semibold">🟡 {cat.intermediate_count}</span>
                    <span className="text-status-danger font-semibold">🔴 {cat.advanced_count}</span>
                  </div>

                  {/* Progress Meter */}
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="text-ink-secondary font-medium">Completed:</span>
                      <span className="font-bold text-ink">{cat.completed_questions} / {cat.total_questions}</span>
                    </div>
                    <div className="w-full bg-bg rounded-full h-1.5 overflow-hidden border border-border/60">
                      <div
                        className="bg-primary h-full rounded-full transition-all"
                        style={{ width: `${(cat.completed_questions / Math.max(cat.total_questions, 1)) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex items-center gap-2 pt-1">
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedCategory(cat.slug);
                        // Find first uncompleted question in this category
                        const firstUnsolved = questions.find(
                          q => q.category_slug === cat.slug && q.user_status !== 'completed'
                        );
                        if (firstUnsolved) {
                          openQuestion(firstUnsolved.id);
                        } else {
                          const firstInCat = questions.find(q => q.category_slug === cat.slug);
                          if (firstInCat) openQuestion(firstInCat.id);
                        }
                      }}
                      className="flex-1 py-2 px-3 bg-primary text-white text-xs font-semibold rounded-lg hover:bg-primary-hover transition-colors shadow-soft flex items-center justify-center gap-1.5 cursor-pointer"
                    >
                      <span>Start Practice</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>

                    <button
                      type="button"
                      onClick={() => setSelectedCategory(cat.slug)}
                      className={`px-3 py-2 text-xs font-semibold rounded-lg border transition-colors ${
                        isSelected
                          ? 'border-primary text-primary bg-primary-tint/30'
                          : 'border-border text-ink-secondary hover:text-ink hover:bg-bg'
                      }`}
                    >
                      Filter
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-surface border border-border rounded-xl p-4 shadow-card space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          {/* Search Input */}
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 text-ink-muted absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search questions by topic (e.g. reverse, prime, binary search)..."
              className="w-full text-xs pl-9 pr-3 py-2 border border-border rounded-lg bg-bg text-ink focus:outline-none focus:border-primary"
            />
          </div>

          {/* Filter Dropdowns */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              aria-label="Filter by Category"
              className="text-xs px-2.5 py-2 border border-border rounded-lg bg-bg text-ink focus:outline-none focus:border-primary cursor-pointer font-medium"
            >
              <option value="all">All Categories</option>
              <option value="c-programming">C Programming</option>
              <option value="python">Python</option>
              <option value="java">Java</option>
              <option value="data-structures">Data Structures</option>
              <option value="dsa">DSA</option>
            </select>

            {/* Difficulty Filter */}
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              aria-label="Filter by Difficulty"
              className="text-xs px-2.5 py-2 border border-border rounded-lg bg-bg text-ink focus:outline-none focus:border-primary cursor-pointer font-medium"
            >
              <option value="all">All Difficulties</option>
              <option value="Beginner">🟢 Beginner</option>
              <option value="Intermediate">🟡 Intermediate</option>
              <option value="Advanced">🔴 Advanced</option>
            </select>

            {/* Status Filter */}
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              aria-label="Filter by Completion Status"
              className="text-xs px-2.5 py-2 border border-border rounded-lg bg-bg text-ink focus:outline-none focus:border-primary cursor-pointer font-medium"
            >
              <option value="all">All Statuses</option>
              <option value="completed">Completed</option>
              <option value="attempted">In Progress</option>
              <option value="uncompleted">Uncompleted</option>
            </select>
          </div>
        </div>

        {/* Results Counter */}
        <div className="flex items-center justify-between text-xs text-ink-secondary pt-1 border-t border-border/50">
          <span>Showing {filteredQuestions.length} practice problems</span>
          {(selectedCategory !== 'all' || selectedDifficulty !== 'all' || selectedStatus !== 'all' || searchQuery) && (
            <button
              onClick={() => {
                setSelectedCategory('all');
                setSelectedDifficulty('all');
                setSelectedStatus('all');
                setSearchQuery('');
              }}
              className="text-primary hover:underline font-semibold"
            >
              Clear all filters
            </button>
          )}
        </div>
      </div>

      {/* Questions List */}
      <div className="space-y-3">
        {filteredQuestions.map((q) => (
          <div
            key={q.id}
            onClick={() => openQuestion(q.id)}
            className="p-4 bg-surface border border-border rounded-xl hover:border-primary/60 hover:shadow-soft transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
          >
            <div className="space-y-1.5 flex-1 pr-4">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[11px] font-semibold text-primary bg-primary-tint/60 px-2 py-0.5 rounded">
                  {q.category}
                </span>
                {getDifficultyBadge(q.difficulty)}
                {getStatusBadge(q.user_status)}
              </div>
              <h4 className="font-serif font-bold text-sm text-ink group-hover:text-primary transition-colors">
                {q.order_index}. {q.title}
              </h4>
              <p className="text-xs text-ink-secondary line-clamp-2 leading-relaxed">
                {q.description}
              </p>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              {q.has_saved_code && (
                <span className="text-[11px] text-accent font-medium flex items-center gap-1 bg-accent/10 px-2 py-1 rounded">
                  <Save className="w-3 h-3" /> Code Saved
                </span>
              )}
              <button
                type="button"
                className="py-1.5 px-3 bg-bg border border-border group-hover:border-primary group-hover:bg-primary-tint/30 text-ink text-xs font-semibold rounded-lg transition-colors flex items-center gap-1.5"
              >
                <span>{q.user_status === 'completed' ? 'Review Solution' : 'Solve Problem'}</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </button>
            </div>
          </div>
        ))}

        {filteredQuestions.length === 0 && (
          <div className="p-8 text-center bg-surface border border-border rounded-xl">
            <HelpCircle className="w-8 h-8 text-ink-muted mx-auto mb-2" />
            <h4 className="font-serif font-bold text-sm text-ink">No questions found</h4>
            <p className="text-xs text-ink-secondary mt-1">
              Try adjusting your category, difficulty, or status filter.
            </p>
          </div>
        )}
      </div>

      {/* ===================================================================== */}
      {/* Question Experience (Workspace & Solution Modal) */}
      {/* ===================================================================== */}
      {activeQuestionId && activeQuestion && (
        <div className="fixed inset-0 bg-ink/40 backdrop-blur-xs z-50 flex items-center justify-center p-3 sm:p-6 overflow-y-auto">
          <div className="bg-surface border border-border rounded-2xl w-full max-w-4xl shadow-2xl max-h-[92vh] flex flex-col overflow-hidden animate-in fade-in duration-200">
            {/* Modal Header */}
            <div className="p-5 border-b border-border flex items-center justify-between bg-primary-tint/20 shrink-0">
              <div className="flex items-center gap-3">
                <span className="text-xs font-semibold text-primary bg-primary-tint px-2.5 py-1 rounded-md">
                  {activeQuestion.category}
                </span>
                {getDifficultyBadge(activeQuestion.difficulty)}
                {getStatusBadge(activeQuestion.user_status)}
              </div>

              <div className="flex items-center gap-2">
                {/* Previous & Next question buttons */}
                {activeQuestion.prev_question_id && (
                  <button
                    type="button"
                    onClick={() => openQuestion(activeQuestion.prev_question_id!)}
                    className="p-1.5 rounded-lg border border-border text-ink-secondary hover:text-ink hover:bg-bg"
                    title="Previous Question"
                  >
                    <ArrowLeft className="w-4 h-4" />
                  </button>
                )}
                {activeQuestion.next_question_id && (
                  <button
                    type="button"
                    onClick={() => openQuestion(activeQuestion.next_question_id!)}
                    className="p-1.5 rounded-lg border border-border text-ink-secondary hover:text-ink hover:bg-bg"
                    title="Next Question"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </button>
                )}
                <button
                  type="button"
                  onClick={closeQuestion}
                  className="p-1.5 rounded-lg border border-border text-ink-secondary hover:text-ink hover:bg-bg ml-2"
                  title="Close Workspace"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Modal Body: Scrollable Question & Practice Workspace */}
            <div className="p-6 overflow-y-auto space-y-6 flex-1 text-ink">
              {/* Question Title & Description */}
              <div>
                <h2 className="font-serif text-2xl font-bold text-ink mb-2">
                  {activeQuestion.order_index}. {activeQuestion.title}
                </h2>
                <div className="text-sm text-ink leading-relaxed whitespace-pre-line bg-bg p-4 rounded-xl border border-border/80">
                  {activeQuestion.description}
                </div>
              </div>

              {/* Example Input / Output */}
              {(activeQuestion.example_input || activeQuestion.example_output) && (
                <div className="grid sm:grid-cols-2 gap-3">
                  {activeQuestion.example_input && (
                    <div className="p-3 bg-bg rounded-lg border border-border">
                      <div className="text-[11px] font-semibold text-ink-muted uppercase tracking-wider mb-1">
                        Example Input
                      </div>
                      <code className="text-xs font-mono text-ink font-medium break-all">
                        {activeQuestion.example_input}
                      </code>
                    </div>
                  )}
                  {activeQuestion.example_output && (
                    <div className="p-3 bg-bg rounded-lg border border-border">
                      <div className="text-[11px] font-semibold text-ink-muted uppercase tracking-wider mb-1">
                        Expected Output
                      </div>
                      <code className="text-xs font-mono text-primary font-medium break-all">
                        {activeQuestion.example_output}
                      </code>
                    </div>
                  )}
                </div>
              )}

              {/* Helpful Hint Button & Disclosure */}
              {activeQuestion.hint && (
                <div className="border border-accent/30 rounded-xl overflow-hidden bg-accent/5">
                  <button
                    type="button"
                    onClick={() => setShowHint(!showHint)}
                    className="w-full p-3.5 flex items-center justify-between text-left text-xs font-semibold text-ink hover:bg-accent/10 transition-colors"
                  >
                    <div className="flex items-center gap-2 text-accent">
                      <Lightbulb className="w-4 h-4" />
                      <span>Need a hint? Click here</span>
                    </div>
                    {showHint ? <ChevronUp className="w-4 h-4 text-ink-muted" /> : <ChevronDown className="w-4 h-4 text-ink-muted" />}
                  </button>
                  {showHint && (
                    <div className="p-4 pt-1 text-xs text-ink-secondary leading-relaxed border-t border-accent/20">
                      💡 {activeQuestion.hint}
                    </div>
                  )}
                </div>
              )}

              {/* Practice Workspace (Code Area) */}
              <div className="border border-border rounded-xl overflow-hidden bg-surface shadow-xs">
                <div className="p-3 bg-bg border-b border-border flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="font-serif text-xs font-bold text-ink">Practice Workspace</span>
                    <span className="text-[11px] text-ink-muted hidden sm:inline">• Save your working solution</span>
                  </div>

                  <div className="flex items-center gap-2">
                    {/* Language Selector */}
                    <select
                      value={selectedLanguage}
                      onChange={(e) => setSelectedLanguage(e.target.value)}
                      aria-label="Workspace Programming Language"
                      className="text-[11px] font-medium px-2 py-1 bg-surface border border-border rounded text-ink focus:outline-none"
                    >
                      <option value="python">Python</option>
                      <option value="c">C</option>
                      <option value="java">Java</option>
                    </select>

                    {/* Save Code Button */}
                    <button
                      type="button"
                      onClick={handleSaveCode}
                      disabled={savingCode}
                      className="inline-flex items-center gap-1.5 px-3 py-1 bg-surface border border-border hover:border-primary text-xs font-semibold rounded text-ink transition-colors cursor-pointer disabled:opacity-60"
                    >
                      <Save className="w-3.5 h-3.5 text-primary" />
                      <span>{savingCode ? 'Saving...' : 'Save Code'}</span>
                    </button>
                  </div>
                </div>

                {/* Code Textarea */}
                <div className="relative">
                  <textarea
                    value={workspaceCode}
                    onChange={(e) => setWorkspaceCode(e.target.value)}
                    placeholder="// Write your solution code here..."
                    rows={12}
                    className="w-full p-4 font-mono text-xs bg-bg/40 text-ink leading-relaxed focus:outline-none resize-y selection:bg-primary-tint"
                    spellCheck={false}
                  />
                </div>
                <div className="px-4 py-2 bg-bg/80 border-t border-border/60 text-[11px] text-ink-muted flex items-center justify-between">
                  <span>Press Save Code to store your draft in your personalized passport database.</span>
                  <span>{workspaceCode.length} characters</span>
                </div>
              </div>

              {/* Action Buttons: Mark as Completed & Show Solution */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleToggleComplete}
                  className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-semibold shadow-soft cursor-pointer transition-all ${
                    activeQuestion.user_status === 'completed'
                      ? 'bg-status-success text-white hover:bg-status-success/90'
                      : 'bg-primary text-white hover:bg-primary-hover'
                  }`}
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>
                    {activeQuestion.user_status === 'completed' ? 'Completed (Click to Reset)' : 'Mark as Completed'}
                  </span>
                </button>

                {/* Show Solution Button */}
                <button
                  type="button"
                  onClick={() => setShowSolution(!showSolution)}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs font-semibold border border-border bg-surface hover:border-primary text-ink transition-colors cursor-pointer"
                >
                  <BookOpen className="w-4 h-4 text-primary" />
                  <span>{showSolution ? 'Hide Solution & Approach' : 'Show Solution & Approach'}</span>
                  {showSolution ? <ChevronUp className="w-3.5 h-3.5 text-ink-muted" /> : <ChevronDown className="w-3.5 h-3.5 text-ink-muted" />}
                </button>
              </div>

              {/* Expandable Solution Section */}
              {showSolution && (
                <div className="border border-primary/30 rounded-xl bg-primary-tint/10 p-5 space-y-4 animate-in fade-in duration-200">
                  <div className="flex items-center justify-between border-b border-primary/20 pb-3">
                    <h3 className="font-serif font-bold text-base text-ink flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-primary" />
                      <span>Reference Solution & Complexity Analysis</span>
                    </h3>

                    {/* Complexity Badges */}
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 rounded bg-surface border border-border text-[11px] font-mono text-ink">
                        Time: <strong>{activeQuestion.time_complexity}</strong>
                      </span>
                      <span className="px-2 py-0.5 rounded bg-surface border border-border text-[11px] font-mono text-ink">
                        Space: <strong>{activeQuestion.space_complexity}</strong>
                      </span>
                    </div>
                  </div>

                  {/* Approach */}
                  {activeQuestion.approach && (
                    <div>
                      <h4 className="text-xs font-bold text-ink uppercase tracking-wider mb-1">
                        Approach
                      </h4>
                      <p className="text-xs text-ink-secondary leading-relaxed whitespace-pre-line">
                        {activeQuestion.approach}
                      </p>
                    </div>
                  )}

                  {/* Explanation */}
                  {activeQuestion.explanation && (
                    <div>
                      <h4 className="text-xs font-bold text-ink uppercase tracking-wider mb-1">
                        Deep Explanation
                      </h4>
                      <p className="text-xs text-ink-secondary leading-relaxed whitespace-pre-line">
                        {activeQuestion.explanation}
                      </p>
                    </div>
                  )}

                  {/* Example Solution Code */}
                  {activeQuestion.solution && (
                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <h4 className="text-xs font-bold text-ink uppercase tracking-wider">
                          Solution Code
                        </h4>
                        <button
                          type="button"
                          onClick={handleCopySolution}
                          className="text-[11px] font-semibold text-primary hover:underline flex items-center gap-1 cursor-pointer"
                        >
                          {copiedSolution ? <Check className="w-3 h-3 text-status-success" /> : <Copy className="w-3 h-3" />}
                          <span>{copiedSolution ? 'Copied!' : 'Copy Code'}</span>
                        </button>
                      </div>
                      <pre className="p-4 bg-ink text-white rounded-lg text-xs font-mono overflow-x-auto leading-relaxed">
                        <code>{activeQuestion.solution}</code>
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-border bg-bg/50 flex items-center justify-between text-xs text-ink-secondary shrink-0">
              <span>SkillPath Practice Engine • College Curriculum Verified</span>
              <button
                type="button"
                onClick={closeQuestion}
                className="px-3 py-1.5 bg-surface border border-border rounded-lg text-ink font-semibold hover:bg-bg transition-colors cursor-pointer"
              >
                Back to Questions
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

