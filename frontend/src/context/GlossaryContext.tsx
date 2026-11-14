import React, { createContext, useContext, useState, useEffect } from 'react';
import { GlossaryItem } from '../types';
import { api } from '../api/client';

interface GlossaryContextType {
  termsMap: Record<string, GlossaryItem>;
  getTerm: (term: string) => GlossaryItem | undefined;
}

const GlossaryContext = createContext<GlossaryContextType | undefined>(undefined);

export const GlossaryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [termsMap, setTermsMap] = useState<Record<string, GlossaryItem>>({});

  useEffect(() => {
    async function loadGlossary() {
      try {
        const items: GlossaryItem[] = await api.getGlossary();
        const map: Record<string, GlossaryItem> = {};
        for (const it of items) {
          map[it.term.toLowerCase()] = it;
        }
        setTermsMap(map);
      } catch (err) {
        // ignore
      }
    }
    loadGlossary();
  }, []);

  const getTerm = (term: string) => {
    return termsMap[term.toLowerCase()];
  };

  return (
    <GlossaryContext.Provider value={{ termsMap, getTerm }}>
      {children}
    </GlossaryContext.Provider>
  );
};

export function useGlossary() {
  const context = useContext(GlossaryContext);
  if (!context) throw new Error('useGlossary must be used within a GlossaryProvider');
  return context;
}

