import React, { useState, useEffect } from 'react';
import { Settings, Cpu, HardDrive, Shield } from 'lucide-react';
import { fetchSettings, saveSettings, fetchHealth } from '../services/api';

export const SettingsView: React.FC = () => {
  const [settings, setSettingsData] = useState<any>({});
  const [health, setHealthData] = useState<any>(null);

  useEffect(() => {
    fetchSettings().then(setSettingsData).catch(console.error);
    fetchHealth().then(setHealthData).catch(console.error);
  }, []);

  const handleSave = async () => {
    await saveSettings(settings);
    alert('Settings saved to disk!');
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 border-slate-700/60">
        <h2 className="text-xl font-bold nova-gradient-text mb-1 flex items-center gap-2">
          <Settings className="w-5 h-5 text-sky-400" />
          <span>Settings & Hardware Diagnostics</span>
        </h2>
        <p className="text-xs text-slate-400 mb-6">Customize LLM synthesis temperature, RAG chunk count, and voice parameters live.</p>

        {health && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <Cpu className="w-4 h-4 text-sky-400" /> CPU Usage
              </div>
              <div className="text-xl font-extrabold font-mono text-sky-300">{health.cpu?.percent}%</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <HardDrive className="w-4 h-4 text-purple-400" /> RAM Usage
              </div>
              <div className="text-xl font-extrabold font-mono text-purple-300">{health.memory?.percent}%</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <Shield className="w-4 h-4 text-emerald-400" /> Active Processes
              </div>
              <div className="text-xl font-extrabold font-mono text-emerald-300">{health.top_processes?.length || 0} Top Procs</div>
            </div>
          </div>
        )}

        <div className="space-y-4 max-w-xl">
          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">LLM Temperature (Creativity): {settings.temperature ?? 0.7}</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={settings.temperature ?? 0.7}
              onChange={(e) => setSettingsData({ ...settings, temperature: parseFloat(e.target.value) })}
              className="w-full accent-sky-400"
            />
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">RAG Candidate Chunks (Top-K): {settings.rag_top_k ?? 4}</label>
            <input
              type="range"
              min="1"
              max="10"
              value={settings.rag_top_k ?? 4}
              onChange={(e) => setSettingsData({ ...settings, rag_top_k: parseInt(e.target.value) })}
              className="w-full accent-purple-400"
            />
          </div>

          <button
            onClick={handleSave}
            className="w-full py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-white text-xs font-bold transition-colors"
          >
            Save Preferences
          </button>
        </div>
      </div>
    </div>
  );
};
