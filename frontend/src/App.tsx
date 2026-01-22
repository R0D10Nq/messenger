import { useEffect, useState } from 'react';
import { useAuthStore } from './store/authStore';
import { AuthPage } from './pages/AuthPage';
import { ChatPage } from './pages/ChatPage';

function App() {
    const { isAuthenticated, user, checkAuth } = useAuthStore();
    const [isInitializing, setIsInitializing] = useState(true);

    useEffect(() => {
        const init = async () => {
            // Если уже авторизован и есть user - не делать запрос
            if (!isAuthenticated || !user) {
                await checkAuth();
            }
            setIsInitializing(false);
        };
        init();
    }, []);

    if (isInitializing) {
        return (
            <div className="min-h-screen bg-gray-100 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
            </div>
        );
    }

    return isAuthenticated ? <ChatPage /> : <AuthPage />;
}

export default App;
