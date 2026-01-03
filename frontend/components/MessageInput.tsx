'use client';

import { useState, useRef } from 'react';
import { useStore } from '@/lib/store';
import { Send, Paperclip } from 'lucide-react';

export default function MessageInput() {
  const [message, setMessage] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { sendMessage, uploadFile, isSending, currentSession } = useStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || isSending) return;

    const text = message.trim();
    setMessage('');
    await sendMessage(text);
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await uploadFile(file);
      // Reset input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const isDisabled = !currentSession || isSending;

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-3">
      {/* File Upload Button */}
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="hidden"
        disabled={isDisabled}
      />
      <button
        type="button"
        onClick={() => fileInputRef.current?.click()}
        disabled={isDisabled}
        className="p-3 min-h-[48px] min-w-[48px] flex items-center justify-center text-gray-500 hover:text-primary hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        title="Upload CSV file"
      >
        <Paperclip className="w-5 h-5" />
      </button>

      {/* Text Input */}
      <div className="flex-1 relative">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={
            currentSession?.status === 'idle'
              ? 'Upload a CSV file to get started...'
              : 'Type your message...'
          }
          disabled={isDisabled}
          rows={1}
          className="w-full px-4 py-2.5 border border-gray-300 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary disabled:bg-gray-50 disabled:cursor-not-allowed"
          style={{ minHeight: '44px', maxHeight: '120px' }}
        />
      </div>

      {/* Send Button */}
      <button
        type="submit"
        disabled={isDisabled || !message.trim()}
        className="p-3 min-h-[48px] min-w-[48px] flex items-center justify-center bg-primary text-white rounded-xl hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send className="w-5 h-5" />
      </button>
    </form>
  );
}
