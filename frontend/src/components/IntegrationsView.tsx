import React, { useState, useEffect } from 'react';
import { Layers, Mail, HardDrive, Calendar, MessageSquare, Code, CheckCircle, ShieldCheck, Key, RefreshCw, X, LogOut, FileText } from 'lucide-react';
import { fetchIntegrations, connectIntegration, testIntegration, disconnectIntegration } from '../services/api';

interface ServiceConfig {
  id: string;
  name: string;
  category: string;
  icon: any;
  color: string;
  description: string;
  tokenLabel: string;
  tokenPlaceholder: string;
  configFields?: { key: string; label: string; placeholder: string }[];
}

export const IntegrationsView: React.FC = () => {
  const [integrationsData, setIntegrationsData] = useState<any>({});
  const [loading, setLoading] = useState(false);
  const [activeModalService, setActiveModalService] = useState<ServiceConfig | null>(null);

  // Form modal states
  const [authToken, setAuthToken] = useState('');
  const [configFields, setConfigFields] = useState<Record<string, string>>({});
  const [testingStatus, setTestingStatus] = useState<string | null>(null);
  const [testingError, setTestingError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const servicesList: ServiceConfig[] = [
    {
      id: 'github',
      name: 'GitHub Workspace',
      category: 'Developer Platform',
      icon: Code,
      color: 'text-sky-400',
      description: 'Search repositories, manage pull requests, code issues & profile data',
      tokenLabel: 'Personal Access Token / OAuth Token',
      tokenPlaceholder: 'ghp_xxxxxxxxxxxxxxxxxxxx',
    },
    {
      id: 'gmail',
      name: 'Gmail Workspace',
      category: 'Email & Communications',
      icon: Mail,
      color: 'text-rose-400',
      description: 'Fetch unread inbox messages, search emails, and compose drafts',
      tokenLabel: 'Google Account Email',
      tokenPlaceholder: 'user@gmail.com',
    },
    {
      id: 'gdrive',
      name: 'Google Drive',
      category: 'Cloud File Storage',
      icon: HardDrive,
      color: 'text-amber-400',
      description: 'Index cloud documents, PDFs, and team assets into RAG search',
      tokenLabel: 'Google Account Email',
      tokenPlaceholder: 'user@gmail.com',
    },
    {
      id: 'gcalendar',
      name: 'Google Calendar',
      category: 'Schedule & Events',
      icon: Calendar,
      color: 'text-blue-400',
      description: 'Schedule, sync, and inspect daily meeting agenda items',
      tokenLabel: 'Google Account Email',
      tokenPlaceholder: 'user@gmail.com',
    },
    {
      id: 'notion',
      name: 'Notion Workspace',
      category: 'Knowledge Base',
      icon: FileText,
      color: 'text-emerald-400',
      description: 'Search Notion workspace pages and sync internal team docs',
      tokenLabel: 'Notion Integration Secret Token',
      tokenPlaceholder: 'secret_xxxxxxxxxxxxxxxxxxxx',
    },
    {
      id: 'slack',
      name: 'Slack Webhooks',
      category: 'Channel Messaging',
      icon: MessageSquare,
      color: 'text-purple-400',
      description: 'Dispatch real-time notification alerts to Slack channels',
      tokenLabel: 'Slack Incoming Webhook URL',
      tokenPlaceholder: 'https://hooks.slack.com/services/T00/B00/XXXX',
    },
    {
      id: 'discord',
      name: 'Discord Webhooks',
      category: 'Channel Messaging',
      icon: MessageSquare,
      color: 'text-indigo-400',
      description: 'Dispatch automated updates & alerts to Discord server webhooks',
      tokenLabel: 'Discord Webhook URL',
      tokenPlaceholder: 'https://discord.com/api/webhooks/12345/XXXX',
    },
  ];

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetchIntegrations();
      setIntegrationsData(res.user_integrations || {});
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const openConnectModal = (service: ServiceConfig) => {
    setActiveModalService(service);
    setAuthToken('');
    setConfigFields({});
    setTestingStatus(null);
    setTestingError(null);
  };

  const handleTestConnection = async () => {
    if (!activeModalService) return;
    setTestingStatus('Testing live API authentication...');
    setTestingError(null);

    try {
      const res = await testIntegration(activeModalService.id, authToken, configFields);
      if (res.success) {
        setTestingStatus(`✅ ${res.message}`);
      } else {
        setTestingError(`⚠️ ${res.message}`);
        setTestingStatus(null);
      }
    } catch (e: any) {
      setTestingError(`⚠️ Connection failed: ${e.message}`);
      setTestingStatus(null);
    }
  };

  const handleSaveConnection = async () => {
    if (!activeModalService) return;
    setIsSubmitting(true);
    try {
      const res = await connectIntegration(activeModalService.id, authToken, configFields);
      if (res.success) {
        await loadData();
        setActiveModalService(null);
      } else {
        setTestingError(res.message);
      }
    } catch (e: any) {
      setTestingError(e.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDisconnect = async (serviceId: string) => {
    if (!confirm(`Are you sure you want to disconnect ${serviceId.toUpperCase()}?`)) return;
    await disconnectIntegration(serviceId);
    await loadData();
    if (activeModalService?.id === serviceId) setActiveModalService(null);
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="glass-panel p-6 border-sky-500/30">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold nova-gradient-text flex items-center gap-2">
              <Layers className="w-5 h-5 text-sky-400" />
              <span>Cloud Integrations & Account Persistence</span>
            </h2>
            <p className="text-xs text-slate-400">
              Connect external services to authenticate API access for Gmail, Google Drive, Calendar, GitHub, Notion, Slack, and Discord.
            </p>
          </div>

          <button
            onClick={loadData}
            className="p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 transition-all text-xs font-medium flex items-center gap-1.5"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-sky-400' : ''}`} />
            <span>Sync Accounts</span>
          </button>
        </div>

        {/* Integration Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          {servicesList.map((svc) => {
            const Icon = svc.icon;
            const userAccount = integrationsData[svc.id] || {};
            const isConnected = userAccount.status === 'connected';

            return (
              <div
                key={svc.id}
                className={`p-5 rounded-2xl glass-panel-hover flex flex-col justify-between space-y-4 border transition-all ${
                  isConnected
                    ? 'bg-slate-900/80 border-emerald-500/30 shadow-lg shadow-emerald-500/5'
                    : 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                      <div className={`p-2 rounded-xl bg-slate-900 border border-slate-800 ${svc.color}`}>
                        <Icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-slate-100">{svc.name}</h4>
                        <span className="text-[10px] text-slate-400 block">{svc.category}</span>
                      </div>
                    </div>

                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border flex items-center gap-1 ${
                        isConnected
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                          : 'bg-slate-800/80 text-slate-400 border-slate-700'
                      }`}
                    >
                      {isConnected ? <CheckCircle className="w-3 h-3 text-emerald-400" /> : <ShieldCheck className="w-3 h-3 text-slate-500" />}
                      <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
                    </span>
                  </div>

                  <p className="text-[11px] text-slate-400 leading-relaxed">{svc.description}</p>
                </div>

                <div className="pt-3 border-t border-slate-800/80 space-y-3">
                  {isConnected && (
                    <div className="text-[11px] font-mono text-emerald-300 bg-emerald-500/5 p-2 rounded-lg border border-emerald-500/20 truncate">
                      👤 {userAccount.account_identifier || 'Active Account'}
                    </div>
                  )}

                  <div className="flex gap-2">
                    <button
                      onClick={() => openConnectModal(svc)}
                      className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${
                        isConnected
                          ? 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700'
                          : 'bg-gradient-to-r from-sky-500 to-purple-600 hover:opacity-90 text-white shadow-md shadow-sky-500/20'
                      }`}
                    >
                      {isConnected ? 'Manage Integration' : 'Connect Account'}
                    </button>
                    {isConnected && (
                      <button
                        onClick={() => handleDisconnect(svc.id)}
                        className="p-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 transition-colors"
                        title="Disconnect Account"
                      >
                        <LogOut className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Account Connection Modal */}
      {activeModalService && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-panel w-full max-w-lg p-6 border-sky-500/40 shadow-2xl space-y-5 animate-in fade-in zoom-in duration-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <Key className="w-5 h-5 text-sky-400" />
                <div>
                  <h3 className="text-sm font-bold text-slate-100">Connect {activeModalService.name}</h3>
                  <p className="text-[11px] text-slate-400">Authenticate API credentials for Nova AI OS</p>
                </div>
              </div>
              <button
                onClick={() => setActiveModalService(null)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  {activeModalService.tokenLabel}
                </label>
                <input
                  type="password"
                  value={authToken}
                  onChange={(e) => setAuthToken(e.target.value)}
                  placeholder={activeModalService.tokenPlaceholder}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-sky-500"
                />
              </div>

              {testingStatus && (
                <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-semibold">
                  {testingStatus}
                </div>
              )}

              {testingError && (
                <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold">
                  {testingError}
                </div>
              )}

              <div className="flex items-center gap-3 pt-2">
                <button
                  onClick={handleTestConnection}
                  className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all border border-slate-700"
                >
                  Test Connection
                </button>
                <button
                  onClick={handleSaveConnection}
                  disabled={isSubmitting}
                  className="flex-1 py-2.5 rounded-xl bg-gradient-to-r from-sky-400 to-purple-600 hover:opacity-90 text-white text-xs font-bold transition-all shadow-md shadow-sky-500/20"
                >
                  {isSubmitting ? 'Authenticating...' : 'Save & Authenticate'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
