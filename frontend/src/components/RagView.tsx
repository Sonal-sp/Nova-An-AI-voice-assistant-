import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, Database } from 'lucide-react';
import { uploadPdfDocument } from '../services/api';

export const RagView: React.FC = () => {
  const [documents, setDocuments] = useState<any[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      try {
        const doc = await uploadPdfDocument(file);
        setDocuments((prev) => [...prev, doc]);
      } catch (err) {
        alert(`Failed to index PDF ${file.name}`);
      }
    }
    setIsUploading(false);
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 border-purple-500/30">
        <h2 className="text-xl font-bold nova-gradient-text mb-1">📄 Hybrid FAISS + BM25 RAG Engine</h2>
        <p className="text-xs text-slate-400">
          Upload PDF document files to build dense cosine embeddings (FAISS) and sparse keyword indices (BM25) with Reciprocal Rank Fusion (RRF).
        </p>

        <div className="mt-6 border-2 border-dashed border-slate-700 hover:border-purple-500/50 rounded-2xl p-8 text-center transition-colors">
          <Upload className="w-10 h-10 text-purple-400 mx-auto mb-3 animate-pulse" />
          <label className="cursor-pointer">
            <span className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold transition-colors inline-block">
              {isUploading ? 'Indexing PDF Documents...' : 'Select PDF Files for RAG'}
            </span>
            <input type="file" accept="application/pdf" multiple onChange={handleFileUpload} className="hidden" disabled={isUploading} />
          </label>
          <p className="text-[11px] text-slate-500 mt-2">Supports multi-document PDF indexing with image extraction</p>
        </div>
      </div>

      {/* Indexed Documents Status */}
      <div className="glass-panel p-6">
        <h3 className="text-sm font-bold text-slate-200 mb-4 flex items-center gap-2">
          <Database className="w-4 h-4 text-purple-400" />
          <span>Indexed RAG Knowledgebase ({documents.length} Files)</span>
        </h3>

        {documents.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">No PDF documents indexed in memory. Upload above!</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {documents.map((doc, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900/80 border border-purple-500/30 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-purple-300 flex items-center gap-1.5">
                    <FileText className="w-4 h-4" />
                    <span>{doc.filename}</span>
                  </span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                    Ready
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 flex gap-4 font-mono">
                  <span>Pages: {doc.pages}</span>
                  <span>Chunks: {doc.chunk_count}</span>
                </div>
                <div className="flex gap-2 pt-1">
                  <span className="px-2 py-1 rounded bg-sky-500/10 text-sky-400 text-[10px] font-semibold flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> FAISS Vector
                  </span>
                  <span className="px-2 py-1 rounded bg-purple-500/10 text-purple-400 text-[10px] font-semibold flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> BM25 Sparse
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
