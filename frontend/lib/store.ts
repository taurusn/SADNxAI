/**
 * Global State Store using Zustand
 */

import { create } from 'zustand';
import { api, Session, SessionDetail, Message } from './api';

interface AppState {
  // Sessions
  sessions: Session[];
  currentSessionId: string | null;
  currentSession: SessionDetail | null;

  // UI State
  isLoading: boolean;
  isSending: boolean;
  error: string | null;
  pollingInterval: NodeJS.Timeout | null;

  // Actions
  loadSessions: () => Promise<void>;
  createSession: () => Promise<string>;
  selectSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  uploadFile: (file: File) => Promise<void>;
  sendMessage: (message: string) => Promise<void>;
  clearError: () => void;
  startPolling: () => void;
  stopPolling: () => void;
}

// Processing states that should trigger polling
const PROCESSING_STATES = ['analyzing', 'masking', 'validating', 'approved'];

export const useStore = create<AppState>((set, get) => ({
  // Initial state
  sessions: [],
  currentSessionId: null,
  currentSession: null,
  isLoading: false,
  isSending: false,
  error: null,
  pollingInterval: null,

  // Load all sessions
  loadSessions: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.listSessions();
      set({ sessions: response.sessions, isLoading: false });
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  // Create new session
  createSession: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.createSession();
      const sessionId = response.session_id;

      // Reload sessions list
      await get().loadSessions();

      // Select the new session
      await get().selectSession(sessionId);

      return sessionId;
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
      throw err;
    }
  },

  // Select and load a session
  selectSession: async (sessionId: string) => {
    // Stop any existing polling
    get().stopPolling();

    set({ isLoading: true, error: null, currentSessionId: sessionId });
    try {
      const session = await api.getSession(sessionId);
      set({ currentSession: session, isLoading: false });

      // Start polling if in processing state
      if (PROCESSING_STATES.includes(session.status)) {
        get().startPolling();
      }
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  // Delete a session
  deleteSession: async (sessionId: string) => {
    set({ isLoading: true, error: null });
    try {
      await api.deleteSession(sessionId);

      // Clear current session if it was deleted
      if (get().currentSessionId === sessionId) {
        set({ currentSessionId: null, currentSession: null });
      }

      // Reload sessions
      await get().loadSessions();
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  // Upload file to current session
  uploadFile: async (file: File) => {
    const sessionId = get().currentSessionId;
    if (!sessionId) {
      set({ error: 'No session selected' });
      return;
    }

    set({ isSending: true, error: null });
    try {
      const response = await api.uploadFile(sessionId, file);

      // Add messages to current session
      const currentSession = get().currentSession;
      if (currentSession) {
        const userMessage: Message = {
          role: 'user',
          content: `I've uploaded a file: ${file.name}`,
        };
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.ai_response,
        };

        set({
          currentSession: {
            ...currentSession,
            title: file.name,
            columns: response.columns,
            sample_data: response.sample_data,
            row_count: response.row_count,
            status: 'analyzing',
            messages: [...currentSession.messages, userMessage, assistantMessage],
          },
          isSending: false,
        });
      }

      // Reload full session to get updated state
      await get().selectSession(sessionId);
      await get().loadSessions();
    } catch (err) {
      set({ error: (err as Error).message, isSending: false });
    }
  },

  // Send chat message
  sendMessage: async (message: string) => {
    const sessionId = get().currentSessionId;
    if (!sessionId) {
      set({ error: 'No session selected' });
      return;
    }

    // Optimistically add user message
    const currentSession = get().currentSession;
    if (currentSession) {
      const userMessage: Message = { role: 'user', content: message };
      set({
        currentSession: {
          ...currentSession,
          messages: [...currentSession.messages, userMessage],
        },
        isSending: true,
        error: null,
      });
    }

    try {
      const response = await api.sendMessage(sessionId, message);

      // Update session with response
      const updatedSession = get().currentSession;
      if (updatedSession) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: response.response,
        };

        set({
          currentSession: {
            ...updatedSession,
            status: response.status,
            classification: response.classification || updatedSession.classification,
            messages: [...updatedSession.messages, assistantMessage],
          },
          isSending: false,
        });
      }

      // Reload full session to get complete state
      await get().selectSession(sessionId);
      await get().loadSessions();

      // Start polling if session is now in processing state
      const updatedSessionAfterReload = get().currentSession;
      if (updatedSessionAfterReload && PROCESSING_STATES.includes(updatedSessionAfterReload.status)) {
        get().startPolling();
      }
    } catch (err) {
      set({ error: (err as Error).message, isSending: false });
    }
  },

  // Clear error
  clearError: () => set({ error: null }),

  // Start polling for session updates (when in processing state)
  startPolling: () => {
    const existing = get().pollingInterval;
    if (existing) return; // Already polling

    const interval = setInterval(async () => {
      const sessionId = get().currentSessionId;
      const currentSession = get().currentSession;

      if (!sessionId || !currentSession) {
        get().stopPolling();
        return;
      }

      // Only poll if in a processing state
      if (!PROCESSING_STATES.includes(currentSession.status)) {
        get().stopPolling();
        return;
      }

      try {
        const session = await api.getSession(sessionId);
        set({ currentSession: session });

        // Stop polling if no longer in processing state
        if (!PROCESSING_STATES.includes(session.status)) {
          get().stopPolling();
          // Also refresh sessions list
          get().loadSessions();
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    }, 2000); // Poll every 2 seconds

    set({ pollingInterval: interval });
  },

  // Stop polling
  stopPolling: () => {
    const interval = get().pollingInterval;
    if (interval) {
      clearInterval(interval);
      set({ pollingInterval: null });
    }
  },
}));
