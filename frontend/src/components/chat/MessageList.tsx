/**
 * Список сообщений
 */

import { useEffect, useRef } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useAuthStore } from '../../store/authStore';
import { TypingIndicator } from './TypingIndicator';
import type { Message } from '../../types/chat';

interface MessageBubbleProps {
    message: Message;
    isOwn: boolean;
}

function MessageBubble({ message, isOwn }: MessageBubbleProps) {
    const time = new Date(message.created_at).toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit',
    });

    return (
        <div className={`flex ${isOwn ? 'justify-end' : 'justify-start'} mb-2`}>
            <div
                className={`max-w-[70%] rounded-2xl px-4 py-2 ${isOwn
                    ? 'bg-blue-500 text-white rounded-br-md'
                    : 'bg-gray-100 text-gray-900 rounded-bl-md'
                    }`}
            >
                {!isOwn && (
                    <p className="text-xs font-medium text-blue-600 mb-1">
                        {message.sender_name}
                    </p>
                )}
                <p className="whitespace-pre-wrap break-words">{message.content}</p>
                <div
                    className={`flex items-center justify-end gap-1 mt-1 text-xs ${isOwn ? 'text-blue-100' : 'text-gray-500'
                        }`}
                >
                    <span>{time}</span>
                    {message.is_edited && <span>(ред.)</span>}
                    {isOwn && (
                        <span>
                            {message.status === 'read' ? '✓✓' : message.status === 'delivered' ? '✓✓' : '✓'}
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
}

export function MessageList() {
    const { messages, currentChat, isLoadingMessages, hasMoreMessages, loadMessages } =
        useChatStore();
    const { user } = useAuthStore();
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleScroll = () => {
        if (!containerRef.current || !currentChat || isLoadingMessages || !hasMoreMessages) {
            return;
        }

        if (containerRef.current.scrollTop === 0) {
            loadMessages(currentChat.id, true);
        }
    };

    if (!currentChat) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
                <p className="text-lg">Выберите чат</p>
                <p className="text-sm mt-1">для начала общения</p>
            </div>
        );
    }

    return (
        <div
            ref={containerRef}
            onScroll={handleScroll}
            className="flex-1 overflow-y-auto p-4"
        >
            {isLoadingMessages && messages.length === 0 ? (
                <div className="flex items-center justify-center h-full">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                </div>
            ) : messages.length === 0 ? (
                <div className="flex items-center justify-center h-full text-gray-500">
                    <p>Нет сообщений. Начните диалог!</p>
                </div>
            ) : (
                <>
                    {hasMoreMessages && (
                        <div className="text-center mb-4">
                            <button
                                onClick={() => loadMessages(currentChat.id, true)}
                                disabled={isLoadingMessages}
                                className="text-blue-600 hover:text-blue-700 text-sm"
                            >
                                {isLoadingMessages ? 'Загрузка...' : 'Загрузить ранее'}
                            </button>
                        </div>
                    )}
                    {messages.map((message) => (
                        <MessageBubble
                            key={message.id}
                            message={message}
                            isOwn={message.sender_id === user?.id}
                        />
                    ))}
                    <TypingIndicator chatId={currentChat.id} />
                    <div ref={messagesEndRef} />
                </>
            )}
        </div>
    );
}
