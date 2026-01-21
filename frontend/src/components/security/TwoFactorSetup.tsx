/**
 * Настройка двухфакторной аутентификации [SECURITY]
 */

import { useState, useEffect } from 'react';
import { securityService } from '../../services/security';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import type { Setup2FAResponse, TwoFactorStatus } from '../../types/security';

interface TwoFactorSetupProps {
    isOpen: boolean;
    onClose: () => void;
}

export function TwoFactorSetup({ isOpen, onClose }: TwoFactorSetupProps) {
    const [status, setStatus] = useState<TwoFactorStatus | null>(null);
    const [setupData, setSetupData] = useState<Setup2FAResponse | null>(null);
    const [code, setCode] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    useEffect(() => {
        if (isOpen) {
            loadStatus();
        }
    }, [isOpen]);

    const loadStatus = async () => {
        try {
            const data = await securityService.get2FAStatus();
            setStatus(data);
        } catch {
            setError('Ошибка загрузки статуса');
        }
    };

    const handleSetup = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const data = await securityService.setup2FA();
            setSetupData(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка настройки');
        } finally {
            setIsLoading(false);
        }
    };

    const handleVerify = async () => {
        if (code.length !== 6) {
            setError('Код должен содержать 6 цифр');
            return;
        }

        setIsLoading(true);
        setError(null);
        try {
            await securityService.verify2FA(code);
            setSuccess('2FA успешно включена!');
            setSetupData(null);
            await loadStatus();
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Неверный код');
        } finally {
            setIsLoading(false);
        }
    };

    const handleDisable = async () => {
        if (code.length !== 6) {
            setError('Введите код из приложения');
            return;
        }

        setIsLoading(true);
        setError(null);
        try {
            await securityService.disable2FA(code);
            setSuccess('2FA отключена');
            setCode('');
            await loadStatus();
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Неверный код');
        } finally {
            setIsLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/50" onClick={onClose} />
            <div className="relative bg-white rounded-2xl shadow-xl w-full max-w-md mx-4 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">
                    Двухфакторная аутентификация
                </h2>

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-4">
                        {error}
                    </div>
                )}

                {success && (
                    <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm mb-4">
                        {success}
                    </div>
                )}

                {status?.enabled ? (
                    <div className="space-y-4">
                        <div className="flex items-center gap-2 text-green-600">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span className="font-medium">2FA включена</span>
                        </div>

                        <Input
                            label="Код для отключения"
                            value={code}
                            onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                            placeholder="000000"
                            maxLength={6}
                        />

                        <Button
                            variant="secondary"
                            className="w-full"
                            onClick={handleDisable}
                            isLoading={isLoading}
                        >
                            Отключить 2FA
                        </Button>
                    </div>
                ) : setupData ? (
                    <div className="space-y-4">
                        <p className="text-sm text-gray-600">
                            Отсканируйте QR-код в приложении Google Authenticator или Authy:
                        </p>

                        <div className="flex justify-center">
                            <img
                                src={`data:image/png;base64,${setupData.qr_code_base64}`}
                                alt="QR код для 2FA"
                                className="w-48 h-48"
                            />
                        </div>

                        <details className="text-sm">
                            <summary className="cursor-pointer text-gray-500">
                                Или введите код вручную
                            </summary>
                            <code className="block mt-2 p-2 bg-gray-100 rounded text-xs break-all">
                                {setupData.secret}
                            </code>
                        </details>

                        <Input
                            label="Код подтверждения"
                            value={code}
                            onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                            placeholder="000000"
                            maxLength={6}
                        />

                        <Button className="w-full" onClick={handleVerify} isLoading={isLoading}>
                            Подтвердить
                        </Button>
                    </div>
                ) : (
                    <div className="space-y-4">
                        <p className="text-sm text-gray-600">
                            Двухфакторная аутентификация добавляет дополнительный уровень защиты вашего аккаунта.
                        </p>

                        <Button className="w-full" onClick={handleSetup} isLoading={isLoading}>
                            Настроить 2FA
                        </Button>
                    </div>
                )}

                <div className="mt-6">
                    <Button variant="outline" className="w-full" onClick={onClose}>
                        Закрыть
                    </Button>
                </div>
            </div>
        </div>
    );
}
