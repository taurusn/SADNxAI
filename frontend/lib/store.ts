/**
 * Global State Store using Zustand
 * Uses WebSocket for real-time chat communication
 */

import { create } from 'zustand';
import { api, Session, SessionDetail, Message, StreamEvent } from './api';
import { wsManager, ServerMessage } from './websocket';

interface AppState {
  // Sessions
  sessions: Session[];
  currentSessionId: string | null;
  currentSession: SessionDetail | null;

  // UI State
  isLoading: boolean;
  isSending: boolean;
  error: string | null;
  sidebarOpen: boolean;
  wsConnected: boolean;

  // Streaming State
  streamingContent: string;
  streamingStatus: string | null;
  currentTool: string | null;
  pendingMessages: string[];

  // Actions
  loadSessions: () => Promise<void>;
  createSession: () => Promise<string>;
  selectSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  uploadFile: (file: File) => Promise<void>;
  sendMessage: (message: string) => Promise<void>;
  clearError: () => void;
  toggleSidebar: () => void;
  closeSidebar: () => void;
}

export const useStore = create<AppState>((set, get) => ({
  // Initial state
  sessions: [],
  currentSessionId: null,
  currentSession: null,
  isLoading: false,
  isSending: false,
  error: null,
  sidebarOpen: false,
  wsConnected: false,
  streamingContent: '',
  streamingStatus: null,
  currentTool: null,
  pendingMessages: [],

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

  // Select and load a session via WebSocket
  selectSession: async (sessionId: string) => {
    set({
      isLoading: true,
      error: null,
      currentSessionId: sessionId,
      currentSession: null, // Clear current session while loading
      wsConnected: false,
    });

    try {
      // Set up WebSocket event handlers BEFORE connecting
      // This clears old handlers and sets up new ones
      setupWebSocketHandlers(set, get);

      // Connect to WebSocket - this closes any previous connection
      // but preserves our newly set up handlers
      await wsManager.connect(sessionId);

      set({ wsConnected: true });

      // Request fresh session state to ensure we have it
      wsManager.refreshSession();

    } catch (err) {
      console.error('[Store] WebSocket connection failed, falling back to REST:', err);

      // Fallback to REST API
      try {
        const session = await api.getSession(sessionId);
        set({ currentSession: session, isLoading: false, wsConnected: false });
      } catch (restErr) {
        set({ error: (restErr as Error).message, isLoading: false });
      }
    }
  },

  // Delete a session
  deleteSession: async (sessionId: string) => {
    set({ isLoading: true, error: null });
    try {
      // Disconnect WebSocket if deleting current session
      if (get().currentSessionId === sessionId) {
        wsManager.disconnect();
        set({ currentSessionId: null, currentSession: null, wsConnected: false });
      }

      await api.deleteSession(sessionId);
      await get().loadSessions();
    } catch (err) {
      set({ error: (err as Error).message, isLoading: false });
    }
  },

  // Upload file to current session (still uses REST + SSE for file upload)
  uploadFile: async (file: File) => {
    const sessionId = get().currentSessionId;
    if (!sessionId) {
      set({ error: 'No session selected' });
      return;
    }

    // Add user message immediately
    const currentSession = get().currentSession;
    if (currentSession) {
      const userMessage: Message = { role: 'user', content: `I've uploaded a file: ${file.name}` };
      set({
        currentSession: {
          ...currentSession,
          title: file.name,
          messages: [...currentSession.messages, userMessage],
        },
        isSending: true,
        streamingContent: '',
        streamingStatus: 'thinking',
        currentTool: null,
        error: null,
      });
    }

    try {
      let finalContent = '';
      let fileInfo: { columns?: string[], row_count?: number } = {};

      await api.uploadFileStream(sessionId, file, (event: StreamEvent) => {
        const session = get().currentSession;
        if (!session) return;

        switch (event.type) {
          case 'file_info':
            fileInfo = { columns: event.columns, row_count: event.row_count };
            set({
              currentSession: {
                ...session,
                columns: event.columns || [],
                row_count: event.row_count || 0,
                status: 'analyzing',
              },
            });
            break;

          case 'thinking':
            set({ streamingStatus: 'thinking', streamingContent: '' });
            break;

          case 'text_delta':
            set((state) => ({
              streamingStatus: 'streaming',
              streamingContent: state.streamingContent + (event.content || ''),
            }));
            break;

          case 'tool_call':
          case 'terminal_tool':
            set((state) => ({
              streamingStatus: 'tool',
              currentTool: event.tool || null,
              pendingMessages: state.streamingContent
                ? [...state.pendingMessages, state.streamingContent]
                : state.pendingMessages,
              streamingContent: '',
            }));
            break;

          case 'tool_result':
            set({ streamingStatus: 'thinking', currentTool: null });
            break;

          case 'message':
            finalContent = event.content || '';
            set({ streamingStatus: 'streaming', streamingContent: finalContent });
            break;

          case 'done':
            const assistantMessage: Message = {
              role: 'assistant',
              content: finalContent,
            };

            set({
              currentSession: {
                ...session,
                status: event.status || session.status,
                messages: [...session.messages, assistantMessage],
              },
              isSending: false,
              streamingStatus: null,
              streamingContent: '',
              currentTool: null,
              pendingMessages: [],
            });
            break;
        }
      });

      // Refresh session via WebSocket after upload
      if (wsManager.isConnected()) {
        wsManager.refreshSession();
      }
      await get().loadSessions();

    } catch (err) {
      set({
        error: (err as Error).message,
        isSending: false,
        streamingStatus: null,
        streamingContent: '',
        currentTool: null,
      });
    }
  },

  // Send chat message via WebSocket
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
        streamingContent: '',
        streamingStatus: 'thinking',
        currentTool: null,
        error: null,
      });
    }

    // Send via WebSocket if connected
    if (wsManager.isConnected()) {
      wsManager.sendChat(message);
      // Response handled by WebSocket event handlers
    } else {
      // Fallback to SSE
      console.log('[Store] WebSocket not connected, falling back to SSE');
      try {
        let finalContent = '';

        await api.sendMessageStream(sessionId, message, (event: StreamEvent) => {
          const session = get().currentSession;
          if (!session) return;

          switch (event.type) {
            case 'thinking':
              set({ streamingStatus: 'thinking', streamingContent: '' });
              break;

            case 'text_delta':
              set((state) => ({
                streamingStatus: 'streaming',
                streamingContent: state.streamingContent + (event.content || ''),
              }));
              break;

            case 'tool_call':
            case 'terminal_tool':
              set((state) => ({
                streamingStatus: 'tool',
                currentTool: event.tool || null,
                pendingMessages: state.streamingContent
                  ? [...state.pendingMessages, state.streamingContent]
                  : state.pendingMessages,
                streamingContent: '',
              }));
              break;

            case 'tool_result':
              set({ streamingStatus: 'thinking', currentTool: null });
              break;

            case 'pipeline_start':
            case 'pipeline_masking':
              set({ streamingStatus: 'pipeline', streamingContent: event.message || 'Running pipeline...' });
              break;

            case 'message':
              finalContent = event.content || '';
              set({ streamingStatus: 'streaming', streamingContent: finalContent });
              break;

            case 'done':
              const newMessages = finalContent.trim()
                ? [...session.messages, { role: 'assistant' as const, content: finalContent }]
                : session.messages;

              set({
                currentSession: {
                  ...session,
                  status: event.status || session.status,
                  messages: newMessages,
                },
                isSending: false,
                streamingStatus: null,
                streamingContent: '',
                currentTool: null,
                pendingMessages: [],
              });
              break;
          }
        });

        await get().loadSessions();

      } catch (err) {
        set({
          error: (err as Error).message,
          isSending: false,
          streamingStatus: null,
          streamingContent: '',
          currentTool: null,
        });
      }
    }
  },

  // Clear error
  clearError: () => set({ error: null }),

  // Sidebar toggle for mobile
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  closeSidebar: () => set({ sidebarOpen: false }),
}));


