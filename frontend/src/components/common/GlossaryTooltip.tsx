import React, { useState } from 'react';
import { useGlossary } from '../../context/GlossaryContext';
import { HelpCircle } from 'lucide-react';

interface GlossaryTooltipProps {
  term: string;
  children?: React.ReactNode;
}

export const GlossaryTooltip: React.FC<GlossaryTooltipProps> = ({ term, children }) => {
  const { getTerm } = useGlossary();
  const [isOpen, setIsOpen] = useState(false);
  const info = getTerm(term);

  if (!info) {
    return <>{children || term}</>;
  }

  return (
    <span
      className="relative inline-block"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
      onClick={() => setIsOpen(!isOpen)}
    >
      <span className="cursor-help border-b border-dotted border-primary text-ink hover:text-primary transition-colors font-medium">
        {children || term}
      </span>
      {isOpen && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-3 bg-surface border border-border rounded-md shadow-card text-xs text-ink z-50 text-left pointer-events-none animate-in fade-in zoom-in-95 duration-150">
          <span className="block font-semibold text-primary mb-1 flex items-center gap-1.5">
            <HelpCircle className="w-3.5 h-3.5" />
            {info.term}
          </span>
          <span className="block text-ink-secondary leading-relaxed mb-1.5">
            {info.plain_meaning}
          </span>
          {info.example && (
            <span className="block text-[11px] text-ink-muted italic border-t border-border/60 pt-1">
              Example: {info.example}
            </span>
          )}
          <span className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-surface" />
        </span>
      )}
    </span>
  );
};

