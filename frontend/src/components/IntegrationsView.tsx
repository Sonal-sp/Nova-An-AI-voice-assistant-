import React from 'react';
import { Layers, Mail, HardDrive, Calendar, MessageSquare, Code } from 'lucide-react';

export const IntegrationsView: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 border-sky-500/30">
        <h2 className="text-xl font-bold nova-gradient-text mb-1 flex items-center gap-2">
          <Layers className="w-5 h-5 text-sky-400" />
          <span>Cloud Integrations Control Suite</span>
        </h2>
        <p className="text-xs text-slate-400 mb-6">
          Real-time API integrations with Gmail, Google Drive, Google Calendar, GitHub, Notion, Slack, and Discord.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100 flex items-center gap-2">
                <Code className="w-4 h-4 text-sky-400" /> GitHub
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Connected</span>
            </div>
            <p className="text-[11px] text-slate-400">Search repos, issues & profiles</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100 flex items-center gap-2">
                <Mail className="w-4 h-4 text-rose-400" /> Gmail
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Connected</span>
            </div>
            <p className="text-[11px] text-slate-400">Read unread emails & create drafts</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100 flex items-center gap-2">
                <HardDrive className="w-4 h-4 text-amber-400" /> Google Drive
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Connected</span>
            </div>
            <p className="text-[11px] text-slate-400">Search cloud docs & PDF assets</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100 flex items-center gap-2">
                <Calendar className="w-4 h-4 text-blue-400" /> Google Calendar
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Connected</span>
            </div>
            <p className="text-[11px] text-slate-400">Schedule & sync calendar meetings</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-100 flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-purple-400" /> Slack & Discord
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">Connected</span>
            </div>
            <p className="text-[11px] text-slate-400">Dispatch Webhook channel messages</p>
          </div>
        </div>
      </div>
    </div>
  );
};
