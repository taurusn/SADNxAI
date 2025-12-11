'use client';

import { useRef, useEffect } from 'react';
import { useStore } from '@/lib/store';
import { api } from '@/lib/api';
import MessageInput from './MessageInput';
import FileUpload from './FileUpload';
import ReactMarkdown from 'react-markdown';
import { Download, FileText, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

const STATUS_BADGES: Record<string, { label: string; color: string; icon: any }> = {
  idle: { label: 'Ready', color: 'bg-gray-100 text-gray-600', icon: AlertCircle },
  analyzing: { label: 'Analyzing', color: 'bg-yellow-100 text-yellow-700', icon: AlertCircle },
  proposed: { label: 'Review Plan', color: 'bg-amber-100 text-amber-800', icon: AlertCircle },
  discussing: { label: 'Discussing', color: 'bg-amber-100 text-amber-800', icon: AlertCircle },
  approved: { label: 'Approved', color: 'bg-purple-100 text-purple-700', icon: CheckCircle },
  masking: { label: 'Processing', color: 'bg-orange-100 text-orange-700', icon: AlertCircle },
  validating: { label: 'Validating', color: 'bg-orange-100 text-orange-700', icon: AlertCircle },
  completed: { label: 'Completed', color: 'bg-green-100 text-green-700', icon: CheckCircle },
  failed: { label: 'Failed', color: 'bg-red-100 text-red-700', icon: XCircle },
};

export default function ChatArea() {
  const { currentSession, currentSessionId, isSending } = useStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentSession?.messages]);

  if (!currentSession) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md px-4">
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <FileText className="w-8 h-8 text-primary" />
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Welcome to SADNxAI
          </h2>
          <p className="text-gray-600 mb-6">
            Start a new chat to anonymize your data. Upload a CSV file and our AI Privacy Consultant will guide you through the process.
          </p>
          <div className="text-sm text-gray-500">
            Select an existing chat from the sidebar or create a new one.
          </div>
        </div>
      </div>
    );
  }

  const status = STATUS_BADGES[currentSession.status] || STATUS_BADGES.idle;
  const StatusIcon = status.icon;

  return (
    <div className="flex-1 flex flex-col h-full">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-3 border-b bg-white">
        <div className="flex items-center gap-3">
          <h1 className="font-semibold text-gray-800 truncate max-w-md">
            {currentSession.title}
          </h1>
          <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${status.color}`}>
            <StatusIcon className="w-3 h-3" />
            {status.label}
          </span>
        </div>

        {/* Download buttons */}
        {currentSession.status === 'completed' && (
          <div className="flex items-center gap-2">
            <a
              href={api.getDataDownloadUrl(currentSession.id)}
              className="flex items-center gap-2 px-3 py-1.5 bg-primary text-white text-sm rounded-lg hover:bg-primary/90 transition-colors"
            >
              <Download className="w-4 h-4" />
              Download CSV
            </a>
            <a
              href={api.getReportDownloadUrl(currentSession.id)}
              className="flex items-center gap-2 px-3 py-1.5 bg-gray-800 text-white text-sm rounded-lg hover:bg-gray-700 transition-colors"
            >
              <FileText className="w-4 h-4" />
              Download Report
            </a>
          </div>
        )}
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {currentSession.messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <FileUpload />
          </div>
        ) : (
          <>
            {currentSession.messages
              .filter((msg) => msg.role === 'user' || msg.role === 'assistant')
              .map((message, index) => (
                <div
                  key={index}
                  className={`flex message-enter ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-2xl px-4 py-3 rounded-2xl ${
                      message.role === 'user'
                        ? 'bg-primary text-white rounded-br-md'
                        : 'bg-white border border-gray-200 rounded-bl-md shadow-sm'
                    }`}
                  >
                    {message.role === 'assistant' ? (
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown>{message.content || ''}</ReactMarkdown>
                      </div>
                    ) : (
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    )}
                  </div>
                </div>
              ))}

            {/* Loading indicator */}
            {isSending && (
              <div className="flex justify-start message-enter">
                <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-gray-400 rounded-full loading-dot" />
                    <span className="w-2 h-2 bg-gray-400 rounded-full loading-dot" />
                    <span className="w-2 h-2 bg-gray-400 rounded-full loading-dot" />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Validation Result Card */}
      {currentSession.validation_result && (
        <div className="mx-6 mb-4">
          <div className={`p-4 rounded-lg border ${
            currentSession.validation_result.passed
              ? 'bg-green-50 border-green-200'
              : 'bg-red-50 border-red-200'
          }`}>
            <div className="flex items-center gap-2 mb-3">
              {currentSession.validation_result.passed ? (
                <CheckCircle className="w-5 h-5 text-green-600" />
              ) : (
                <XCircle className="w-5 h-5 text-red-600" />
              )}
              <span className={`font-semibold ${
                currentSession.validation_result.passed ? 'text-green-700' : 'text-red-700'
              }`}>
                Validation {currentSession.validation_result.passed ? 'Passed' : 'Failed'}
              </span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
              {Object.entries(currentSession.validation_result.metrics).map(([name, metric]: [string, any]) => (
                <div key={name} className="bg-white/50 p-2 rounded">
                  <div className="text-gray-600 text-xs uppercase">{name.replace('_', '-')}</div>
                  <div className={`font-mono font-semibold ${metric.passed ? 'text-green-600' : 'text-red-600'}`}>
                    {typeof metric.value === 'number' ? metric.value.toFixed(2) : metric.value}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t bg-white px-6 py-4">
        <MessageInput />
      </div>
    </div>
  );
}
