/**
 * Типы для push-уведомлений
 */

export interface NotificationSettings {
    enabled: boolean;
    sound: boolean;
    vibration: boolean;
    showPreview: boolean;
    groupNotifications: boolean;
    quietHoursEnabled: boolean;
    quietHoursStart: string;
    quietHoursEnd: string;
    mutedChats: string[];
}

export interface PushNotification {
    id: string;
    title: string;
    body: string;
    icon?: string;
    image?: string;
    tag?: string;
    data?: {
        chatId?: string;
        messageId?: string;
        type?: NotificationType;
    };
    timestamp: number;
}

export type NotificationType = 'message' | 'call' | 'mention' | 'reaction' | 'system';

export type NotificationPermission = 'default' | 'granted' | 'denied';

export const DEFAULT_NOTIFICATION_SETTINGS: NotificationSettings = {
    enabled: true,
    sound: true,
    vibration: true,
    showPreview: true,
    groupNotifications: true,
    quietHoursEnabled: false,
    quietHoursStart: '22:00',
    quietHoursEnd: '08:00',
    mutedChats: [],
};

export const NOTIFICATION_SOUNDS = [
    { id: 'default', name: 'По умолчанию' },
    { id: 'chime', name: 'Колокольчик' },
    { id: 'ping', name: 'Пинг' },
    { id: 'pop', name: 'Поп' },
    { id: 'none', name: 'Без звука' },
];
