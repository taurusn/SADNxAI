'use client';

import { useEffect } from 'react';
import { useStore } from '@/lib/store';
import Sidebar from '@/components/Sidebar';
import ChatArea from '@/components/ChatArea';

export default function Home() {
  const { loadSessions, error, clearError, sidebarOpen, closeSidebar } = useStore();

  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  return (
    <div className="flex h-[100dvh] overflow-hidden">
      {/* Mobile overlay backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden transition-opacity"
          onClick={closeSidebar}
        />
      )}

      {/* Sidebar - drawer on mobile, fixed on desktop */}
      <div className={`
        fixed md:relative inset-y-0 left-0 z-50
        transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        <Sidebar onClose={closeSidebar} />
      </div>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col overflow-hidden w-full">
        <ChatArea />
      </main>

      {/* Error Toast - responsive positioning */}
      {error && (
        <div className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-4 sm:max-w-md bg-error text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3">
          <span className="flex-1">{error}</span>
          <button
            onClick={clearError}
            className="text-white/80 hover:text-white p-1"
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
