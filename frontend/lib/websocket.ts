/**
 * WebSocket Manager for SADNxAI
 * Handles real-time communication with the chat service
 */

// Determine WebSocket URL based on environment
const getWsUrl = (): string => {
  if (typeof window === 'undefined') return '';

  const isProduction = window.location.hostname !== 'localhost';

  if (isProduction) {
    // In production, use relative path with wss://
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${window.location.host}/api/ws`;
  }

  // Local development
  return 'ws://localhost:8000/api/ws';
};

export interface ServerMessage {
  type:
    | 'connected'
    | 'session'
    | 'token'
    | 'thinking'
    | 'tool_start'
    | 'tool_end'
    | 'pipeline_start'
    | 'pipeline_progress'
    | 'message'
    | 'done'
    | 'error'
    | 'pong'
    | 'ping';
  payload: Record<string, any>;
  id?: string;
  timestamp: number;
}

export interface ClientMessage {
  type: 'chat' | 'ping' | 'get_session';
  payload: Record<string, any>;
  id: string;
}

type MessageHandler = (message: ServerMessage) => void;
type ConnectionHandler = (connected: boolean) => void;

interface PendingRequest {
  resolve: (message: ServerMessage) => void;
  reject: (error: Error) => void;
  timeout: NodeJS.Timeout;
}

class WebSocketManager {
  private ws: WebSocket | null = null;
  private sessionId: string | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private connectionHandlers: Set<ConnectionHandler> = new Set();
  private pendingRequests: Map<string, PendingRequest> = new Map();
  private messageQueue: ClientMessage[] = [];
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private pingInterval: NodeJS.Timeout | null = null;
  private isConnecting = false;
  private shouldReconnect = true;

  /**
   * Connect to a session's WebSocket
   */
  connect(sessionId: string): Promise<void> {
    return new Promise((resolve, reject) => {
      // Don't reconnect if already connected to same session
      if (this.sessionId === sessionId && this.ws?.readyState === WebSocket.OPEN) {
        resolve();
        return;
      }

      // Disconnect from previous session
      if (this.sessionId && this.sessionId !== sessionId) {
        this.disconnect();
      }

      this.sessionId = sessionId;
      this.shouldReconnect = true;
      this.isConnecting = true;

      const wsUrl = `${getWsUrl()}/${sessionId}`;
      console.log(`[WS] Connecting to ${wsUrl}`);

      try {
        this.ws = new WebSocket(wsUrl);
      } catch (error) {
        this.isConnecting = false;
        reject(error);
        return;
      }

      this.ws.onopen = () => {
        console.log('[WS] Connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.flushQueue();
        this.startHeartbeat();
        this.notifyConnectionHandlers(true);
        resolve();
      };

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as ServerMessage;
          this.handleMessage(message);
        } catch (error) {
          console.error('[WS] Failed to parse message:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log(`[WS] Disconnected: code=${event.code}, reason=${event.reason}`);
        this.isConnecting = false;
        this.stopHeartbeat();
        this.notifyConnectionHandlers(false);

        // Attempt reconnection if not intentionally closed
        if (this.shouldReconnect && event.code !== 1000) {
          this.attemptReconnect();
        }
      };

      this.ws.onerror = (error) => {
        console.error('[WS] Error:', error);
        if (this.isConnecting) {
          this.isConnecting = false;
          reject(new Error('WebSocket connection failed'));
        }
      };
    });
  }

  /**
   * Disconnect from the current session
   */
  disconnect(): void {
    console.log('[WS] Disconnecting');
    this.shouldReconnect = false;
    this.stopHeartbeat();
    this.clearReconnectTimeout();

    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }

    this.sessionId = null;
    this.messageQueue = [];
    this.clearPendingRequests();
    this.clearHandlers();
  }

  /**
   * Clear all event handlers
   */
  clearHandlers(): void {
    this.handlers.clear();
    this.connectionHandlers.clear();
  }

  /**
   * Send a chat message
   */
  sendChat(message: string): string {
    const id = this.generateId();
    this.send({
      type: 'chat',
      payload: { message },
      id,
    });
    return id;
  }

  /**
   * Send a message and wait for response
   */
  async sendAndWait(message: ClientMessage, timeoutMs = 30000): Promise<ServerMessage> {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(message.id);
        reject(new Error('Request timeout'));
      }, timeoutMs);

      this.pendingRequests.set(message.id, { resolve, reject, timeout });
      this.send(message);
    });
  }

  /**
   * Request fresh session state
   */
  refreshSession(): string {
    const id = this.generateId();
    this.send({
      type: 'get_session',
      payload: {},
      id,
    });
    return id;
  }

  /**
   * Register a handler for a specific message type
   */
  on(type: string, handler: MessageHandler): () => void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)!.add(handler);

    // Return unsubscribe function
    return () => {
      this.handlers.get(type)?.delete(handler);
    };
  }

  /**
   * Register a handler for all messages
   */
  onAny(handler: MessageHandler): () => void {
    return this.on('*', handler);
  }

  /**
   * Register a connection state handler
   */
  onConnection(handler: ConnectionHandler): () => void {
    this.connectionHandlers.add(handler);
    return () => {
      this.connectionHandlers.delete(handler);
    };
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  /**
   * Get current session ID
   */
  getSessionId(): string | null {
    return this.sessionId;
  }

  // Private methods

  private send(message: ClientMessage): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      // Queue message for when connection is restored
      this.messageQueue.push(message);
      console.log('[WS] Message queued (not connected)');
    }
  }

  private handleMessage(message: ServerMessage): void {
    // Handle pong for heartbeat
    if (message.type === 'pong') {
      return;
    }

    // Handle server ping
    if (message.type === 'ping') {
      this.send({ type: 'ping', payload: {}, id: this.generateId() });
      return;
    }

    // Check for pending request
    if (message.id && this.pendingRequests.has(message.id)) {
      const pending = this.pendingRequests.get(message.id)!;
      clearTimeout(pending.timeout);
      this.pendingRequests.delete(message.id);

      if (message.type === 'error') {
        pending.reject(new Error(message.payload.message || 'Request failed'));
      } else {
        pending.resolve(message);
      }
    }

    // Emit to specific type handlers
    const typeHandlers = this.handlers.get(message.type);
    if (typeHandlers) {
      typeHandlers.forEach((handler) => {
        try {
          handler(message);
        } catch (error) {
          console.error(`[WS] Handler error for ${message.type}:`, error);
        }
      });
    }

    // Emit to wildcard handlers
    const wildcardHandlers = this.handlers.get('*');
    if (wildcardHandlers) {
      wildcardHandlers.forEach((handler) => {
        try {
          handler(message);
        } catch (error) {
          console.error('[WS] Wildcard handler error:', error);
        }
      });
    }
  }

  private flushQueue(): void {
    while (this.messageQueue.length > 0 && this.ws?.readyState === WebSocket.OPEN) {
      const message = this.messageQueue.shift()!;
      this.ws.send(JSON.stringify(message));
    }
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('[WS] Max reconnect attempts reached');
      return;
    }

    // Exponential backoff: 1s, 2s, 4s, 8s, ... up to 30s
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;

    console.log(`[WS] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    this.reconnectTimeout = setTimeout(() => {
      if (this.sessionId && this.shouldReconnect) {
        this.connect(this.sessionId).catch((error) => {
          console.error('[WS] Reconnect failed:', error);
        });
      }
    }, delay);
  }

  private clearReconnectTimeout(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }

  private startHeartbeat(): void {
    this.stopHeartbeat();
    this.pingInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.send({ type: 'ping', payload: {}, id: this.generateId() });
      }
    }, 30000);
  }

  private stopHeartbeat(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  private notifyConnectionHandlers(connected: boolean): void {
    this.connectionHandlers.forEach((handler) => {
      try {
        handler(connected);
      } catch (error) {
        console.error('[WS] Connection handler error:', error);
      }
    });
  }

  private clearPendingRequests(): void {
    this.pendingRequests.forEach((pending) => {
      clearTimeout(pending.timeout);
      pending.reject(new Error('Connection closed'));
    });
    this.pendingRequests.clear();
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Export singleton instance
export const wsManager = new WebSocketManager();
