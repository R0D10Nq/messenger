/**
 * Типы для аналитики
 */

export type AnalyticsPeriod = 'day' | 'week' | 'month' | 'year';
export type MetricType = 'messages' | 'users' | 'chats' | 'media' | 'calls';

export interface DataPoint {
    timestamp: string;
    value: number;
}

export interface MetricSummary {
    current: number;
    previous: number;
    change_percent: number;
    trend: 'up' | 'down' | 'stable';
}

export interface OverviewResponse {
    messages: MetricSummary;
    active_users: MetricSummary;
    new_chats: MetricSummary;
    media_shared: MetricSummary;
}

export interface UserActivityResponse {
    total_messages: number;
    total_chats: number;
    total_media: number;
    total_calls: number;
    messages_by_day: DataPoint[];
    active_hours: Record<number, number>;
    most_active_chat_id: string | null;
}

export interface ChatAnalyticsResponse {
    message_count: number;
    member_count: number;
    media_count: number;
    messages_by_day: DataPoint[];
    top_senders: Array<{ user_id: string; username: string; count: number }>;
    peak_hours: number[];
    avg_messages_per_day: number;
}

export const PERIOD_LABELS: Record<AnalyticsPeriod, string> = {
    day: 'День',
    week: 'Неделя',
    month: 'Месяц',
    year: 'Год',
};
