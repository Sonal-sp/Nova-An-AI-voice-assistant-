import React, { useState, useEffect, useRef } from 'react';
import { Send, Copy, Volume2, FileText, Check, Sparkles } from 'lucide-react';
import { VoiceWidget } from './VoiceWidget';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: any[];
  metadata?: any;
}

interface ChatViewProps {
  selectedModel: string;
  isListening: boolean;
  externalPrompt?: string;
  onClearExternalPrompt?: () => void;
}

export const ChatView: React.FC<ChatViewProps> = ({
  selectedModel,
  isListening,
  externalPrompt,
  onClearExternalPrompt,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [streamingText, setStreamingText] = useState('');
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const chatBottomRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingText]);

  // Handle trigger from external continuous wake word listener ("Hey Nova")
  useEffect(() => {
    if (externalPrompt) {
      handleSendMessage(externalPrompt);
      if (onClearExternalPrompt) onClearExternalPrompt();
    }
  }, [externalPrompt]);

  const handleSendMessage = async (customText?: string) => {
    const promptText = customText || input;
    if (!promptText.trim() || isGenerating) return;

    const userMessage: Message = { role: 'user', content: promptText };
    setMessages((prev) => [...prev, userMessage]);
    if (!customText) setInput('');
    setIsGenerating(true);
    setStreamingText('');

    try {
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: promptText,
          selected_model: selectedModel,
        }),
      });

      if (!response.body) throw new Error('ReadableStream not supported');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';
      let citations: any[] = [];
      let metadata: any = {};

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunkStr = decoder.decode(value, { stream: true });
        const lines = chunkStr.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));
              if (data.type === 'token') {
                accumulatedText += data.content;
                setStreamingText(accumulatedText);
              } else if (data.type === 'done') {
                citations = data.citations || [];
                metadata = data.metadata || {};
              }
            } catch (e) {
              // Ignore non-JSON lines
            }
          }
        }
      }

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: accumulatedText || 'Response completed.',
          citations,
          metadata,
        },
      ]);
      setStreamingText('');
    } catch (e: any) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `⚠️ Error generating response: ${e.message}` },
      ]);
    } finally {
      setIsGenerating(false);
    }
  };

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-140px)] relative">
      {/* Voice Visualizer Indicator */}
      <VoiceWidget isListening={isListening} />

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto pr-2 space-y-4 pb-24">
        {messages.length === 0 && !streamingText && (
          <div className="text-center py-16 px-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-sky-400 to-purple-600 flex items-center justify-center text-3xl mx-auto mb-4 shadow-xl shadow-sky-500/20">
              🤖
            </div>
            <h2 className="text-2xl font-bold nova-gradient-text mb-2">Welcome to Nova AI OS</h2>
            <p className="text-sm text-slate-400 max-w-md mx-auto leading-relaxed">
              Ask anything, upload PDFs for hybrid RAG, synthesize vision mockups, or say <strong className="text-sky-300">"Hey Nova"</strong> for continuous voice command!
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 max-w-3xl mx-auto mt-8">
              <button
                onClick={() => handleSendMessage('Explain quantum physics in simple terms')}
                className="p-3.5 text-left rounded-xl bg-slate-900/60 border border-slate-800 hover:border-sky-500/40 hover:bg-slate-800/80 transition-all text-xs font-semibold text-slate-300"
              >
                🎙️ <span className="text-sky-400 font-bold block mb-1">Voice & Concept Explanation</span>
                Quantum physics in simple terms
              </button>
              <button
                onClick={() => handleSendMessage('How does hybrid FAISS + BM25 RAG work?')}
                className="p-3.5 text-left rounded-xl bg-slate-900/60 border border-slate-800 hover:border-purple-500/40 hover:bg-slate-800/80 transition-all text-xs font-semibold text-slate-300"
              >
                📄 <span className="text-purple-400 font-bold block mb-1">Hybrid RAG Query</span>
                How FAISS + BM25 RAG works
              </button>
              <button
                onClick={() => handleSendMessage('Launch VS Code desktop application')}
                className="p-3.5 text-left rounded-xl bg-slate-900/60 border border-slate-800 hover:border-pink-500/40 hover:bg-slate-800/80 transition-all text-xs font-semibold text-slate-300"
              >
                🖥️ <span className="text-pink-400 font-bold block mb-1">Desktop System Launcher</span>
                Launch VS Code desktop app
              </button>
              <button
                onClick={() => handleSendMessage('Show system hardware performance status')}
                className="p-3.5 text-left rounded-xl bg-slate-900/60 border border-slate-800 hover:border-emerald-500/40 hover:bg-slate-800/80 transition-all text-xs font-semibold text-slate-300"
              >
                📊 <span className="text-emerald-400 font-bold block mb-1">Hardware Monitor</span>
                Check CPU and memory usage
              </button>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`glass-panel p-5 transition-all ${
              msg.role === 'user' ? 'border-sky-500/20 bg-slate-900/40' : 'border-slate-700/60 bg-slate-900/70'
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2.5">
                <span className="text-lg">{msg.role === 'user' ? '👤' : '🤖'}</span>
                <span className="text-xs font-bold text-slate-200">
                  {msg.role === 'user' ? 'User' : 'Nova AI OS'}
                </span>
                {msg.role === 'assistant' && (
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-sky-500/10 text-sky-400 border border-sky-500/30">
                    {selectedModel}
                  </span>
                )}
              </div>

              {msg.role === 'assistant' && (
                <div className="flex items-center gap-1.5">
                  <button
                    onClick={() => copyToClipboard(msg.content, index)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
                    title="Copy response"
                  >
                    {copiedIndex === index ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                  <button
                    onClick={() => speakText(msg.content)}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800 transition-colors"
                    title="Speak aloud (TTS)"
                  >
                    <Volume2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </div>

            <div className="text-sm text-slate-200 leading-relaxed whitespace-pre-wrap font-sans">
              {msg.content}
            </div>

            {/* RAG Citations */}
            {msg.citations && msg.citations.length > 0 && (
              <div className="mt-4 pt-3 border-t border-slate-800">
                <div className="text-xs font-bold text-sky-400 flex items-center gap-1.5 mb-2">
                  <FileText className="w-3.5 h-3.5" />
                  <span>Attributed RAG Sources</span>
                </div>
                <div className="space-y-1.5">
                  {msg.citations.map((cit: any, cIdx: number) => (
                    <div key={cIdx} className="p-2 rounded-lg bg-slate-950/60 border border-slate-800 text-xs text-slate-300">
                      <span className="font-semibold text-purple-300">{cit.document || 'Document'} (Page {cit.page || 1})</span>: "{cit.text}"
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}

        {/* Live SSE Token Streaming Assistant Box */}
        {streamingText && (
          <div className="glass-panel p-5 border-sky-500/40 bg-slate-900/80">
            <div className="flex items-center gap-2.5 mb-3">
              <span className="text-lg">🤖</span>
              <span className="text-xs font-bold text-sky-400 flex items-center gap-1.5">
                <span>Nova AI OS</span>
                <Sparkles className="w-3.5 h-3.5 animate-spin text-purple-400" />
              </span>
            </div>
            <div className="text-sm text-slate-100 leading-relaxed whitespace-pre-wrap font-sans">
              {streamingText}
              <span className="inline-block w-2 h-4 bg-sky-400 ml-1 animate-pulse" />
            </div>
          </div>
        )}

        <div ref={chatBottomRef} />
      </div>

      {/* Raycast Floating Chat Input */}
      <div className="absolute bottom-0 left-0 right-0 pt-2 pb-1 bg-gradient-to-t from-[#07090E] via-[#07090E]/90 to-transparent">
        <div className="glass-panel p-2 flex items-center gap-2 border-sky-500/30 focus-within:border-sky-400 shadow-2xl shadow-sky-500/10">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask Nova anything (or say 'Hey Nova')..."
            className="flex-1 bg-transparent border-none px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
            disabled={isGenerating}
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={!input.trim() || isGenerating}
            className="p-2.5 rounded-xl bg-gradient-to-tr from-sky-400 to-purple-600 text-white font-semibold disabled:opacity-40 hover:opacity-90 transition-opacity"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
