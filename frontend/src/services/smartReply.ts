/**
 * Сервис для smart replies
 */

import { api } from './api';
import type { SmartReplyResponse, SmartReplySettings } from '../types/smartReply';

export const smartReplyService = {
    async generateReplies(messageId: string, contextMessages = 5): Promise<SmartReplyResponse> {
        return api.post<SmartReplyResponse>('/smart-reply/generate', {
            message_id: messageId,
            context_messages: contextMessages,
        });
    },

    async getQuickReplies(text: string): Promise<SmartReplyResponse> {
        return api.post<SmartReplyResponse>(`/smart-reply/quick?text=${encodeURIComponent(text)}`, {});
    },

    async getSettings(): Promise<SmartReplySettings> {
        return api.get<SmartReplySettings>('/smart-reply/settings');
    },

    async updateSettings(settings: SmartReplySettings): Promise<SmartReplySettings> {
        return api.put<SmartReplySettings>('/smart-reply/settings', settings);
    },
};
