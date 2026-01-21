/**
 * Сервис для закреплённых сообщений
 */

import { api } from './api';
import type { PinnedMessage, PinnedMessagesList } from '../types/pin';

export const pinService = {
    async pinMessage(chatId: string, messageId: string): Promise<PinnedMessage> {
        return api.post<PinnedMessage>(`/chats/${chatId}/pin/${messageId}`);
    },

    async unpinMessage(chatId: string, messageId: string): Promise<void> {
        await api.delete(`/chats/${chatId}/pin/${messageId}`);
    },

    async getPinnedMessages(chatId: string): Promise<PinnedMessagesList> {
        return api.get<PinnedMessagesList>(`/chats/${chatId}/pinned`);
    },
};
