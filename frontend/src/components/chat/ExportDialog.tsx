/**
 * Диалог экспорта чата
 */

import { useState } from 'react';
import { exportService } from '../../services/export';
import type { ExportFormat } from '../../types/export';
import { FORMAT_LABELS } from '../../types/export';

interface ExportDialogProps {
    chatId: string;
    chatName: string;
    onClose: () => void;
}

export function ExportDialog({ chatId, chatName, onClose }: ExportDialogProps) {
    const [format, setFormat] = useState<ExportFormat>('json');
    const [includeMedia, setIncludeMedia] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);
    const [jobId, setJobId] = useState<string | null>(null);

    const handleExport = async () => {
        try {
            setLoading(true);
            setError(null);

            const job = await exportService.startExport({
                chat_id: chatId,
                format,
                include_media: includeMedia,
            });

            setJobId(job.id);
            setSuccess(true);

            setTimeout(async () => {
                try {
                    await exportService.downloadExport(job.id);
                } catch (err) {
                    console.error('Ошибка скачивания:', err);
                }
            }, 1000);
        } catch (err) {
            setError('Ошибка экспорта чата');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-md mx-4">
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Экспорт чата
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div className="p-4 space-y-4">
                    {success ? (
                        <div className="text-center py-4">
                            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-3">
                                <svg className="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            </div>
                            <p className="text-gray-900 dark:text-white font-medium">
                                Экспорт готов!
                            </p>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                Файл начнёт скачиваться автоматически
                            </p>
                            <button
                                onClick={() => jobId && exportService.downloadExport(jobId)}
                                className="mt-4 text-blue-500 hover:text-blue-600 text-sm font-medium"
                            >
                                Скачать ещё раз
                            </button>
                        </div>
                    ) : (
                        <>
                            <div className="text-sm text-gray-500 dark:text-gray-400">
                                Экспортировать чат «{chatName}»
                            </div>

                            {error && (
                                <div className="p-3 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-lg text-sm">
                                    {error}
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Формат
                                </label>
                                <div className="space-y-2">
                                    {(Object.keys(FORMAT_LABELS) as ExportFormat[]).map((f) => (
                                        <label
                                            key={f}
                                            className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-600 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700"
                                        >
                                            <input
                                                type="radio"
                                                name="format"
                                                value={f}
                                                checked={format === f}
                                                onChange={() => setFormat(f)}
                                                className="w-4 h-4 text-blue-500"
                                            />
                                            <div>
                                                <div className="font-medium text-gray-900 dark:text-white">
                                                    {FORMAT_LABELS[f]}
                                                </div>
                                                <div className="text-xs text-gray-500 dark:text-gray-400">
                                                    {f === 'json' && 'Структурированный формат для программной обработки'}
                                                    {f === 'html' && 'Для просмотра в браузере'}
                                                    {f === 'txt' && 'Простой текстовый формат'}
                                                </div>
                                            </div>
                                        </label>
                                    ))}
                                </div>
                            </div>

                            <label className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-600 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
                                <input
                                    type="checkbox"
                                    checked={includeMedia}
                                    onChange={(e) => setIncludeMedia(e.target.checked)}
                                    className="w-4 h-4 text-blue-500 rounded"
                                />
                                <div>
                                    <div className="font-medium text-gray-900 dark:text-white">
                                        Включить медиафайлы
                                    </div>
                                    <div className="text-xs text-gray-500 dark:text-gray-400">
                                        Изображения, видео, документы
                                    </div>
                                </div>
                            </label>
                        </>
                    )}
                </div>

                <div className="flex gap-3 p-4 border-t border-gray-200 dark:border-gray-700">
                    {success ? (
                        <button
                            onClick={onClose}
                            className="flex-1 py-2 px-4 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                        >
                            Закрыть
                        </button>
                    ) : (
                        <>
                            <button
                                onClick={onClose}
                                className="flex-1 py-2 px-4 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                            >
                                Отмена
                            </button>
                            <button
                                onClick={handleExport}
                                disabled={loading}
                                className="flex-1 py-2 px-4 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white font-medium rounded-lg transition-colors"
                            >
                                {loading ? 'Экспорт...' : 'Экспортировать'}
                            </button>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}
