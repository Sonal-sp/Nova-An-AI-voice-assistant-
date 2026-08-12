import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { ChatView } from './components/ChatView';
import { RagView } from './components/RagView';
import { VisionView } from './components/VisionView';
import { ProductivityView } from './components/ProductivityView';
import { IntegrationsView } from './components/IntegrationsView';
import { SettingsView } from './components/SettingsView';
import { DiagnosticsView } from './components/DiagnosticsView';
import { CommandPalette } from './components/CommandPalette';
import { wakeWordEngine } from './services/wakeWord';
import { fetchHealth, fetchModels } from './services/api';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [selectedModel, setSelectedModel] = useState('Gemini 2.5 Flash');
  const [models, setModels] = useState<string[]>(['Gemini 2.5 Flash', 'Gemini 2.0 Flash']);
  const [health, setHealth] = useState<any>(null);
  const [isListening, setIsListening] = useState(true);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [voicePrompt, setVoicePrompt] = useState<string | undefined>(undefined);

  useEffect(() => {
    // Poll system health metrics
    const interval = setInterval(() => {
      fetchHealth().then(setHealth).catch(console.error);
    }, 5000);
    fetchHealth().then(setHealth).catch(console.error);

    // Fetch models
    fetchModels().then((data) => setModels(data.models)).catch(console.error);

    return () => clearInterval(interval);
  }, []);

  // Initialize continuous Web Speech Wake Word Listener ("Hey Nova")
  useEffect(() => {
    if (isListening) {
      wakeWordEngine.start((prompt, wakeWordDetected) => {
        if (wakeWordDetected || prompt) {
          setActiveTab('chat');
          setVoicePrompt(prompt);
        }
      });
    } else {
      wakeWordEngine.stop();
    }
  }, [isListening]);

  // Keyboard shortcut listener for Raycast Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="min-h-screen bg-[#07090E] text-slate-100 flex flex-col p-4 md:p-6 selection:bg-sky-500/30 selection:text-sky-200">
      {/* Top Glassmorphic Header */}
      <Header health={health} onOpenCommandPalette={() => setIsCommandPaletteOpen(true)} />

      {/* Main OS Body Layout */}
      <div className="flex-1 flex gap-6 max-w-7xl w-full mx-auto">
        {/* Control Center Sidebar */}
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          selectedModel={selectedModel}
          setSelectedModel={setSelectedModel}
          models={models}
          isListening={isListening}
          onToggleListening={() => setIsListening(!isListening)}
        />

        {/* Dynamic Active Workspace View */}
        <main className="flex-1 flex flex-col min-w-0">
          {activeTab === 'chat' && (
            <ChatView
              selectedModel={selectedModel}
              isListening={isListening}
              externalPrompt={voicePrompt}
              onClearExternalPrompt={() => setVoicePrompt(undefined)}
            />
          )}

          {activeTab === 'rag' && <RagView />}

          {activeTab === 'vision' && <VisionView />}

          {activeTab === 'productivity' && <ProductivityView />}

          {activeTab === 'integrations' && <IntegrationsView />}

          {activeTab === 'diagnostics' && <DiagnosticsView />}

          {activeTab === 'settings' && <SettingsView />}
        </main>
      </div>

      {/* Raycast Cmd+K Command Palette Modal */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onSelectTab={(tab) => {
          setActiveTab(tab);
          setIsCommandPaletteOpen(false);
        }}
      />
    </div>
  );
};

export default App;
