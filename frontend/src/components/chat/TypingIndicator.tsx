/**
 * Индикатор набора текста
 */

import { useEffect, useState, useCallback } from 'react';
import { wsService } from '../../services/websocket';

interface TypingUser {
    userId: string;
    name: string;
}

interface TypingIndicatorProps {
    chatId: string;
}

export function TypingIndicator({ chatId }: TypingIndicatorProps) {
    const [typingUsers, setTypingUsers] = useState<TypingUser[]>([]);

    const handleTypingStart = useCallback(
        (data: unknown) => {
            const { chat_id, user_id, user_name } = data as {
                chat_id: string;
                user_id: string;
                user_name: string;
            };

            if (chat_id !== chatId) return;

            setTypingUsers((prev) => {
                if (prev.some((u) => u.userId === user_id)) return prev;
                return [...prev, { userId: user_id, name: user_name }];
            });
        },
        [chatId]
    );

    const handleTypingStop = useCallback(
        (data: unknown) => {
            const { chat_id, user_id } = data as { chat_id: string; user_id: string };

            if (chat_id !== chatId) return;

            setTypingUsers((prev) => prev.filter((u) => u.userId !== user_id));
        },
        [chatId]
    );

    useEffect(() => {
        wsService.on('typing_start', handleTypingStart);
        wsService.on('typing_stop', handleTypingStop);

        return () => {
            wsService.off('typing_start', handleTypingStart);
            wsService.off('typing_stop', handleTypingStop);
        };
    }, [handleTypingStart, handleTypingStop]);

    useEffect(() => {
        setTypingUsers([]);
    }, [chatId]);

    if (typingUsers.length === 0) return null;

    const getTypingText = () => {
        if (typingUsers.length === 1) {
            return `${typingUsers[0].name} печатает`;
        }
        if (typingUsers.length === 2) {
            return `${typingUsers[0].name} и ${typingUsers[1].name} печатают`;
        }
        return `${typingUsers[0].name} и ещё ${typingUsers.length - 1} печатают`;
    };

    return (
        <div className="px-4 py-2 text-sm text-gray-500 flex items-center gap-2">
            <span className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </span>
            <span>{getTypingText()}</span>
        </div>
    );
}
