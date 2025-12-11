'use client';

import { useEffect } from 'react';
import { useStore } from '@/lib/store';
import Sidebar from '@/components/Sidebar';
import ChatArea from '@/components/ChatArea';

export default function Home() {
  const { loadSessions, error, clearError } = useStore();

  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <ChatArea />
      </main>

      {/* Error Toast */}
      {error && (
        <div className="fixed bottom-4 right-4 bg-error text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 max-w-md">
          <span className="flex-1">{error}</span>
          <button
            onClick={clearError}
            className="text-white/80 hover:text-white"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
}
