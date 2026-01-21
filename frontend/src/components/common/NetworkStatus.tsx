/**
 * Компонент отображения статуса сети
 */

import { useState, useEffect } from 'react';
import { offlineService } from '../../services/offline';
import type { SyncState } from '../../types/offline';

export function NetworkStatus() {
    const [state, setState] = useState<SyncState>(offlineService.getState());
    const [showBanner, setShowBanner] = useState(false);

    useEffect(() => {
        const unsubscribe = offlineService.subscribe((newState) => {
            setState(newState);
            if (newState.status === 'offline') {
                setShowBanner(true);
            }
        });

        return unsubscribe;
    }, []);

    const handleDismiss = () => {
        setShowBanner(false);
    };

    const handleRetryAll = () => {
        offlineService.syncPendingMessages();
    };

    if (state.status === 'online' && state.pendingCount === 0 && !showBanner) {
        return null;
    }

    return (
        <>
            {state.status === 'offline' && showBanner && (
                <div className="fixed top-0 left-0 right-0 bg-yellow-500 text-yellow-900 px-4 py-2 flex items-center justify-between z-50">
                    <div className="flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-2.83m-1.414 5.658a9 9 0 01-2.167-9.238m7.824 2.167a1 1 0 111.414 1.414m-1.414-1.414L3 3m8.293 8.293l1.414 1.414" />
                        </svg>
                        <span className="font-medium">Нет подключения к интернету</span>
                        {state.pendingCount > 0 && (
                            <span className="text-sm">({state.pendingCount} сообщений в очереди)</span>
                        )}
                    </div>
                    <button
                        onClick={handleDismiss}
                        className="p-1 hover:bg-yellow-600/20 rounded"
                    >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            )}

            {state.status === 'syncing' && (
                <div className="fixed top-0 left-0 right-0 bg-blue-500 text-white px-4 py-2 flex items-center justify-center gap-2 z-50">
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
                    <span>Синхронизация сообщений...</span>
                </div>
            )}

            {state.status === 'online' && state.pendingCount > 0 && (
                <div className="fixed bottom-4 right-4 bg-gray-900 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 z-50">
                    <span>{state.pendingCount} сообщений ожидают отправки</span>
                    <button
                        onClick={handleRetryAll}
                        className="px-3 py-1 bg-blue-500 hover:bg-blue-600 rounded text-sm font-medium"
                    >
                        Отправить
                    </button>
                </div>
            )}
        </>
    );
}

export function OfflineIndicator() {
    const [isOffline, setIsOffline] = useState(!navigator.onLine);

    useEffect(() => {
        const handleOnline = () => setIsOffline(false);
        const handleOffline = () => setIsOffline(true);

        window.addEventListener('online', handleOnline);
        window.addEventListener('offline', handleOffline);

        return () => {
            window.removeEventListener('online', handleOnline);
            window.removeEventListener('offline', handleOffline);
        };
    }, []);

    if (!isOffline) return null;

    return (
        <div className="inline-flex items-center gap-1 text-yellow-600 dark:text-yellow-500">
            <div className="w-2 h-2 bg-yellow-500 rounded-full" />
            <span className="text-xs">Оффлайн</span>
        </div>
    );
}
