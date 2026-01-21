/**
 * Компонент управления устройствами
 */

import { useState, useEffect } from 'react';
import { deviceService } from '../../services/device';
import type { DeviceResponse } from '../../types/device';
import { DEVICE_TYPE_ICONS, PLATFORM_NAMES } from '../../types/device';

interface DeviceManagerProps {
    onClose?: () => void;
}

export function DeviceManager({ onClose }: DeviceManagerProps) {
    const [devices, setDevices] = useState<DeviceResponse[]>([]);
    const [currentDeviceId, setCurrentDeviceId] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadDevices();
    }, []);

    const loadDevices = async () => {
        try {
            setLoading(true);
            const data = await deviceService.listDevices();
            setDevices(data.devices);
            setCurrentDeviceId(data.current_device_id);
        } catch (err) {
            console.error('Ошибка загрузки устройств:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleRemoveDevice = async (deviceId: string) => {
        if (!confirm('Завершить сессию на этом устройстве?')) return;

        try {
            await deviceService.removeDevice(deviceId);
            setDevices(devices.filter((d) => d.id !== deviceId));
        } catch (err) {
            console.error('Ошибка удаления устройства:', err);
        }
    };

    const handleTerminateAll = async () => {
        if (!confirm('Завершить все сессии кроме текущей?')) return;

        try {
            await deviceService.terminateAllOtherSessions();
            setDevices(devices.filter((d) => d.id === currentDeviceId));
        } catch (err) {
            console.error('Ошибка завершения сессий:', err);
        }
    };

    const formatLastActive = (dateStr: string): string => {
        const date = new Date(dateStr);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);

        if (diffMins < 1) return 'Сейчас';
        if (diffMins < 60) return `${diffMins} мин. назад`;
        if (diffMins < 1440) return `${Math.floor(diffMins / 60)} ч. назад`;
        return date.toLocaleDateString();
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Устройства
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

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {loading ? (
                    <div className="space-y-3">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="h-20 bg-gray-100 dark:bg-gray-700 rounded-xl animate-pulse" />
                        ))}
                    </div>
                ) : (
                    <>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                            {devices.length} устройств подключено
                        </p>

                        <div className="space-y-3">
                            {devices.map((device) => (
                                <div
                                    key={device.id}
                                    className={`p-4 rounded-xl border-2 ${device.is_current
                                            ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-500'
                                            : 'bg-gray-50 dark:bg-gray-700/50 border-transparent'
                                        }`}
                                >
                                    <div className="flex items-start gap-3">
                                        <div className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm">
                                            <svg
                                                className="w-6 h-6 text-gray-600 dark:text-gray-400"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    strokeWidth={2}
                                                    d={DEVICE_TYPE_ICONS[device.device_type]}
                                                />
                                            </svg>
                                        </div>

                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-2">
                                                <h3 className="font-medium text-gray-900 dark:text-white truncate">
                                                    {device.device_name}
                                                </h3>
                                                {device.is_current && (
                                                    <span className="px-2 py-0.5 bg-blue-500 text-white text-xs rounded-full">
                                                        Текущее
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                                {PLATFORM_NAMES[device.platform]}
                                            </p>
                                            <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                                                {formatLastActive(device.last_active_at)}
                                                {device.ip_address && ` · ${device.ip_address}`}
                                            </p>
                                        </div>

                                        {!device.is_current && (
                                            <button
                                                onClick={() => handleRemoveDevice(device.id)}
                                                className="p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                                                title="Завершить сессию"
                                            >
                                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                                </svg>
                                            </button>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {devices.length > 1 && (
                            <button
                                onClick={handleTerminateAll}
                                className="w-full py-2 px-4 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                            >
                                Завершить все другие сессии
                            </button>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
