/**
 * Компонент быстрых ответов
 */

import { useState, useEffect } from 'react';
import { smartReplyService } from '../../services/smartReply';

interface SmartRepliesProps {
    messageText: string;
    messageId?: string;
    onSelect: (reply: string) => void;
    onHide?: () => void;
}

export function SmartReplies({ messageText, messageId, onSelect, onHide }: SmartRepliesProps) {
    const [replies, setReplies] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);
    const [visible, setVisible] = useState(true);

    useEffect(() => {
        if (messageText) {
            loadReplies();
        }
    }, [messageText, messageId]);

    const loadReplies = async () => {
        try {
            setLoading(true);
            let response;

            if (messageId) {
                response = await smartReplyService.generateReplies(messageId);
            } else {
                response = await smartReplyService.getQuickReplies(messageText);
            }

            setReplies(response.replies);
        } catch (err) {
            console.error('Ошибка загрузки ответов:', err);
            setReplies([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSelect = (reply: string) => {
        onSelect(reply);
        setVisible(false);
    };

    const handleHide = () => {
        setVisible(false);
        onHide?.();
    };

    if (!visible || replies.length === 0) {
        return null;
    }

    return (
        <div className="flex items-center gap-2 py-2 px-3 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700">
            <span className="text-xs text-gray-500 dark:text-gray-400 flex-shrink-0">
                Быстрые ответы:
            </span>

            <div className="flex flex-wrap gap-2 flex-1">
                {loading ? (
                    <div className="animate-pulse flex gap-2">
                        <div className="h-7 w-16 bg-gray-200 dark:bg-gray-700 rounded-full" />
                        <div className="h-7 w-20 bg-gray-200 dark:bg-gray-700 rounded-full" />
                        <div className="h-7 w-14 bg-gray-200 dark:bg-gray-700 rounded-full" />
                    </div>
                ) : (
                    replies.map((reply, index) => (
                        <button
                            key={index}
                            onClick={() => handleSelect(reply)}
                            className="px-3 py-1 text-sm bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-full text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/30 hover:border-blue-300 dark:hover:border-blue-600 transition-colors"
                        >
                            {reply}
                        </button>
                    ))
                )}
            </div>

            <button
                onClick={handleHide}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 flex-shrink-0"
                aria-label="Скрыть подсказки"
            >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    );
}
