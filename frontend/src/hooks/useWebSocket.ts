/**
 * Хук для работы с WebSocket
 */

import { useEffect, useCallback } from 'react';
import { wsService } from '../services/websocket';
import { useAuthStore } from '../store/authStore';
import { useChatStore } from '../store/chatStore';
import type { Message } from '../types/chat';

export function useWebSocket() {
    const { isAuthenticated } = useAuthStore();
    const { addMessage, updateMessageStatus, currentChat } = useChatStore();

    const handleNewMessage = useCallback(
        (data: unknown) => {
            const message = data as Message;
            addMessage(message);
        },
        [addMessage]
    );

    const handleMessageDelivered = useCallback(
        (data: unknown) => {
            const { message_id } = data as { message_id: string };
            updateMessageStatus(message_id, 'delivered');
        },
        [updateMessageStatus]
    );

    const handleMessageRead = useCallback(
        (data: unknown) => {
            const { message_id } = data as { message_id: string };
            updateMessageStatus(message_id, 'read');
        },
        [updateMessageStatus]
    );

    useEffect(() => {
        if (!isAuthenticated) return;

        const token = localStorage.getItem('access_token');
        if (token) {
            wsService.connect(token);
        }

        wsService.on('new_message', handleNewMessage);
        wsService.on('message_delivered', handleMessageDelivered);
        wsService.on('message_read', handleMessageRead);

        return () => {
            wsService.off('new_message', handleNewMessage);
            wsService.off('message_delivered', handleMessageDelivered);
            wsService.off('message_read', handleMessageRead);
            wsService.disconnect();
        };
    }, [isAuthenticated, handleNewMessage, handleMessageDelivered, handleMessageRead]);

    useEffect(() => {
        if (currentChat) {
            wsService.joinChat(currentChat.id);
            return () => {
                wsService.leaveChat(currentChat.id);
            };
        }
    }, [currentChat]);

    return {
        isConnected: wsService.isConnected,
        sendMessage: wsService.sendMessage.bind(wsService),
        startTyping: wsService.startTyping.bind(wsService),
        stopTyping: wsService.stopTyping.bind(wsService),
        markRead: wsService.markRead.bind(wsService),
    };
}
