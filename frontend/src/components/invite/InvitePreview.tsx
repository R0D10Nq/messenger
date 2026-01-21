/**
 * Компонент превью приглашения
 */

import { useState, useEffect } from 'react';
import { inviteService } from '../../services/invite';
import type { InvitePreviewResponse } from '../../types/invite';

interface InvitePreviewProps {
    code: string;
    onJoin?: (chatId: string) => void;
    onClose?: () => void;
}

export function InvitePreview({ code, onJoin, onClose }: InvitePreviewProps) {
    const [preview, setPreview] = useState<InvitePreviewResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [joining, setJoining] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadPreview();
    }, [code]);

    const loadPreview = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await inviteService.getPreview(code);
            setPreview(data);
        } catch (err) {
            setError('Приглашение не найдено или недействительно');
        } finally {
            setLoading(false);
        }
    };

    const handleJoin = async () => {
        try {
            setJoining(true);
            const result = await inviteService.joinByInvite(code);
            if (result.success && onJoin) {
                onJoin(result.chat_id);
            }
        } catch (err) {
            setError('Не удалось присоединиться');
        } finally {
            setJoining(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-2 border-blue-500 border-t-transparent" />
            </div>
        );
    }

    if (error || !preview) {
        return (
            <div className="p-6 text-center">
                <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    Ошибка
                </h3>
                <p className="text-gray-500 dark:text-gray-400 mb-4">{error}</p>
                {onClose && (
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg text-gray-700 dark:text-gray-300"
                    >
                        Закрыть
                    </button>
                )}
            </div>
        );
    }

    if (preview.is_expired) {
        return (
            <div className="p-6 text-center">
                <div className="w-16 h-16 bg-yellow-100 dark:bg-yellow-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    Приглашение истекло
                </h3>
                <p className="text-gray-500 dark:text-gray-400">
                    Это приглашение больше не действительно
                </p>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="flex flex-col items-center text-center">
                <div className="w-20 h-20 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mb-4">
                    {preview.avatar_url ? (
                        <img
                            src={preview.avatar_url}
                            alt={preview.chat_name}
                            className="w-full h-full rounded-full object-cover"
                        />
                    ) : (
                        <span className="text-3xl font-bold text-blue-500">
                            {preview.chat_name[0]?.toUpperCase()}
                        </span>
                    )}
                </div>

                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                    {preview.chat_name}
                </h2>

                <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-2">
                    <span className="capitalize">
                        {preview.chat_type === 'group' ? 'Группа' : preview.chat_type === 'channel' ? 'Канал' : 'Чат'}
                    </span>
                    <span>·</span>
                    <span>{preview.member_count} участников</span>
                </div>

                {preview.description && (
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                        {preview.description}
                    </p>
                )}

                {preview.preview_messages && preview.preview_messages.length > 0 && (
                    <div className="w-full bg-gray-50 dark:bg-gray-800 rounded-lg p-3 mb-4 text-left">
                        <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Последние сообщения:</p>
                        {preview.preview_messages.map((msg, idx) => (
                            <div key={idx} className="text-sm text-gray-700 dark:text-gray-300 mb-1">
                                <span className="font-medium">{msg.sender}:</span> {msg.content}
                            </div>
                        ))}
                    </div>
                )}

                <button
                    onClick={handleJoin}
                    disabled={joining}
                    className="w-full py-3 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium rounded-lg transition-colors"
                >
                    {joining ? 'Присоединение...' : 'Присоединиться'}
                </button>

                {preview.requires_approval && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                        Требуется одобрение администратора
                    </p>
                )}
            </div>
        </div>
    );
}