/**
 * Set up WebSocket event handlers
 * Called when connecting to a new session
 */
function setupWebSocketHandlers(
  set: (partial: Partial<AppState> | ((state: AppState) => Partial<AppState>)) => void,
  get: () => AppState
) {
  // Clear any existing handlers to prevent duplicates
  wsManager.clearHandlers();

  // Connection state
  wsManager.onConnection((connected) => {
    set({ wsConnected: connected });
    if (!connected) {
      console.log('[Store] WebSocket disconnected');
    }
  });

  // Session state updates
  wsManager.on('session', (msg: ServerMessage) => {
    const sessionData = msg.payload;
    set({
      currentSession: sessionData as SessionDetail,
      isLoading: false,
    });
  });

  // Connected event
  wsManager.on('connected', (msg: ServerMessage) => {
    console.log('[Store] WebSocket connected to session:', msg.payload.session_id);
    set({ isLoading: false });
  });

  // Thinking indicator
  wsManager.on('thinking', () => {
    set({ streamingStatus: 'thinking', streamingContent: '' });
  });

  // Token streaming
  wsManager.on('token', (msg: ServerMessage) => {
    set((state) => ({
      streamingStatus: 'streaming',
      streamingContent: state.streamingContent + (msg.payload.content || ''),
    }));
  });

  // Tool execution start
  wsManager.on('tool_start', (msg: ServerMessage) => {
    set((state) => ({
      streamingStatus: 'tool',
      currentTool: msg.payload.tool || null,
      pendingMessages: state.streamingContent
        ? [...state.pendingMessages, state.streamingContent]
        : state.pendingMessages,
      streamingContent: '',
    }));
  });

  // Tool execution end
  wsManager.on('tool_end', () => {
    set({ streamingStatus: 'thinking', currentTool: null });
  });

  // Pipeline events
  wsManager.on('pipeline_start', (msg: ServerMessage) => {
    set({
      streamingStatus: 'pipeline',
      streamingContent: msg.payload.message || 'Starting pipeline...',
    });
  });

  wsManager.on('pipeline_progress', (msg: ServerMessage) => {
    set({
      streamingStatus: 'pipeline',
      streamingContent: msg.payload.message || 'Running pipeline...',
    });
  });

  // Final message content
  wsManager.on('message', (msg: ServerMessage) => {
    const content = msg.payload.content || '';
    set({
      streamingStatus: 'streaming',
      streamingContent: content,
    });
  });

  // Done event - finalize the response
  // NOTE: Don't add message here - the 'session' event already brought messages from Redis
  wsManager.on('done', (msg: ServerMessage) => {
    const session = get().currentSession;

    // Just update status, don't add messages (already in session from 'session' event)
    if (session) {
      set({
        currentSession: {
          ...session,
          status: msg.payload.status || session.status,
        },
      });
    }

    set({
      isSending: false,
      streamingStatus: null,
      streamingContent: '',
      currentTool: null,
      pendingMessages: [],
    });

    // Refresh sessions list
    get().loadSessions();
  });

  // Error handling
  wsManager.on('error', (msg: ServerMessage) => {
    console.error('[Store] WebSocket error:', msg.payload.message);
    set({
      error: msg.payload.message,
      isSending: false,
      streamingStatus: null,
    });
  });
}
