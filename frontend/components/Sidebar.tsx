'use client';

import { useStore } from '@/lib/store';
import { Plus, MessageSquare, Trash2, X } from 'lucide-react';
import Image from 'next/image';

interface SidebarProps {
  onClose?: () => void;
}

const STATUS_COLORS: Record<string, string> = {
  idle: 'bg-gray-400',
  analyzing: 'bg-yellow-400',
  proposed: 'bg-amber-600',
  discussing: 'bg-amber-600',
  approved: 'bg-purple-400',
  masking: 'bg-orange-400',
  validating: 'bg-orange-400',
  completed: 'bg-green-400',
  failed: 'bg-red-400',
};

export default function Sidebar({ onClose }: SidebarProps) {
  const {
    sessions,
    currentSessionId,
    isLoading,
    createSession,
    selectSession,
    deleteSession,
  } = useStore();

  const handleNewChat = async () => {
    await createSession();
  };

  const handleDeleteSession = async (e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this session?')) {
      await deleteSession(sessionId);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <aside className="w-72 bg-sidebar text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Image src="/logo.png" alt="SADNxAI Logo" width={32} height={32} />
            <span className="text-xl font-bold">SADNxAI</span>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="p-2 -mr-2 rounded-lg hover:bg-sidebar-light md:hidden min-h-[44px] min-w-[44px] flex items-center justify-center"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        <button
          onClick={handleNewChat}
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-primary hover:bg-primary/90 rounded-lg transition-colors disabled:opacity-50"
        >
          <Plus className="w-5 h-5" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Session List */}
      <div className="flex-1 overflow-y-auto p-2">
        {sessions.length === 0 ? (
          <div className="text-gray-500 text-center py-8 text-sm">
            No conversations yet.<br />Start by creating a new chat.
          </div>
        ) : (
          <div className="space-y-1">
            {sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => {
                  selectSession(session.id);
                  onClose?.(); // Close sidebar on mobile after selection
                }}
                className={`
                  group flex items-center gap-3 px-3 py-3 rounded-lg cursor-pointer transition-colors min-h-[48px]
                  ${currentSessionId === session.id
                    ? 'bg-sidebar-light'
                    : 'hover:bg-sidebar-border'
                  }
                `}
              >
                <MessageSquare className="w-4 h-4 text-gray-400 flex-shrink-0" />

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium truncate">
                      {session.title}
                    </span>
                    <span
                      className={`w-2 h-2 rounded-full flex-shrink-0 ${STATUS_COLORS[session.status] || 'bg-gray-400'}`}
                      title={session.status}
                    />
                  </div>
                  <div className="text-xs text-gray-500">
                    {formatDate(session.updated_at)}
                    {session.row_count > 0 && ` • ${session.row_count.toLocaleString()} rows`}
                  </div>
                </div>

                <button
                  onClick={(e) => handleDeleteSession(e, session.id)}
                  className="opacity-100 sm:opacity-0 sm:group-hover:opacity-100 p-2 -mr-1 hover:bg-sidebar-light/50 rounded transition-all min-h-[44px] min-w-[44px] flex items-center justify-center"
                  title="Delete session"
                >
                  <Trash2 className="w-4 h-4 text-gray-400" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border text-xs text-gray-500">
        <div>SADNxAI v1.0.0</div>
        <div>AI-Powered Data Anonymization</div>
      </div>
    </aside>
  );
}
