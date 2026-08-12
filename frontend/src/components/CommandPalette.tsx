import React, { useState } from 'react';
import { Search, Code, Globe, Music, Calculator, Activity, X } from 'lucide-react';
import { launchDesktopApp } from '../services/api';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTab: (tab: string) => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({ isOpen, onClose, onSelectTab }) => {
  const [query, setQuery] = useState('');

  if (!isOpen) return null;

  const actions = [
    { id: 'vscode', title: 'Launch VS Code Desktop', category: 'App Launcher', icon: Code, action: () => launchDesktopApp('vscode') },
    { id: 'chrome', title: 'Launch Google Chrome Browser', category: 'App Launcher', icon: Globe, action: () => launchDesktopApp('chrome') },
    { id: 'spotify', title: 'Launch Spotify Desktop', category: 'App Launcher', icon: Music, action: () => launchDesktopApp('spotify') },
    { id: 'calc', title: 'Launch Calculator', category: 'App Launcher', icon: Calculator, action: () => launchDesktopApp('calc') },
    { id: 'rag', title: 'Open Hybrid FAISS+BM25 RAG', category: 'Navigation', icon: Search, action: () => onSelectTab('rag') },
    { id: 'productivity', title: 'Open Productivity Notes & To-dos', category: 'Navigation', icon: Activity, action: () => onSelectTab('productivity') },
  ];

  const filtered = actions.filter((a) => a.title.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex items-start justify-center pt-24 px-4">
      <div className="glass-panel w-full max-w-xl border-sky-500/40 shadow-2xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center gap-3">
          <Search className="w-5 h-5 text-sky-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command or search action (Raycast Cmd+K)..."
            className="flex-1 bg-transparent border-none text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
            autoFocus
          />
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-100">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="max-h-80 overflow-y-auto p-2 space-y-1">
          {filtered.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={async () => {
                  await item.action();
                  onClose();
                }}
                className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-sky-500/20 text-left transition-colors group"
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-4 h-4 text-sky-400 group-hover:text-sky-300" />
                  <span className="text-xs font-semibold text-slate-200">{item.title}</span>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                  {item.category}
                </span>
              </button>
            );
          })}

          {filtered.length === 0 && (
            <div className="p-6 text-center text-xs text-slate-500">No matching Raycast commands found.</div>
          )}
        </div>
      </div>
    </div>
  );
};
