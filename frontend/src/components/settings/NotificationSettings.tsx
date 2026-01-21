/**
 * Компонент настроек уведомлений
 */

import { useState } from 'react';
import { notificationService } from '../../services/notifications';
import type { NotificationSettings as NotificationSettingsType } from '../../types/notifications';

interface NotificationSettingsProps {
    onClose?: () => void;
}

export function NotificationSettings({ onClose }: NotificationSettingsProps) {
    const [settings, setSettings] = useState<NotificationSettingsType>(notificationService.getSettings());
    const [permission, setPermission] = useState(notificationService.getPermission());

    const handleToggle = (key: keyof NotificationSettingsType) => {
        const current = settings[key];
        if (typeof current === 'boolean') {
            const newSettings = { ...settings, [key]: !current };
            setSettings(newSettings);
            notificationService.updateSettings({ [key]: !current });
        }
    };

    const handleTimeChange = (key: 'quietHoursStart' | 'quietHoursEnd', value: string) => {
        const newSettings = { ...settings, [key]: value };
        setSettings(newSettings);
        notificationService.updateSettings({ [key]: value });
    };

    const handleRequestPermission = async () => {
        const result = await notificationService.requestPermission();
        setPermission(result);
    };

    const handleTestNotification = () => {
        notificationService.show({
            title: 'Тестовое уведомление',
            body: 'Это проверка работы уведомлений',
        });
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Уведомления
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
                {permission !== 'granted' && (
                    <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl">
                        <div className="flex items-start gap-3">
                            <svg className="w-5 h-5 text-yellow-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            <div className="flex-1">
                                <p className="text-sm text-yellow-800 dark:text-yellow-200">
                                    {permission === 'denied'
                                        ? 'Уведомления заблокированы в настройках браузера'
                                        : 'Разрешите уведомления для получения сообщений'}
                                </p>
                                {permission === 'default' && (
                                    <button
                                        onClick={handleRequestPermission}
                                        className="mt-2 text-sm font-medium text-yellow-600 dark:text-yellow-400 hover:underline"
                                    >
                                        Разрешить уведомления
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Основные
                    </h3>
                    <div className="space-y-3">
                        <ToggleOption
                            label="Уведомления"
                            description="Включить push-уведомления"
                            checked={settings.enabled}
                            onChange={() => handleToggle('enabled')}
                        />
                        <ToggleOption
                            label="Звук"
                            description="Воспроизводить звук при уведомлении"
                            checked={settings.sound}
                            onChange={() => handleToggle('sound')}
                            disabled={!settings.enabled}
                        />
                        <ToggleOption
                            label="Вибрация"
                            description="Вибрировать при уведомлении"
                            checked={settings.vibration}
                            onChange={() => handleToggle('vibration')}
                            disabled={!settings.enabled}
                        />
                        <ToggleOption
                            label="Показывать превью"
                            description="Отображать текст сообщения в уведомлении"
                            checked={settings.showPreview}
                            onChange={() => handleToggle('showPreview')}
                            disabled={!settings.enabled}
                        />
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Тихий режим
                    </h3>
                    <ToggleOption
                        label="Тихие часы"
                        description="Отключить уведомления в указанное время"
                        checked={settings.quietHoursEnabled}
                        onChange={() => handleToggle('quietHoursEnabled')}
                    />

                    {settings.quietHoursEnabled && (
                        <div className="mt-3 flex items-center gap-4 pl-4">
                            <div>
                                <label className="text-xs text-gray-500 dark:text-gray-400">С</label>
                                <input
                                    type="time"
                                    value={settings.quietHoursStart}
                                    onChange={(e) => handleTimeChange('quietHoursStart', e.target.value)}
                                    className="block mt-1 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                                />
                            </div>
                            <div>
                                <label className="text-xs text-gray-500 dark:text-gray-400">До</label>
                                <input
                                    type="time"
                                    value={settings.quietHoursEnd}
                                    onChange={(e) => handleTimeChange('quietHoursEnd', e.target.value)}
                                    className="block mt-1 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
                                />
                            </div>
                        </div>
                    )}
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Группировка
                    </h3>
                    <ToggleOption
                        label="Группировать уведомления"
                        description="Объединять несколько уведомлений из одного чата"
                        checked={settings.groupNotifications}
                        onChange={() => handleToggle('groupNotifications')}
                    />
                </section>

                {permission === 'granted' && (
                    <button
                        onClick={handleTestNotification}
                        className="w-full py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
                    >
                        Тестовое уведомление
                    </button>
                )}
            </div>
        </div>
    );
}

interface ToggleOptionProps {
    label: string;
    description: string;
    checked: boolean;
    onChange: () => void;
    disabled?: boolean;
}

function ToggleOption({ label, description, checked, onChange, disabled }: ToggleOptionProps) {
    return (
        <label className={`flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg ${disabled ? 'opacity-50' : 'cursor-pointer'}`}>
            <div>
                <span className="text-gray-900 dark:text-white font-medium">{label}</span>
                <p className="text-xs text-gray-500 dark:text-gray-400">{description}</p>
            </div>
            <button
                role="switch"
                aria-checked={checked}
                onClick={disabled ? undefined : onChange}
                disabled={disabled}
                className={`relative w-12 h-6 rounded-full transition-colors ${checked ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                    } ${disabled ? 'cursor-not-allowed' : ''}`}
            >
                <span
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${checked ? 'left-7' : 'left-1'
                        }`}
                />
            </button>
        </label>
    );
}
