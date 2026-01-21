/**
 * Форма регистрации
 */

import { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

interface RegisterFormProps {
    onSwitchToLogin: () => void;
}

export function RegisterForm({ onSwitchToLogin }: RegisterFormProps) {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [validationError, setValidationError] = useState('');
    const { register, isLoading, error, clearError } = useAuthStore();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        clearError();
        setValidationError('');

        if (password !== confirmPassword) {
            setValidationError('Пароли не совпадают');
            return;
        }

        if (password.length < 8) {
            setValidationError('Пароль должен быть не менее 8 символов');
            return;
        }

        try {
            await register(email, password, name);
        } catch {
            // Ошибка уже сохранена в store
        }
    };

    const displayError = validationError || error;

    return (
        <div className="w-full max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8">
                <div className="text-center mb-8">
                    <h1 className="text-2xl font-bold text-gray-900">Регистрация</h1>
                    <p className="text-gray-600 mt-2">Создайте новый аккаунт</p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {displayError && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                            {displayError}
                        </div>
                    )}

                    <Input
                        label="Имя"
                        type="text"
                        name="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Ваше имя"
                        required
                        autoComplete="name"
                    />

                    <Input
                        label="Email"
                        type="email"
                        name="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="email@example.com"
                        required
                        autoComplete="email"
                    />

                    <Input
                        label="Пароль"
                        type="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Минимум 8 символов"
                        required
                        autoComplete="new-password"
                    />

                    <Input
                        label="Подтверждение пароля"
                        type="password"
                        name="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Повторите пароль"
                        required
                        autoComplete="new-password"
                    />

                    <Button
                        type="submit"
                        className="w-full"
                        size="lg"
                        isLoading={isLoading}
                    >
                        Зарегистрироваться
                    </Button>
                </form>

                <div className="mt-6 text-center">
                    <p className="text-gray-600">
                        Уже есть аккаунт?{' '}
                        <button
                            type="button"
                            onClick={onSwitchToLogin}
                            className="text-blue-600 hover:text-blue-700 font-medium"
                        >
                            Войти
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
}
