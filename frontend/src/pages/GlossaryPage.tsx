import React, { useState, useEffect } from 'react';
import {
  BookMarked,
  Search,
  Tag,
  Copy,
  Check,
  Sparkles,
  HelpCircle,
  Lightbulb
} from 'lucide-react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';

interface GlossaryItem {
  id: number;
  term: string;
  category: string;
  plain_meaning: string;
  example: string;
}

const CATEGORIES = [
  'All',
  'AI & Data',
  'Web Development',
  'Cloud & DevOps',
  'Core Tech',
  'Testing & QA'
];

export const GlossaryPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { addToast } = useToast();
  const [items, setItems] = useState<GlossaryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [copiedId, setCopiedId] = useState<number | null>(null);

  useEffect(() => {
    loadGlossary();
  }, []);

  const loadGlossary = async () => {
    try {
      setLoading(true);
      const res = await api.getGlossary();
      setItems(res || []);
    } catch {
      // Fallback seed terms for offline robustness
      setItems([
        {
          id: 1,
          term: 'API (Application Programming Interface)',
          category: 'Web Development',
          plain_meaning: 'A digital waiter. Just as a waiter takes your order to the kitchen and brings your food back, an API takes your request to a server and brings back the data.',
          example: 'When a weather app shows current temperature, it calls a weather API to fetch it.'
        },
        {
          id: 2,
          term: 'Machine Learning',
          category: 'AI & Data',
          plain_meaning: 'Teaching a computer to recognize patterns from examples instead of writing rigid rules for every possible situation.',
          example: 'Showing a computer 10,000 photos of cats until it learns to identify a cat on its own.'
        },
        {
          id: 3,
          term: 'SQL (Structured Query Language)',
          category: 'AI & Data',
          plain_meaning: 'The universal language used to ask questions to a database (like filtering, sorting, and counting rows in a giant spreadsheet).',
          example: 'SELECT name FROM students WHERE marks > 80;'
        },
        {
          id: 4,
          term: 'Docker & Containers',
          category: 'Cloud & DevOps',
          plain_meaning: 'A lightweight lunchbox that packages your application and everything it needs so it runs identically on any computer or cloud server.',
          example: 'Eliminates the common excuse "it works on my machine!"'
        },
        {
          id: 5,
          term: 'Git & Version Control',
          category: 'Core Tech',
          plain_meaning: 'A time machine for your code that saves snapshots of your work so you can undo mistakes or collaborate with a team safely.',
          example: 'git commit -m "Added login button"'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (item: GlossaryItem) => {
    navigator.clipboard.writeText(`${item.term}: ${item.plain_meaning}\nExample: ${item.example}`);
    setCopiedId(item.id);
    addToast('Glossary definition copied!', 'info');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.term.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.plain_meaning.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.example && item.example.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesCategory =
      selectedCategory === 'All' ||
      item.category.toLowerCase().includes(selectedCategory.toLowerCase()) ||
      (selectedCategory === 'AI & Data' && (item.category.includes('AI') || item.category.includes('Data')));

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-primary-tint text-primary uppercase tracking-wider">
            Beginner-First Glossary
          </span>
        </div>
        <h1 className="font-serif text-2xl md:text-3xl font-bold text-ink">
          Plain-Language Tech Dictionary
        </h1>
        <p className="text-sm text-ink-secondary mt-1">
          Every technical term explained at a grade-8 reading level with simple everyday analogies. No unexplained acronyms.
        </p>
      </div>

      {/* Search and Category Filter Bar */}
      <div className="bg-surface border border-border rounded-lg p-4 shadow-soft space-y-3">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-ink-muted" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search any term (e.g., API, Neural Network, CI/CD, React, Cache, Docker)..."
            className="w-full bg-bg border border-border rounded-md pl-9 pr-4 py-2 text-sm text-ink focus:outline-none focus:border-primary placeholder:text-ink-muted"
          />
        </div>

        {/* Category Pills */}
        <div className="flex flex-wrap gap-1.5 pt-1">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                selectedCategory === cat
                  ? 'bg-primary text-white font-semibold shadow-xs'
                  : 'bg-bg text-ink-secondary hover:text-ink hover:bg-border/40'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Terms Count Bar */}
      <div className="flex items-center justify-between text-xs text-ink-muted px-1">
        <span>
          Showing {filteredItems.length} of {items.length} plain-language definitions
        </span>
        <span>Tap any card to copy meaning</span>
      </div>

      {/* Grid of Glossary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredItems.map((item) => (
          <div
            key={item.id}
            className="bg-surface border border-border hover:border-primary/50 transition-all rounded-lg p-5 shadow-soft flex flex-col justify-between group"
          >
            <div>
              <div className="flex items-start justify-between gap-3 mb-2">
                <h3 className="font-serif text-base font-bold text-ink group-hover:text-primary transition-colors">
                  {item.term}
                </h3>
                <span className="shrink-0 text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-bg text-ink-muted border border-border">
                  {item.category}
                </span>
              </div>

              <div className="text-sm text-ink leading-relaxed mb-3">
                {item.plain_meaning}
              </div>

              {item.example && (
                <div className="bg-bg border-l-2 border-primary/50 p-2.5 rounded-r text-xs text-ink-secondary mt-2 flex items-start gap-2">
                  <Lightbulb className="w-3.5 h-3.5 text-accent shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-ink">Example / In Practice: </span>
                    <span>{item.example}</span>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-4 pt-3 border-t border-border/50 flex items-center justify-end">
              <button
                onClick={() => handleCopy(item)}
                className="text-xs text-ink-muted hover:text-ink flex items-center gap-1.5 transition-colors p-1"
                title="Copy definition"
              >
                {copiedId === item.id ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-status-success" />
                    <span className="text-status-success font-medium">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span>Copy</span>
                  </>
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredItems.length === 0 && !loading && (
        <div className="bg-surface border border-border rounded-lg p-12 text-center shadow-soft">
          <HelpCircle className="w-10 h-10 text-ink-muted mx-auto mb-3" />
          <h3 className="font-serif text-lg font-bold text-ink mb-1">No matching terms found</h3>
          <p className="text-xs text-ink-secondary max-w-sm mx-auto mb-4">
            Try a different search term or ask your AI Mentor to explain this concept in simple words.
          </p>
          <button
            onClick={() => onNavigate('/mentor')}
            className="inline-flex items-center gap-2 bg-primary text-white text-xs font-semibold px-4 py-2 rounded-md hover:bg-primary-hover transition-colors"
          >
            <span>Ask AI Mentor to explain</span>
          </button>
        </div>
      )}
    </div>
  );
};

