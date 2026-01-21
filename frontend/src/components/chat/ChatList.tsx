/**
 * Список чатов
 */

import { useEffect } from 'react';
import { useChatStore } from '../../store/chatStore';
import type { Chat } from '../../types/chat';

interface ChatListItemProps {
    chat: Chat;
    isActive: boolean;
    onClick: () => void;
}

function ChatListItem({ chat, isActive, onClick }: ChatListItemProps) {
    const displayName = chat.name || 'Без имени';
    const lastMessageText = chat.last_message?.content || 'Нет сообщений';
    const lastMessageTime = chat.last_message
        ? new Date(chat.last_message.created_at).toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit',
        })
        : '';

    return (
        <button
            onClick={onClick}
            className={`w-full p-3 flex items-center gap-3 hover:bg-gray-100 transition-colors text-left ${isActive ? 'bg-blue-50 border-r-2 border-blue-500' : ''
                }`}
        >
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold text-lg flex-shrink-0">
                {displayName[0]?.toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-900 truncate">{displayName}</span>
                    <span className="text-xs text-gray-500 flex-shrink-0">{lastMessageTime}</span>
                </div>
                <div className="flex items-center justify-between mt-0.5">
                    <span className="text-sm text-gray-500 truncate">{lastMessageText}</span>
                    {chat.unread_count > 0 && (
                        <span className="bg-blue-500 text-white text-xs rounded-full px-2 py-0.5 ml-2 flex-shrink-0">
                            {chat.unread_count}
                        </span>
                    )}
                </div>
            </div>
        </button>
    );
}

export function ChatList() {
    const { chats, currentChat, isLoading, loadChats, selectChat } = useChatStore();

    useEffect(() => {
        loadChats();
    }, [loadChats]);

    if (isLoading && chats.length === 0) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
            </div>
        );
    }

    if (chats.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center h-full text-gray-500 p-4">
                <p className="text-center">Нет чатов</p>
                <p className="text-sm text-center mt-1">Начните общение с контактом</p>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-full overflow-y-auto">
            {chats.map((chat) => (
                <ChatListItem
                    key={chat.id}
                    chat={chat}
                    isActive={currentChat?.id === chat.id}
                    onClick={() => selectChat(chat.id)}
                />
            ))}
        </div>
    );
}
