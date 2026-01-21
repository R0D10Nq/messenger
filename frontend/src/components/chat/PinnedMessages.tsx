/**
 * Компонент закреплённых сообщений
 */

import { useState, useEffect, useCallback } from 'react';
import { pinService } from '../../services/pin';
import type { PinnedMessage } from '../../types/pin';

interface PinnedMessagesProps {
    chatId: string;
    onMessageClick?: (messageId: string) => void;
}

export function PinnedMessages({ chatId, onMessageClick }: PinnedMessagesProps) {
    const [pinnedMessages, setPinnedMessages] = useState<PinnedMessage[]>([]);
    const [isExpanded, setIsExpanded] = useState(false);

    const loadPinnedMessages = useCallback(async () => {
        try {
            const response = await pinService.getPinnedMessages(chatId);
            setPinnedMessages(response.pinned_messages);
        } catch (error) {
            console.error('Ошибка загрузки закреплённых сообщений:', error);
        }
    }, [chatId]);

    useEffect(() => {
        loadPinnedMessages();
    }, [loadPinnedMessages]);

    if (pinnedMessages.length === 0) {
        return null;
    }

    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'short',
        });
    };

    const currentMessage = pinnedMessages[0];

    return (
        <div className="bg-blue-50 border-b border-blue-100">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full px-4 py-2 flex items-center gap-2 hover:bg-blue-100 transition-colors"
            >
                <span className="text-blue-500 text-sm font-medium">
                    Закреплено ({pinnedMessages.length})
                </span>
                <span className="flex-1 text-left text-sm text-gray-700 truncate">
                    {currentMessage.message_content}
                </span>
                <span className="text-gray-400 text-xs">
                    {isExpanded ? '▲' : '▼'}
                </span>
            </button>

            {isExpanded && (
                <div className="border-t border-blue-100">
                    {pinnedMessages.map((pinned) => (
                        <button
                            key={pinned.id}
                            onClick={() => onMessageClick?.(pinned.message_id)}
                            className="w-full px-4 py-3 text-left hover:bg-blue-100 border-b border-blue-50 last:border-b-0"
                        >
                            <div className="flex justify-between items-start mb-1">
                                <span className="text-xs text-gray-500">
                                    Закрепил(а) {pinned.pinned_by_name}
                                </span>
                                <span className="text-xs text-gray-400">
                                    {formatDate(pinned.pinned_at)}
                                </span>
                            </div>
                            <p className="text-sm text-gray-800 line-clamp-2">
                                {pinned.message_content}
                            </p>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
