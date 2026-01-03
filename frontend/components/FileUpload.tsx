'use client';

import { useState, useRef, useCallback } from 'react';
import { useStore } from '@/lib/store';
import { Upload, FileText, X } from 'lucide-react';

export default function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { uploadFile, isSending } = useStore();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (selectedFile) {
      await uploadFile(selectedFile);
      setSelectedFile(null);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="w-full max-w-lg px-4 md:px-0">
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileSelect}
        className="hidden"
      />

      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !selectedFile && fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-xl p-6 md:p-8 text-center cursor-pointer transition-all
          ${isDragging
            ? 'border-primary bg-primary/5'
            : selectedFile
              ? 'border-green-400 bg-green-50'
              : 'border-gray-300 hover:border-primary hover:bg-gray-50'
          }
        `}
      >
        {selectedFile ? (
          <div className="space-y-4">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <FileText className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="font-medium text-gray-800">{selectedFile.name}</p>
              <p className="text-sm text-gray-500">{formatFileSize(selectedFile.size)}</p>
            </div>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedFile(null);
                }}
                className="px-4 py-3 min-h-[44px] text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleUpload();
                }}
                disabled={isSending}
                className="px-4 py-3 min-h-[44px] bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50"
              >
                {isSending ? 'Uploading...' : 'Upload & Analyze'}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto">
              <Upload className="w-6 h-6 text-gray-500" />
            </div>
            <div>
              <p className="font-medium text-gray-800">
                Drop your CSV file here
              </p>
              <p className="text-sm text-gray-500">
                or click to browse (max 100MB)
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Info */}
      <p className="mt-4 text-center text-xs text-gray-500">
        Upload a CSV file containing the data you want to anonymize.
        Our AI will analyze the columns and suggest appropriate privacy techniques.
      </p>
    </div>
  );
}
