/**
 * Типы для оффлайн режима
 */

export type NetworkStatus = 'online' | 'offline' | 'syncing';

export interface QueuedMessage {
    id: string;
    chatId: string;
    content: string;
    timestamp: number;
    retryCount: number;
    status: 'pending' | 'sending' | 'failed';
}

export interface SyncState {
    status: NetworkStatus;
    lastSyncAt: number | null;
    pendingCount: number;
    isSyncing: boolean;
}

export interface OfflineData {
    messages: QueuedMessage[];
    lastSync: number | null;
}

export const MAX_RETRY_COUNT = 3;
export const SYNC_INTERVAL = 30000;
