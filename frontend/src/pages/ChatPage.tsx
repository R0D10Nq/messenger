/**
 * Страница чатов
 */

import { useAuthStore } from '../store/authStore';
import { ChatList } from '../components/chat/ChatList';
import { ChatHeader } from '../components/chat/ChatHeader';
import { MessageList } from '../components/chat/MessageList';
import { MessageInput } from '../components/chat/MessageInput';
import { Button } from '../components/ui/Button';

export function ChatPage() {
    const { user, logout, isLoading } = useAuthStore();

    return (
        <div className="h-screen flex flex-col bg-gray-100">
            {/* Header */}
            <header className="bg-white shadow-sm border-b px-4 py-3 flex items-center justify-between flex-shrink-0">
                <h1 className="text-xl font-bold text-blue-600">Messenger</h1>
                <div className="flex items-center gap-4">
                    <span className="text-gray-700">{user?.name}</span>
                    <Button variant="outline" size="sm" onClick={logout} isLoading={isLoading}>
                        Выйти
                    </Button>
                </div>
            </header>

            {/* Main content */}
            <div className="flex flex-1 overflow-hidden">
                {/* Sidebar - Chat list */}
                <aside className="w-80 bg-white border-r flex flex-col flex-shrink-0">
                    <div className="p-4 border-b">
                        <input
                            type="search"
                            placeholder="Поиск чатов..."
                            className="w-full px-3 py-2 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <ChatList />
                    </div>
                </aside>

                {/* Chat area */}
                <main className="flex-1 flex flex-col bg-white">
                    <ChatHeader />
                    <MessageList />
                    <MessageInput />
                </main>
            </div>
        </div>
    );
}
