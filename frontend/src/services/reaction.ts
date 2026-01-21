/**
 * Сервис для реакций на сообщения
 */

import { api } from './api';
import type { MessageReactions, ReactionCreate } from '../types/reaction';

export const reactionService = {
    async addReaction(messageId: string, data: ReactionCreate): Promise<void> {
        await api.post(`/reactions/messages/${messageId}`, data);
    },

    async removeReaction(messageId: string, emoji: string): Promise<void> {
        await api.delete(`/reactions/messages/${messageId}/${encodeURIComponent(emoji)}`);
    },

    async getReactions(messageId: string): Promise<MessageReactions> {
        return api.get<MessageReactions>(`/reactions/messages/${messageId}`);
    },
};
