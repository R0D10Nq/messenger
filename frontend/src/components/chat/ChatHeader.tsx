/**
 * Заголовок чата
 */

import { useChatStore } from '../../store/chatStore';

export function ChatHeader() {
    const { currentChat } = useChatStore();

    if (!currentChat) return null;

    const displayName = currentChat.name || 'Без имени';
    const membersCount = currentChat.members.length;
    const isGroup = currentChat.chat_type === 'group';

    return (
        <div className="border-b bg-white px-4 py-3 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold">
                {displayName[0]?.toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
                <h2 className="font-semibold text-gray-900 truncate">{displayName}</h2>
                <p className="text-sm text-gray-500">
                    {isGroup
                        ? `${membersCount} участник${membersCount > 1 ? (membersCount < 5 ? 'а' : 'ов') : ''}`
                        : 'В сети'}
                </p>
            </div>
            <div className="flex items-center gap-2">
                <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="w-5 h-5 text-gray-600"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z"
                        />
                    </svg>
                </button>
                <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="w-5 h-5 text-gray-600"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z"
                        />
                    </svg>
                </button>
            </div>
        </div>
    );
}
