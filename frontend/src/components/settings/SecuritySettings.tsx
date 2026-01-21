/**
 * Компонент настроек безопасности
 */

import { useState } from 'react';

interface SecuritySettingsProps {
    onClose?: () => void;
}

interface SecurityState {
    twoFactorEnabled: boolean;
    activeSessions: number;
    lastPasswordChange: string;
    loginNotifications: boolean;
    unknownDeviceAlert: boolean;
    showOnlineStatus: boolean;
    allowSearchByPhone: boolean;
}

export function SecuritySettings({ onClose }: SecuritySettingsProps) {
    const [security, setSecurity] = useState<SecurityState>({
        twoFactorEnabled: false,
        activeSessions: 2,
        lastPasswordChange: '2024-12-15',
        loginNotifications: true,
        unknownDeviceAlert: true,
        showOnlineStatus: true,
        allowSearchByPhone: false,
    });

    const [showPasswordModal, setShowPasswordModal] = useState(false);

    const handleToggle = (key: keyof SecurityState) => {
        const current = security[key];
        if (typeof current === 'boolean') {
            setSecurity({ ...security, [key]: !current });
        }
    };

    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        });
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Безопасность
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
                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Двухфакторная аутентификация
                    </h3>
                    <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div className={`p-2 rounded-lg ${security.twoFactorEnabled ? 'bg-green-100 dark:bg-green-900/30' : 'bg-gray-200 dark:bg-gray-600'}`}>
                                    <svg className={`w-5 h-5 ${security.twoFactorEnabled ? 'text-green-500' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                    </svg>
                                </div>
                                <div>
                                    <p className="font-medium text-gray-900 dark:text-white">
                                        {security.twoFactorEnabled ? 'Включена' : 'Отключена'}
                                    </p>
                                    <p className="text-sm text-gray-500 dark:text-gray-400">
                                        Дополнительная защита аккаунта
                                    </p>
                                </div>
                            </div>
                            <button
                                onClick={() => handleToggle('twoFactorEnabled')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${security.twoFactorEnabled
                                        ? 'bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50'
                                        : 'bg-blue-500 text-white hover:bg-blue-600'
                                    }`}
                            >
                                {security.twoFactorEnabled ? 'Отключить' : 'Включить'}
                            </button>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Пароль
                    </h3>
                    <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="font-medium text-gray-900 dark:text-white">Пароль</p>
                                <p className="text-sm text-gray-500 dark:text-gray-400">
                                    Последнее изменение: {formatDate(security.lastPasswordChange)}
                                </p>
                            </div>
                            <button
                                onClick={() => setShowPasswordModal(true)}
                                className="px-4 py-2 bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-500 rounded-lg font-medium text-gray-900 dark:text-white transition-colors"
                            >
                                Изменить
                            </button>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Активные сессии
                    </h3>
                    <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="font-medium text-gray-900 dark:text-white">
                                    {security.activeSessions} активных устройств
                                </p>
                                <p className="text-sm text-gray-500 dark:text-gray-400">
                                    Управляйте подключёнными устройствами
                                </p>
                            </div>
                            <button className="px-4 py-2 text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg font-medium transition-colors">
                                Просмотреть
                            </button>
                        </div>
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Уведомления безопасности
                    </h3>
                    <div className="space-y-3">
                        <ToggleItem
                            title="Уведомления о входе"
                            description="Получать уведомления при входе с нового устройства"
                            checked={security.loginNotifications}
                            onChange={() => handleToggle('loginNotifications')}
                        />
                        <ToggleItem
                            title="Предупреждения о неизвестных устройствах"
                            description="Показывать предупреждения при входе с неизвестного устройства"
                            checked={security.unknownDeviceAlert}
                            onChange={() => handleToggle('unknownDeviceAlert')}
                        />
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Конфиденциальность
                    </h3>
                    <div className="space-y-3">
                        <ToggleItem
                            title="Показывать онлайн-статус"
                            description="Другие пользователи видят, когда вы в сети"
                            checked={security.showOnlineStatus}
                            onChange={() => handleToggle('showOnlineStatus')}
                        />
                        <ToggleItem
                            title="Поиск по номеру телефона"
                            description="Разрешить находить вас по номеру телефона"
                            checked={security.allowSearchByPhone}
                            onChange={() => handleToggle('allowSearchByPhone')}
                        />
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-red-500 mb-3">
                        Опасная зона
                    </h3>
                    <div className="space-y-3">
                        <button className="w-full p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-left hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors">
                            <p className="font-medium text-red-600 dark:text-red-400">Удалить аккаунт</p>
                            <p className="text-sm text-red-500/70 dark:text-red-400/70">
                                Это действие нельзя отменить
                            </p>
                        </button>
                    </div>
                </section>
            </div>

            {showPasswordModal && (
                <ChangePasswordModal onClose={() => setShowPasswordModal(false)} />
            )}
        </div>
    );
}

interface ToggleItemProps {
    title: string;
    description: string;
    checked: boolean;
    onChange: () => void;
}

function ToggleItem({ title, description, checked, onChange }: ToggleItemProps) {
    return (
        <label className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg cursor-pointer">
            <div>
                <span className="text-gray-900 dark:text-white font-medium">{title}</span>
                <p className="text-xs text-gray-500 dark:text-gray-400">{description}</p>
            </div>
            <button
                role="switch"
                aria-checked={checked}
                onClick={onChange}
                className={`relative w-12 h-6 rounded-full transition-colors ${checked ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                    }`}
            >
                <span
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${checked ? 'left-7' : 'left-1'
                        }`}
                />
            </button>
        </label>
    );
}

interface ChangePasswordModalProps {
    onClose: () => void;
}

function ChangePasswordModal({ onClose }: ChangePasswordModalProps) {
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (newPassword !== confirmPassword) {
            alert('Пароли не совпадают');
            return;
        }
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md mx-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Изменить пароль
                </h3>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        type="password"
                        placeholder="Текущий пароль"
                        value={currentPassword}
                        onChange={(e) => setCurrentPassword(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    <input
                        type="password"
                        placeholder="Новый пароль"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    <input
                        type="password"
                        placeholder="Подтвердите пароль"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    <div className="flex gap-3">
                        <button
                            type="button"
                            onClick={onClose}
                            className="flex-1 py-2 bg-gray-200 dark:bg-gray-600 rounded-lg font-medium text-gray-900 dark:text-white"
                        >
                            Отмена
                        </button>
                        <button
                            type="submit"
                            className="flex-1 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg font-medium text-white"
                        >
                            Сохранить
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
