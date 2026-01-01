/**
 * API Client for SADNxAI Chat Service
 */

// Use relative path for production (Cloudflare Tunnel), absolute for local dev
const API_URL = process.env.NEXT_PUBLIC_API_URL || (typeof window !== 'undefined' && window.location.hostname !== 'localhost' ? '/api' : 'http://localhost:8000/api');

export interface Session {
  id: string;
  title: string;
  status: string;
  created_at: string;
  updated_at: string;
  row_count: number;
  has_classification: boolean;
  has_validation: boolean;
}

export interface Message {
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string | null;
  tool_calls?: any[];
  tool_call_id?: string;
}

export interface Classification {
  direct_identifiers: string[];
  quasi_identifiers: string[];
  linkage_identifiers: string[];
  date_columns: string[];
  sensitive_attributes: string[];
  recommended_techniques: Record<string, string>;
  reasoning: Record<string, string>;
}

export interface UploadResponse {
  columns: string[];
  sample_data: Record<string, any>[];
  row_count: number;
  ai_response: string;
}

export interface ChatResponse {
  response: string;
  status: string;
  classification?: Classification;
}

export interface StreamEvent {
  type: 'thinking' | 'tool_call' | 'tool_result' | 'message' | 'text_delta' | 'terminal_tool' | 'pipeline_start' | 'pipeline_masking' | 'file_info' | 'done';
  content?: string;
  tool?: string;
  args?: any;
  success?: boolean;
  status?: string;
  message?: string;
  has_classification?: boolean;
  has_validation?: boolean;
  // File info fields
  columns?: string[];
  row_count?: number;
  filename?: string;
}

export interface SessionDetail {
  id: string;
  title: string;
  status: string;
  file_path: string | null;
  columns: string[];
  sample_data: Record<string, any>[];
  row_count: number;
  classification: Classification | null;
  thresholds: any;
  validation_result: any;
  messages: Message[];
  output_path: string | null;
  report_path: string | null;
  created_at: string;
  updated_at: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Session endpoints
  async createSession(): Promise<{ session_id: string }> {
    return this.request('/sessions', { method: 'POST' });
  }

  async listSessions(): Promise<{ sessions: Session[] }> {
    return this.request('/sessions');
  }

  async getSession(sessionId: string): Promise<SessionDetail> {
    return this.request(`/sessions/${sessionId}`);
  }

  async deleteSession(sessionId: string): Promise<{ deleted: boolean }> {
    return this.request(`/sessions/${sessionId}`, { method: 'DELETE' });
  }

  // File upload with SSE streaming
  async uploadFileStream(
    sessionId: string,
    file: File,
    onEvent: (event: StreamEvent) => void
  ): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    const url = `${this.baseUrl}/sessions/${sessionId}/upload`;
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(error.detail);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            onEvent(data as StreamEvent);
          } catch (e) {
            console.error('Failed to parse SSE event:', line);
          }
        }
      }
    }

    // Process any remaining buffer content after stream ends
    if (buffer.trim() && buffer.startsWith('data: ')) {
      try {
        const data = JSON.parse(buffer.slice(6));
        onEvent(data as StreamEvent);
      } catch (e) {
        console.error('Failed to parse final SSE event:', buffer);
      }
    }
  }

  // Chat with SSE streaming
  async sendMessageStream(
    sessionId: string,
    message: string,
    onEvent: (event: StreamEvent) => void
  ): Promise<void> {
    const url = `${this.baseUrl}/sessions/${sessionId}/chat`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            onEvent(data as StreamEvent);
          } catch (e) {
            console.error('Failed to parse SSE event:', line);
          }
        }
      }
    }

    // Process any remaining buffer content after stream ends
    if (buffer.trim() && buffer.startsWith('data: ')) {
      try {
        const data = JSON.parse(buffer.slice(6));
        onEvent(data as StreamEvent);
      } catch (e) {
        console.error('Failed to parse final SSE event:', buffer);
      }
    }
  }

  // Legacy non-streaming chat (kept for compatibility)
  async sendMessage(sessionId: string, message: string): Promise<ChatResponse> {
    return this.request(`/sessions/${sessionId}/chat`, {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // Thresholds
  async updateThresholds(sessionId: string, thresholds: any): Promise<any> {
    return this.request(`/sessions/${sessionId}/thresholds`, {
      method: 'PATCH',
      body: JSON.stringify(thresholds),
    });
  }

  // Downloads
  getDataDownloadUrl(sessionId: string): string {
    return `${this.baseUrl}/sessions/${sessionId}/download/data`;
  }

  getReportDownloadUrl(sessionId: string): string {
    return `${this.baseUrl}/sessions/${sessionId}/download/report`;
  }
}

export const api = new ApiClient();
