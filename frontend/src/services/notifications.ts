/**
 * Сервис для push-уведомлений
 */

import type { NotificationSettings, PushNotification, NotificationPermission } from '../types/notifications';
import { DEFAULT_NOTIFICATION_SETTINGS } from '../types/notifications';

const STORAGE_KEY = 'notification_settings';

class NotificationService {
    private settings: NotificationSettings = DEFAULT_NOTIFICATION_SETTINGS;
    private permission: NotificationPermission = 'default';
    private listeners: Set<(notification: PushNotification) => void> = new Set();

    constructor() {
        this.loadSettings();
        this.checkPermission();
    }

    private loadSettings(): void {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                this.settings = { ...DEFAULT_NOTIFICATION_SETTINGS, ...JSON.parse(stored) };
            } catch {
                this.settings = DEFAULT_NOTIFICATION_SETTINGS;
            }
        }
    }

    private saveSettings(): void {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.settings));
    }

    private checkPermission(): void {
        if ('Notification' in window) {
            this.permission = Notification.permission as NotificationPermission;
        }
    }

    async requestPermission(): Promise<NotificationPermission> {
        if (!('Notification' in window)) {
            return 'denied';
        }

        const result = await Notification.requestPermission();
        this.permission = result as NotificationPermission;
        return this.permission;
    }

    getPermission(): NotificationPermission {
        return this.permission;
    }

    isEnabled(): boolean {
        return this.settings.enabled && this.permission === 'granted';
    }

    getSettings(): NotificationSettings {
        return { ...this.settings };
    }

    updateSettings(updates: Partial<NotificationSettings>): void {
        this.settings = { ...this.settings, ...updates };
        this.saveSettings();
    }

    isInQuietHours(): boolean {
        if (!this.settings.quietHoursEnabled) return false;

        const now = new Date();
        const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;

        const start = this.settings.quietHoursStart;
        const end = this.settings.quietHoursEnd;

        if (start <= end) {
            return currentTime >= start && currentTime <= end;
        } else {
            return currentTime >= start || currentTime <= end;
        }
    }

    isChatMuted(chatId: string): boolean {
        return this.settings.mutedChats.includes(chatId);
    }

    muteChat(chatId: string): void {
        if (!this.settings.mutedChats.includes(chatId)) {
            this.settings.mutedChats.push(chatId);
            this.saveSettings();
        }
    }

    unmuteChat(chatId: string): void {
        this.settings.mutedChats = this.settings.mutedChats.filter((id) => id !== chatId);
        this.saveSettings();
    }

    async show(notification: Omit<PushNotification, 'id' | 'timestamp'>): Promise<void> {
        if (!this.isEnabled()) return;
        if (this.isInQuietHours()) return;
        if (notification.data?.chatId && this.isChatMuted(notification.data.chatId)) return;

        const fullNotification: PushNotification = {
            ...notification,
            id: `notif_${Date.now()}`,
            timestamp: Date.now(),
        };

        if ('Notification' in window && this.permission === 'granted') {
            const nativeNotification = new Notification(notification.title, {
                body: this.settings.showPreview ? notification.body : 'Новое сообщение',
                icon: notification.icon || '/icon.png',
                tag: notification.tag,
                silent: !this.settings.sound,
            });

            nativeNotification.onclick = () => {
                window.focus();
                if (notification.data?.chatId) {
                    window.location.href = `/chat/${notification.data.chatId}`;
                }
                nativeNotification.close();
            };
        }

        if (this.settings.sound) {
            this.playSound();
        }

        if (this.settings.vibration && 'vibrate' in navigator) {
            navigator.vibrate(200);
        }

        this.notifyListeners(fullNotification);
    }

    private playSound(): void {
        const audio = new Audio('/sounds/notification.mp3');
        audio.volume = 0.5;
        audio.play().catch(() => { });
    }

    subscribe(listener: (notification: PushNotification) => void): () => void {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }

    private notifyListeners(notification: PushNotification): void {
        this.listeners.forEach((listener) => listener(notification));
    }
}

export const notificationService = new NotificationService();
