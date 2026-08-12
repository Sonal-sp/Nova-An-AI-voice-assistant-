import React from 'react';
import { Cpu, HardDrive, ShieldCheck, Command } from 'lucide-react';

interface HeaderProps {
  health: any;
  onOpenCommandPalette: () => void;
}

export const Header: React.FC<HeaderProps> = ({ health, onOpenCommandPalette }) => {
  const cpuUsage = health?.cpu?.percent ?? 0;
  const ramUsage = health?.memory?.percent ?? 0;

  return (
    <header className="glass-panel px-6 py-4 mb-6 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-400 to-purple-600 flex items-center justify-center shadow-lg shadow-sky-500/20 text-xl font-bold">
          🤖
        </div>
        <div>
          <h1 className="text-xl font-extrabold nova-gradient-text tracking-tight">Nova AI OS</h1>
          <p className="text-xs text-slate-400">Next-Gen Multi-Modal Desktop & Cloud Intelligence Engine</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Hardware Status Pills */}
        <div className="hidden md:flex items-center gap-4 px-3 py-1.5 rounded-xl bg-slate-900/60 border border-slate-700/50 text-xs font-mono text-slate-300">
          <div className="flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-sky-400" />
            <span>CPU: <strong className="text-sky-300">{cpuUsage}%</strong></span>
          </div>
          <div className="w-px h-3 bg-slate-700" />
          <div className="flex items-center gap-1.5">
            <HardDrive className="w-3.5 h-3.5 text-purple-400" />
            <span>RAM: <strong className="text-purple-300">{ramUsage}%</strong></span>
          </div>
        </div>

        {/* Raycast Quick Command Button */}
        <button
          onClick={onOpenCommandPalette}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-xs text-slate-200 transition-all shadow-sm"
        >
          <Command className="w-3.5 h-3.5 text-sky-400" />
          <span>Cmd + K</span>
        </button>

        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>System Operational</span>
        </span>
      </div>
    </header>
  );
};
