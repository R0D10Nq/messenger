/**
 * Компонент настроек экономии данных
 */

import { useState } from 'react';
import { dataSaverService } from '../../services/dataSaver';
import type { DataSaverSettings as DataSaverSettingsType, ImageQuality, VideoQuality } from '../../types/dataSaver';
import { IMAGE_QUALITY_LABELS, VIDEO_QUALITY_LABELS } from '../../types/dataSaver';

interface DataSaverSettingsProps {
    onClose?: () => void;
}

export function DataSaverSettings({ onClose }: DataSaverSettingsProps) {
    const [settings, setSettings] = useState<DataSaverSettingsType>(dataSaverService.getSettings());
    const [saved, setSaved] = useState(false);

    const handleChange = <K extends keyof DataSaverSettingsType>(
        key: K,
        value: DataSaverSettingsType[K]
    ) => {
        const newSettings = { ...settings, [key]: value };
        setSettings(newSettings);
        dataSaverService.saveSettings(newSettings);
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    };

    const handleEnableDataSaver = () => {
        dataSaverService.enableDataSaver();
        setSettings(dataSaverService.getSettings());
    };

    const handleDisableDataSaver = () => {
        dataSaverService.disableDataSaver();
        setSettings(dataSaverService.getSettings());
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Экономия данных
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
            )}

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {saved && (
                    <div className="p-2 bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 text-sm rounded-lg text-center">
                        Настройки сохранены
                    </div>
                )}

                <div className="flex items-center justify-between p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
                    <div>
                        <h3 className="font-medium text-gray-900 dark:text-white">
                            Режим экономии данных
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                            Уменьшает потребление трафика
                        </p>
                    </div>
                    <button
                        onClick={settings.enabled ? handleDisableDataSaver : handleEnableDataSaver}
                        className={`relative w-12 h-6 rounded-full transition-colors ${settings.enabled ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                            }`}
                    >
                        <span
                            className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${settings.enabled ? 'left-7' : 'left-1'
                                }`}
                        />
                    </button>
                </div>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Автозагрузка медиа
                    </h3>
                    <div className="space-y-3">
                        {[
                            { key: 'autoDownloadImages' as const, label: 'Изображения' },
                            { key: 'autoDownloadVideos' as const, label: 'Видео' },
                            { key: 'autoDownloadAudio' as const, label: 'Аудио' },
                            { key: 'autoDownloadDocuments' as const, label: 'Документы' },
                        ].map(({ key, label }) => (
                            <label
                                key={key}
                                className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg cursor-pointer"
                            >
                                <span className="text-gray-900 dark:text-white">{label}</span>
                                <input
                                    type="checkbox"
                                    checked={settings[key]}
                                    onChange={(e) => handleChange(key, e.target.checked)}
                                    className="w-5 h-5 text-blue-500 rounded"
                                />
                            </label>
                        ))}
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Качество медиа
                    </h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm text-gray-700 dark:text-gray-300 mb-2">
                                Качество изображений
                            </label>
                            <select
                                value={settings.imageQuality}
                                onChange={(e) => handleChange('imageQuality', e.target.value as ImageQuality)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                {Object.entries(IMAGE_QUALITY_LABELS).map(([value, label]) => (
                                    <option key={value} value={value}>{label}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm text-gray-700 dark:text-gray-300 mb-2">
                                Качество видео
                            </label>
                            <select
                                value={settings.videoQuality}
                                onChange={(e) => handleChange('videoQuality', e.target.value as VideoQuality)}
                                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                            >
                                {Object.entries(VIDEO_QUALITY_LABELS).map(([value, label]) => (
                                    <option key={value} value={value}>{label}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Дополнительно
                    </h3>
                    <div className="space-y-3">
                        <label className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg cursor-pointer">
                            <div>
                                <span className="text-gray-900 dark:text-white">Предзагрузка медиа</span>
                                <p className="text-xs text-gray-500 dark:text-gray-400">
                                    Загружать медиа заранее для быстрого просмотра
                                </p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.preloadMedia}
                                onChange={(e) => handleChange('preloadMedia', e.target.checked)}
                                className="w-5 h-5 text-blue-500 rounded"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg cursor-pointer">
                            <div>
                                <span className="text-gray-900 dark:text-white">Уменьшить анимации</span>
                                <p className="text-xs text-gray-500 dark:text-gray-400">
                                    Отключить анимации для экономии ресурсов
                                </p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.reducedAnimations}
                                onChange={(e) => handleChange('reducedAnimations', e.target.checked)}
                                className="w-5 h-5 text-blue-500 rounded"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg cursor-pointer">
                            <div>
                                <span className="text-gray-900 dark:text-white">Сжимать загрузки</span>
                                <p className="text-xs text-gray-500 dark:text-gray-400">
                                    Сжимать изображения перед отправкой
                                </p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.compressUploads}
                                onChange={(e) => handleChange('compressUploads', e.target.checked)}
                                className="w-5 h-5 text-blue-500 rounded"
                            />
                        </label>
                    </div>
                </section>
            </div>
        </div>
    );
}
