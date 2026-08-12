import React, { useState, useEffect } from 'react';
import { Settings, Cpu, HardDrive, Shield, Palette, Volume2, Save, Check } from 'lucide-react';
import { fetchSettings, saveSettings, fetchHealth } from '../services/api';

export const SettingsView: React.FC = () => {
  const [settings, setSettingsData] = useState<any>({
    theme: 'Cyberpunk Dark',
    voice_gender: 'Female',
    speech_rate: 1.0,
    speech_pitch: 1.0,
    wake_word: 'Hey Nova',
    auto_tts: false,
    temperature: 0.7,
    rag_top_k: 4,
  });
  const [health, setHealthData] = useState<any>(null);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    fetchSettings().then((d) => setSettingsData((prev: any) => ({ ...prev, ...d }))).catch(console.error);
    fetchHealth().then(setHealthData).catch(console.error);
  }, []);

  const handleSave = async () => {
    await saveSettings(settings);
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="glass-panel p-6 border-slate-700/60">
        <h2 className="text-xl font-bold nova-gradient-text mb-1 flex items-center gap-2">
          <Settings className="w-5 h-5 text-sky-400" />
          <span>Settings & Hardware Diagnostics</span>
        </h2>
        <p className="text-xs text-slate-400 mb-6">
          Customize AI OS theme, voice synthesis gender/pitch, LLM creativity temperature, and RAG search parameters live.
        </p>

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
              <div className="text-xl font-extrabold font-mono text-emerald-300">
                {health.top_processes?.length || 0} Top Procs
              </div>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {/* Theme & Design System */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
            <h3 className="text-xs font-bold text-sky-400 flex items-center gap-2 uppercase tracking-wider">
              <Palette className="w-4 h-4" /> AI OS Interface Theme
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {['Cyberpunk Dark', 'Midnight Blue', 'Matrix Emerald', 'Sunset Amber'].map((t) => (
                <button
                  key={t}
                  onClick={() => setSettingsData({ ...settings, theme: t })}
                  className={`p-2.5 rounded-xl border text-xs font-semibold transition-all ${
                    settings.theme === t
                      ? 'bg-sky-500/20 text-sky-300 border-sky-400'
                      : 'bg-slate-950/60 text-slate-400 border-slate-800 hover:text-slate-200'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* Voice Assistant & Speech Preferences */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
            <h3 className="text-xs font-bold text-purple-400 flex items-center gap-2 uppercase tracking-wider">
              <Volume2 className="w-4 h-4" /> Voice Synthesis Preferences
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Voice Gender / Accent</label>
                <select
                  value={settings.voice_gender ?? 'Female'}
                  onChange={(e) => setSettingsData({ ...settings, voice_gender: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
                >
                  <option value="Female">Female (en-US Natural)</option>
                  <option value="Male">Male (en-US Standard)</option>
                  <option value="British Female">British Female (en-GB)</option>
                  <option value="British Male">British Male (en-GB)</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">Wake-Word Phrase</label>
                <select
                  value={settings.wake_word ?? 'Hey Nova'}
                  onChange={(e) => setSettingsData({ ...settings, wake_word: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
                >
                  <option value="Hey Nova">"Hey Nova"</option>
                  <option value="Listen Nova">"Listen Nova"</option>
                  <option value="Ok Nova">"Ok Nova"</option>
                  <option value="Hello Nova">"Hello Nova"</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Speech Rate: {settings.speech_rate ?? 1.0}x
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="2.0"
                  step="0.1"
                  value={settings.speech_rate ?? 1.0}
                  onChange={(e) => setSettingsData({ ...settings, speech_rate: parseFloat(e.target.value) })}
                  className="w-full accent-purple-400"
                />
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Speech Pitch: {settings.speech_pitch ?? 1.0}x
                </label>
                <input
                  type="range"
                  min="0.5"
                  max="1.5"
                  step="0.1"
                  value={settings.speech_pitch ?? 1.0}
                  onChange={(e) => setSettingsData({ ...settings, speech_pitch: parseFloat(e.target.value) })}
                  className="w-full accent-purple-400"
                />
              </div>
            </div>
          </div>

          {/* Model & RAG Tuning */}
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
            <h3 className="text-xs font-bold text-sky-400 uppercase tracking-wider">🧠 Model Inference Tuning</h3>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">
                LLM Temperature (Creativity): {settings.temperature ?? 0.7}
              </label>
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
              <label className="text-xs font-semibold text-slate-300 block mb-1">
                RAG Candidate Chunks (Top-K): {settings.rag_top_k ?? 4}
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={settings.rag_top_k ?? 4}
                onChange={(e) => setSettingsData({ ...settings, rag_top_k: parseInt(e.target.value) })}
                className="w-full accent-sky-400"
              />
            </div>
          </div>

          <button
            onClick={handleSave}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-sky-400 to-purple-600 hover:opacity-90 text-white text-xs font-bold transition-all shadow-lg shadow-sky-500/20 flex items-center justify-center gap-2"
          >
            {savedSuccess ? <Check className="w-4 h-4 text-emerald-300" /> : <Save className="w-4 h-4" />}
            <span>{savedSuccess ? 'Preferences Saved Successfully!' : 'Save Preferences'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
