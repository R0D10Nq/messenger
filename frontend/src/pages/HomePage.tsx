/**
 * Главная страница (после входа)
 */

import { useAuthStore } from '../store/authStore';
import { Button } from '../components/ui/Button';

export function HomePage() {
    const { user, logout, isLoading } = useAuthStore();

    return (
        <div className="min-h-screen bg-gray-100">
            <header className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
                    <h1 className="text-xl font-bold text-blue-600">Messenger</h1>
                    <div className="flex items-center gap-4">
                        <span className="text-gray-700">
                            {user?.name || user?.email}
                        </span>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={logout}
                            isLoading={isLoading}
                        >
                            Выйти
                        </Button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 py-8">
                <div className="bg-white rounded-xl shadow-lg p-8">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">
                        Добро пожаловать, {user?.name}!
                    </h2>
                    <p className="text-gray-600">
                        Здесь будет интерфейс чатов. Разработка в процессе...
                    </p>

                    <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-blue-50 rounded-lg p-6">
                            <h3 className="font-semibold text-blue-900">Чаты</h3>
                            <p className="text-blue-700 text-sm mt-1">Личные и групповые</p>
                        </div>
                        <div className="bg-green-50 rounded-lg p-6">
                            <h3 className="font-semibold text-green-900">Контакты</h3>
                            <p className="text-green-700 text-sm mt-1">Управление контактами</p>
                        </div>
                        <div className="bg-purple-50 rounded-lg p-6">
                            <h3 className="font-semibold text-purple-900">Звонки</h3>
                            <p className="text-purple-700 text-sm mt-1">Аудио и видео</p>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
