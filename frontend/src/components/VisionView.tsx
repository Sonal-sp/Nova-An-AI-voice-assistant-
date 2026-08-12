import React, { useState } from 'react';
import { Eye, Upload, Sparkles } from 'lucide-react';
import { analyzeVisionImage } from '../services/api';

export const VisionView: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setAnalysisResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
    try {
      const res = await analyzeVisionImage(selectedFile, prompt);
      setAnalysisResult(res.analysis);
    } catch (e: any) {
      alert(`Vision AI Error: ${e.message}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 border-pink-500/30">
        <h2 className="text-xl font-bold nova-gradient-text mb-1 flex items-center gap-2">
          <Eye className="w-5 h-5 text-pink-400" />
          <span>Vision AI & Optical Character Recognition (OCR)</span>
        </h2>
        <p className="text-xs text-slate-400">
          Upload UI mockups, architecture diagrams, screenshots, or text documents to synthesize visual breakdown and OCR text.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          <div className="space-y-4">
            <div className="border-2 border-dashed border-slate-700 hover:border-pink-500/50 rounded-2xl p-6 text-center transition-colors">
              {previewUrl ? (
                <img src={previewUrl} alt="Preview" className="max-h-48 rounded-xl mx-auto border border-slate-700" />
              ) : (
                <div>
                  <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                  <p className="text-xs text-slate-400 mb-2">Upload screenshot, diagram, or text image</p>
                </div>
              )}
              <label className="mt-3 inline-block">
                <span className="px-3.5 py-1.5 rounded-xl bg-pink-600 hover:bg-pink-500 text-white text-xs font-bold transition-colors cursor-pointer">
                  {previewUrl ? 'Change Image' : 'Select Image'}
                </span>
                <input type="file" accept="image/*" onChange={handleImageSelect} className="hidden" />
              </label>
            </div>

            <div>
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Custom analysis prompt (e.g. 'Extract all text via OCR')..."
                className="w-full bg-slate-900/90 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-pink-500"
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={!selectedFile || isAnalyzing}
              className="w-full py-2.5 rounded-xl bg-gradient-to-tr from-pink-500 to-purple-600 text-white text-xs font-bold disabled:opacity-40 hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              <span>{isAnalyzing ? 'Analyzing Image Visuals...' : 'Synthesize Vision AI Analysis'}</span>
            </button>
          </div>

          <div className="glass-panel p-5 bg-slate-900/80">
            <h3 className="text-xs font-bold text-pink-400 uppercase tracking-wider mb-3">Analysis Result</h3>
            {analysisResult ? (
              <div className="text-xs text-slate-200 leading-relaxed whitespace-pre-wrap font-sans max-h-72 overflow-y-auto pr-1">
                {analysisResult}
              </div>
            ) : (
              <div className="text-center py-16 text-xs text-slate-500">
                Upload an image on the left and click synthesize to see Vision AI analysis.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
