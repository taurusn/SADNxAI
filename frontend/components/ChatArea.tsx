'use client';

import { useRef, useEffect } from 'react';
import { useStore } from '@/lib/store';
import { api } from '@/lib/api';
import MessageInput from './MessageInput';
import FileUpload from './FileUpload';
import ReactMarkdown from 'react-markdown';
import { Download, FileText, CheckCircle, XCircle, AlertCircle, Loader2, Wrench, Sparkles, Menu } from 'lucide-react';

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
  const { currentSession, currentSessionId, isSending, streamingContent, streamingStatus, currentTool, pendingMessages, toggleSidebar } = useStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages, streaming content, or pending messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentSession?.messages, streamingContent, pendingMessages]);

  if (!currentSession) {
    return (
      <div className="flex-1 flex flex-col h-full bg-gray-50">
        {/* Mobile header for welcome screen */}
        <div className="flex md:hidden items-center justify-between px-4 py-3 border-b border-gray-200 bg-white">
          <button
            onClick={toggleSidebar}
            className="p-2 -ml-2 rounded-lg hover:bg-gray-100 min-h-[44px] min-w-[44px] flex items-center justify-center"
          >
            <Menu className="w-6 h-6" />
          </button>
          <span className="font-semibold text-gray-900">SADNxAI</span>
          <div className="w-10" />
        </div>

        <div className="flex-1 flex items-center justify-center">
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
            <div className="text-sm text-gray-500 hidden md:block">
              Select an existing chat from the sidebar or create a new one.
            </div>
            <button
              onClick={toggleSidebar}
              className="md:hidden mt-2 px-4 py-3 bg-primary text-white rounded-lg min-h-[44px]"
            >
              Open Menu
            </button>
          </div>
        </div>
      </div>
    );
  }

  const status = STATUS_BADGES[currentSession.status] || STATUS_BADGES.idle;
  const StatusIcon = status.icon;

  return (
    <div className="flex-1 flex flex-col h-full">
      {/* Mobile header - only visible on mobile */}
      <div className="flex md:hidden items-center justify-between px-4 py-3 border-b border-gray-200 bg-white">
        <button
          onClick={toggleSidebar}
          className="p-2 -ml-2 rounded-lg hover:bg-gray-100 min-h-[44px] min-w-[44px] flex items-center justify-center"
        >
          <Menu className="w-6 h-6" />
        </button>
        <span className="font-semibold text-gray-900">SADNxAI</span>
        <div className="w-10" /> {/* Spacer for centering */}
      </div>

      {/* Desktop Header - hidden on mobile */}
      <header className="hidden md:flex items-center justify-between px-6 py-3 border-b bg-white">
        <div className="flex items-center gap-3">
          <h1 className="font-semibold text-gray-800 truncate max-w-md">
            {currentSession.title}
          </h1>
          <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${status.color}`}>
            <StatusIcon className="w-3 h-3" />
            {status.label}
          </span>
        </div>

        {/* Download buttons - show for both completed and failed (with output available) */}
        {(currentSession.status === 'completed' || currentSession.status === 'failed') && currentSession.output_path && (
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
            <a
              href={api.getDataDownloadUrl(currentSession.id)}
              className="flex items-center justify-center gap-2 px-4 py-2 min-h-[44px] bg-primary text-white text-sm rounded-lg hover:bg-primary/90 transition-colors"
            >
              <Download className="w-4 h-4" />
              <span>CSV</span>
            </a>
            {currentSession.report_path && (
              <a
                href={api.getReportDownloadUrl(currentSession.id)}
                className="flex items-center justify-center gap-2 px-4 py-2 min-h-[44px] bg-gray-800 text-white text-sm rounded-lg hover:bg-gray-700 transition-colors"
              >
                <FileText className="w-4 h-4" />
                <span>Report</span>
              </a>
            )}
          </div>
        )}
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4 md:px-6 space-y-4">
        {currentSession.messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <FileUpload />
          </div>
        ) : (
          <>
            {currentSession.messages
              .filter((msg) => (msg.role === 'user' || msg.role === 'assistant') && msg.content?.trim())
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

            {/* Pending messages from completed iterations - show accumulated context */}
            {isSending && pendingMessages.length > 0 && (
              <div className="flex justify-start message-enter">
                <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm max-w-2xl">
                  <div className="prose prose-sm max-w-none space-y-2">
                    {pendingMessages.map((content, idx) => (
                      <div key={`pending-${idx}`} className="text-gray-700">
                        <ReactMarkdown>{content}</ReactMarkdown>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Current streaming / status indicator */}
            {isSending && (
              <div className="flex justify-start message-enter">
                <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm max-w-2xl">
                  {/* Currently streaming content */}
                  {streamingContent && (
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown>{streamingContent}</ReactMarkdown>
                      {streamingStatus === 'streaming' && (
                        <span className="inline-block w-1.5 h-4 bg-primary animate-pulse ml-0.5 align-text-bottom" />
                      )}
                    </div>
                  )}

                  {/* Thinking indicator */}
                  {!streamingContent && streamingStatus === 'thinking' && (
                    <div className="flex items-center gap-2 text-primary">
                      <Sparkles className="w-4 h-4 animate-pulse" />
                      <span className="text-sm">Thinking...</span>
                    </div>
                  )}

                  {/* Tool execution indicator - always show when status is 'tool' */}
                  {streamingStatus === 'tool' && (
                    <div className="flex items-center gap-2 text-amber-600">
                      <Wrench className="w-4 h-4 animate-spin" />
                      <span className="text-sm">
                        {currentTool ? `Executing: ${currentTool}` : 'Executing tool...'}
                      </span>
                    </div>
                  )}

                  {/* Pipeline indicator */}
                  {streamingStatus === 'pipeline' && (
                    <div className="flex items-center gap-2 text-purple-600">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">{streamingContent || 'Running pipeline...'}</span>
                    </div>
                  )}

                  {/* Loading dots - fallback when waiting for response */}
                  {!streamingContent && !streamingStatus && (
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full loading-dot" />
                      <span className="w-2 h-2 bg-gray-400 rounded-full loading-dot" />
                      <span className="w-2 h-2 bg-gray-400 rounded-full loading-dot" />
                    </div>
                  )}
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Validation Result Card */}
      {currentSession.validation_result && (
        <div className="mx-4 mb-4 md:mx-6">
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
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 sm:gap-3 text-sm">
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
      <div className="border-t bg-white px-4 py-3 md:px-6 md:py-4 pb-safe-bottom">
        <MessageInput />
      </div>
    </div>
  );
}
