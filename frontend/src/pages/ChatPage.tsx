/**
 * Страница чатов
 */

import { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { ChatList } from '../components/chat/ChatList';
import { ChatHeader } from '../components/chat/ChatHeader';
import { MessageList } from '../components/chat/MessageList';
import { MessageInput } from '../components/chat/MessageInput';
import { ProfileModal } from '../components/profile/ProfileModal';
import { ContactList } from '../components/contacts/ContactList';
import { AddContactModal } from '../components/contacts/AddContactModal';
import { Button } from '../components/ui/Button';

type SidebarTab = 'chats' | 'contacts';

export function ChatPage() {
    const { user, logout, isLoading } = useAuthStore();
    const [activeTab, setActiveTab] = useState<SidebarTab>('chats');
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [isAddContactOpen, setIsAddContactOpen] = useState(false);

    return (
        <div className="h-screen flex flex-col bg-gray-100">
            {/* Header */}
            <header className="bg-white shadow-sm border-b px-4 py-3 flex items-center justify-between flex-shrink-0">
                <h1 className="text-xl font-bold text-blue-600">Messenger</h1>
                <div className="flex items-center gap-3">
                    <button
                        onClick={() => setIsProfileOpen(true)}
                        className="flex items-center gap-2 hover:bg-gray-100 rounded-lg px-3 py-1.5 transition-colors"
                    >
                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-sm font-semibold">
                            {user?.name?.[0]?.toUpperCase()}
                        </div>
                        <span className="text-gray-700">{user?.name}</span>
                    </button>
                    <Button variant="outline" size="sm" onClick={logout} isLoading={isLoading}>
                        Выйти
                    </Button>
                </div>
            </header>

            {/* Main content */}
            <div className="flex flex-1 overflow-hidden">
                {/* Sidebar */}
                <aside className="w-80 bg-white border-r flex flex-col flex-shrink-0">
                    {/* Tabs */}
                    <div className="flex border-b">
                        <button
                            onClick={() => setActiveTab('chats')}
                            className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'chats'
                                    ? 'text-blue-600 border-b-2 border-blue-600'
                                    : 'text-gray-500 hover:text-gray-700'
                                }`}
                        >
                            Чаты
                        </button>
                        <button
                            onClick={() => setActiveTab('contacts')}
                            className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'contacts'
                                    ? 'text-blue-600 border-b-2 border-blue-600'
                                    : 'text-gray-500 hover:text-gray-700'
                                }`}
                        >
                            Контакты
                        </button>
                    </div>

                    {/* Tab content */}
                    {activeTab === 'chats' ? (
                        <>
                            <div className="p-3 border-b">
                                <input
                                    type="search"
                                    placeholder="Поиск чатов..."
                                    className="w-full px-3 py-2 bg-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                />
                            </div>
                            <div className="flex-1 overflow-y-auto">
                                <ChatList />
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="p-3 border-b">
                                <Button
                                    className="w-full"
                                    size="sm"
                                    onClick={() => setIsAddContactOpen(true)}
                                >
                                    Добавить контакт
                                </Button>
                            </div>
                            <div className="flex-1 overflow-y-auto p-2">
                                <ContactList onClose={() => setActiveTab('chats')} />
                            </div>
                        </>
                    )}
                </aside>

                {/* Chat area */}
                <main className="flex-1 flex flex-col bg-white">
                    <ChatHeader />
                    <MessageList />
                    <MessageInput />
                </main>
            </div>

            {/* Modals */}
            <ProfileModal isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
            <AddContactModal isOpen={isAddContactOpen} onClose={() => setIsAddContactOpen(false)} />
        </div>
    );
}
