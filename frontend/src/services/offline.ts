/**
 * Сервис для оффлайн режима и синхронизации
 */

import type { NetworkStatus, QueuedMessage, SyncState, OfflineData } from '../types/offline';
import { MAX_RETRY_COUNT, SYNC_INTERVAL } from '../types/offline';

const STORAGE_KEY = 'offline_data';

class OfflineService {
    private status: NetworkStatus = 'online';
    private queue: QueuedMessage[] = [];
    private lastSync: number | null = null;
    private listeners: Set<(state: SyncState) => void> = new Set();
    private syncInterval: number | null = null;

    constructor() {
        this.loadFromStorage();
        this.setupNetworkListeners();
        this.startSyncInterval();
    }

    private loadFromStorage(): void {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                const data: OfflineData = JSON.parse(stored);
                this.queue = data.messages || [];
                this.lastSync = data.lastSync;
            } catch {
                this.queue = [];
                this.lastSync = null;
            }
        }
    }

    private saveToStorage(): void {
        const data: OfflineData = {
            messages: this.queue,
            lastSync: this.lastSync,
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }

    private setupNetworkListeners(): void {
        window.addEventListener('online', () => {
            this.status = 'online';
            this.notifyListeners();
            this.syncPendingMessages();
        });

        window.addEventListener('offline', () => {
            this.status = 'offline';
            this.notifyListeners();
        });

        this.status = navigator.onLine ? 'online' : 'offline';
    }

    private startSyncInterval(): void {
        this.syncInterval = window.setInterval(() => {
            if (this.status === 'online' && this.queue.length > 0) {
                this.syncPendingMessages();
            }
        }, SYNC_INTERVAL);
    }

    getState(): SyncState {
        return {
            status: this.status,
            lastSyncAt: this.lastSync,
            pendingCount: this.queue.filter((m) => m.status !== 'failed').length,
            isSyncing: this.status === 'syncing',
        };
    }

    isOnline(): boolean {
        return this.status === 'online';
    }

    isOffline(): boolean {
        return this.status === 'offline';
    }

    queueMessage(chatId: string, content: string): string {
        const id = `offline_${Date.now()}_${Math.random().toString(36).slice(2)}`;
        const message: QueuedMessage = {
            id,
            chatId,
            content,
            timestamp: Date.now(),
            retryCount: 0,
            status: 'pending',
        };

        this.queue.push(message);
        this.saveToStorage();
        this.notifyListeners();

        if (this.status === 'online') {
            this.syncPendingMessages();
        }

        return id;
    }

    async syncPendingMessages(): Promise<void> {
        if (this.status === 'offline' || this.queue.length === 0) {
            return;
        }

        this.status = 'syncing';
        this.notifyListeners();

        const pendingMessages = this.queue.filter((m) => m.status === 'pending');

        for (const message of pendingMessages) {
            try {
                message.status = 'sending';
                this.notifyListeners();

                await this.sendMessage(message);

                this.queue = this.queue.filter((m) => m.id !== message.id);
            } catch (err) {
                message.retryCount++;
                if (message.retryCount >= MAX_RETRY_COUNT) {
                    message.status = 'failed';
                } else {
                    message.status = 'pending';
                }
            }
        }

        this.lastSync = Date.now();
        this.status = 'online';
        this.saveToStorage();
        this.notifyListeners();
    }

    private async sendMessage(message: QueuedMessage): Promise<void> {
        const token = localStorage.getItem('access_token');
        const response = await fetch(
            `${import.meta.env.VITE_API_URL || ''}/api/chats/${message.chatId}/messages`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ content: message.content }),
            }
        );

        if (!response.ok) {
            throw new Error('Ошибка отправки сообщения');
        }
    }

    retryMessage(messageId: string): void {
        const message = this.queue.find((m) => m.id === messageId);
        if (message && message.status === 'failed') {
            message.status = 'pending';
            message.retryCount = 0;
            this.saveToStorage();
            this.notifyListeners();
            this.syncPendingMessages();
        }
    }

    removeFailedMessage(messageId: string): void {
        this.queue = this.queue.filter((m) => m.id !== messageId);
        this.saveToStorage();
        this.notifyListeners();
    }

    getPendingMessages(): QueuedMessage[] {
        return [...this.queue];
    }

    getFailedMessages(): QueuedMessage[] {
        return this.queue.filter((m) => m.status === 'failed');
    }

    subscribe(listener: (state: SyncState) => void): () => void {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }

    private notifyListeners(): void {
        const state = this.getState();
        this.listeners.forEach((listener) => listener(state));
    }

    destroy(): void {
        if (this.syncInterval) {
            clearInterval(this.syncInterval);
        }
    }
}

export const offlineService = new OfflineService();
