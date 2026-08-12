import React from 'react';

interface VoiceWidgetProps {
  isListening: boolean;
  statusText?: string;
}

export const VoiceWidget: React.FC<VoiceWidgetProps> = ({ isListening, statusText }) => {
  return (
    <div className="glass-panel p-4 mb-6 flex flex-col items-center justify-center border-sky-500/30 bg-slate-900/80 shadow-lg shadow-sky-500/10">
      <div className="flex items-center justify-center gap-2 h-10 my-2">
        <div className={`w-1.5 rounded-full bg-gradient-to-b from-sky-400 to-purple-500 ${isListening ? 'animate-bounce' : 'h-3 opacity-40'}`} style={{ animationDelay: '0s', height: '24px' }} />
        <div className={`w-1.5 rounded-full bg-gradient-to-b from-purple-400 to-pink-500 ${isListening ? 'animate-bounce' : 'h-5 opacity-40'}`} style={{ animationDelay: '0.15s', height: '36px' }} />
        <div className={`w-1.5 rounded-full bg-gradient-to-b from-cyan-400 to-sky-500 ${isListening ? 'animate-bounce' : 'h-4 opacity-40'}`} style={{ animationDelay: '0.3s', height: '28px' }} />
        <div className={`w-1.5 rounded-full bg-gradient-to-b from-pink-400 to-purple-500 ${isListening ? 'animate-bounce' : 'h-6 opacity-40'}`} style={{ animationDelay: '0.1s', height: '42px' }} />
        <div className={`w-1.5 rounded-full bg-gradient-to-b from-sky-400 to-cyan-500 ${isListening ? 'animate-bounce' : 'h-3 opacity-40'}`} style={{ animationDelay: '0.25s', height: '22px' }} />
      </div>
      <div className="text-xs font-semibold text-sky-400 tracking-wider uppercase font-mono mt-1">
        {statusText || (isListening ? '🎙️ Web Speech Listener Active — Say "Hey Nova"' : '🎤 Microphone Idle')}
      </div>
    </div>
  );
};
