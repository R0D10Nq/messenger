/**
 * Сервис для работы с ботами
 */

import { api } from './api';
import type {
    BotCommand,
    BotMessageRequest,
    BotResponse,
    CreateBotRequest,
} from '../types/bot';

export const botService = {
    async createBot(request: CreateBotRequest): Promise<BotResponse> {
        return api.post<BotResponse>('/bots', request);
    },

    async listMyBots(): Promise<BotResponse[]> {
        return api.get<BotResponse[]>('/bots');
    },

    async getBot(botId: string): Promise<BotResponse> {
        return api.get<BotResponse>(`/bots/${botId}`);
    },

    async updateBot(botId: string, updates: Partial<CreateBotRequest>): Promise<BotResponse> {
        return api.put<BotResponse>(`/bots/${botId}`, updates);
    },

    async deleteBot(botId: string): Promise<void> {
        return api.delete(`/bots/${botId}`);
    },

    async regenerateToken(botId: string): Promise<{ api_token: string }> {
        return api.post(`/bots/${botId}/token`, {});
    },

    async setCommands(botId: string, commands: BotCommand[]): Promise<BotCommand[]> {
        return api.post<BotCommand[]>(`/bots/${botId}/commands`, { commands });
    },

    async getCommands(botId: string): Promise<BotCommand[]> {
        return api.get<BotCommand[]>(`/bots/${botId}/commands`);
    },

    async sendMessage(botId: string, request: BotMessageRequest): Promise<{ message_id: string }> {
        return api.post(`/bots/${botId}/message`, request);
    },

    async setWebhook(botId: string, url: string): Promise<{ success: boolean }> {
        return api.post(`/bots/${botId}/webhook`, { url });
    },

    async deleteWebhook(botId: string): Promise<{ success: boolean }> {
        return api.delete(`/bots/${botId}/webhook`);
    },
};
