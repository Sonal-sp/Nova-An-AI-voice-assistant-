import React, { useState, useEffect } from 'react';
import { Activity, Cpu, HardDrive, Database, RefreshCw, Copy, Check } from 'lucide-react';
import { fetchHealth } from '../services/api';

export const DiagnosticsView: React.FC = () => {
  const [diagnosticsData, setDiagnosticsData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchHealth();
      setDiagnosticsData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCopy = () => {
    if (diagnosticsData) {
      navigator.clipboard.writeText(JSON.stringify(diagnosticsData, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="glass-panel p-6 border-slate-700/60">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold nova-gradient-text flex items-center gap-2">
              <Activity className="w-5 h-5 text-sky-400" />
              <span>System Benchmark Diagnostics</span>
            </h2>
            <p className="text-xs text-slate-400">Real-time hardware performance monitor, CPU/RAM stats, and active process tree.</p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-white transition-all flex items-center gap-1.5"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy JSON'}</span>
            </button>
            <button
              onClick={loadData}
              className="px-3.5 py-1.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-white text-xs font-bold transition-all flex items-center gap-1.5 shadow-md shadow-sky-500/20"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Run Benchmark</span>
            </button>
          </div>
        </div>

        {diagnosticsData && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <Cpu className="w-4 h-4 text-sky-400" /> OS Platform
              </div>
              <div className="text-sm font-bold text-slate-100">{diagnosticsData.system_info?.os_name} {diagnosticsData.system_info?.os_release}</div>
              <span className="text-[10px] text-slate-500 font-mono">Python {diagnosticsData.system_info?.python_version}</span>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <Cpu className="w-4 h-4 text-sky-400" /> CPU Load
              </div>
              <div className="text-xl font-extrabold text-sky-300 font-mono">{diagnosticsData.cpu?.percent}%</div>
              <span className="text-[10px] text-slate-500 font-mono">{diagnosticsData.cpu?.logical_cores} Cores</span>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <HardDrive className="w-4 h-4 text-purple-400" /> RAM Memory
              </div>
              <div className="text-xl font-extrabold text-purple-300 font-mono">{diagnosticsData.memory?.percent}%</div>
              <span className="text-[10px] text-slate-500 font-mono">{diagnosticsData.memory?.used_gb} / {diagnosticsData.memory?.total_gb} GB</span>
            </div>

            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
              <div className="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
                <Database className="w-4 h-4 text-emerald-400" /> Disk Storage
              </div>
              <div className="text-xl font-extrabold text-emerald-300 font-mono">{diagnosticsData.storage?.percent}%</div>
              <span className="text-[10px] text-slate-500 font-mono">{diagnosticsData.storage?.free_gb} GB Free</span>
            </div>
          </div>
        )}

        {/* Diagnostic JSON Report Box */}
        <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 font-mono text-xs text-sky-300 overflow-x-auto max-h-96">
          <pre>{JSON.stringify(diagnosticsData, null, 2)}</pre>
        </div>
      </div>
    </div>
  );
};
