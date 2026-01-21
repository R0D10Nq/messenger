/**
 * Сервис для работы с аналитикой
 */

import { api } from './api';
import type {
    AnalyticsPeriod,
    ChatAnalyticsResponse,
    OverviewResponse,
    UserActivityResponse,
} from '../types/analytics';

export const analyticsService = {
    async getOverview(period: AnalyticsPeriod = 'week'): Promise<OverviewResponse> {
        return api.get<OverviewResponse>(`/analytics/overview?period=${period}`);
    },

    async getUserActivity(period: AnalyticsPeriod = 'week'): Promise<UserActivityResponse> {
        return api.get<UserActivityResponse>(`/analytics/user?period=${period}`);
    },

    async getChatAnalytics(chatId: string, period: AnalyticsPeriod = 'week'): Promise<ChatAnalyticsResponse> {
        return api.get<ChatAnalyticsResponse>(`/analytics/chat/${chatId}?period=${period}`);
    },

    async exportAnalytics(period: AnalyticsPeriod, format: 'csv' | 'json' = 'csv'): Promise<{ download_url: string }> {
        return api.post('/analytics/export', { period, format });
    },
};
