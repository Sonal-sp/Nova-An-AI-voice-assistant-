import React from 'react';
import {
  MessageSquare, FileText, Eye, CheckSquare, Layers, Activity, Settings, Mic,
  Code, Globe, Music, Calculator
} from 'lucide-react';
import { launchDesktopApp } from '../services/api';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  selectedModel: string;
  setSelectedModel: (model: string) => void;
  models: string[];
  isListening: boolean;
  onToggleListening: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  selectedModel,
  setSelectedModel,
  models,
  isListening,
  onToggleListening,
}) => {
  const navItems = [
    { id: 'chat', label: 'AI Workspace Chat', icon: MessageSquare },
    { id: 'rag', label: 'Hybrid RAG (FAISS+BM25)', icon: FileText },
    { id: 'vision', label: 'Vision AI & OCR', icon: Eye },
    { id: 'productivity', label: 'Productivity Suite', icon: CheckSquare },
    { id: 'integrations', label: 'Cloud Integrations', icon: Layers },
    { id: 'diagnostics', label: 'System Diagnostics', icon: Activity },
    { id: 'settings', label: 'Preferences', icon: Settings },
  ];

  const handleLaunch = async (appName: string) => {
    try {
      const res = await launchDesktopApp(appName);
      alert(res.message || `Launched ${appName}`);
    } catch (e) {
      alert(`Error launching ${appName}`);
    }
  };

  return (
    <aside className="glass-panel w-72 p-5 flex flex-col justify-between shrink-0 hidden lg:flex">
      <div className="space-y-6">
        {/* Model Switcher */}
        <div>
          <label className="text-xs font-semibold text-slate-400 block mb-2 uppercase tracking-wider">
            🧠 Model Engine
          </label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full bg-slate-900/90 border border-slate-700/70 rounded-xl px-3 py-2 text-xs font-semibold text-slate-100 focus:outline-none focus:border-sky-500 transition-colors cursor-pointer"
          >
            {models.map((m) => (
              <option key={m} value={m} className="bg-slate-900 text-slate-100">
                {m}
              </option>
            ))}
          </select>
        </div>

        {/* Continuous Voice Engine Card */}
        <div className="p-4 rounded-xl bg-slate-900/70 border border-sky-500/30 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-sky-400 flex items-center gap-1.5">
              <Mic className="w-4 h-4" />
              <span>Voice Assistant</span>
            </span>
            <span className={`w-2 h-2 rounded-full ${isListening ? 'bg-emerald-400 animate-ping' : 'bg-slate-600'}`} />
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Continuous Web Speech listener active. Say <strong className="text-sky-300">"Hey Nova"</strong> hands-free!
          </p>
          <button
            onClick={onToggleListening}
            className={`w-full py-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 ${
              isListening
                ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-rose-500/30'
                : 'bg-sky-500/20 text-sky-300 border border-sky-500/40 hover:bg-sky-500/30'
            }`}
          >
            <Mic className="w-3.5 h-3.5" />
            <span>{isListening ? 'Pause "Hey Nova"' : 'Enable "Hey Nova"'}</span>
          </button>
        </div>

        {/* Navigation Section */}
        <div>
          <label className="text-xs font-semibold text-slate-400 block mb-2 uppercase tracking-wider">
            ⚙️ Control Center
          </label>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-sky-500/20 to-purple-500/20 text-sky-300 border border-sky-500/40 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-500'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Raycast Quick Launch Apps */}
        <div>
          <label className="text-xs font-semibold text-slate-400 block mb-2 uppercase tracking-wider">
            🖥️ Desktop Raycast Launcher
          </label>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => handleLaunch('vscode')}
              className="flex items-center gap-1.5 px-2.5 py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-slate-700/50 text-[11px] font-medium text-slate-300 transition-colors"
            >
              <Code className="w-3.5 h-3.5 text-blue-400" />
              <span>VS Code</span>
            </button>
            <button
              onClick={() => handleLaunch('chrome')}
              className="flex items-center gap-1.5 px-2.5 py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-slate-700/50 text-[11px] font-medium text-slate-300 transition-colors"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-400" />
              <span>Chrome</span>
            </button>
            <button
              onClick={() => handleLaunch('spotify')}
              className="flex items-center gap-1.5 px-2.5 py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-slate-700/50 text-[11px] font-medium text-slate-300 transition-colors"
            >
              <Music className="w-3.5 h-3.5 text-green-400" />
              <span>Spotify</span>
            </button>
            <button
              onClick={() => handleLaunch('calc')}
              className="flex items-center gap-1.5 px-2.5 py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-slate-700/50 text-[11px] font-medium text-slate-300 transition-colors"
            >
              <Calculator className="w-3.5 h-3.5 text-orange-400" />
              <span>Calculator</span>
            </button>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-800 text-[10px] text-slate-500 text-center">
        Nova AI Operating System v2.5.0 • All Rights Reserved
      </div>
    </aside>
  );
};
