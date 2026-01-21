/**
 * Индикатор онлайн статуса пользователя
 */

interface OnlineStatusProps {
    isOnline: boolean;
    lastSeenAt?: string | null;
    size?: 'sm' | 'md' | 'lg';
    showText?: boolean;
}

function formatLastSeen(lastSeenAt: string): string {
    const date = new Date(lastSeenAt);
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'только что';
    if (minutes < 60) return `${minutes} мин. назад`;
    if (hours < 24) return `${hours} ч. назад`;
    if (days < 7) return `${days} дн. назад`;

    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'short',
    });
}

const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
};

export function OnlineStatus({ isOnline, lastSeenAt, size = 'md', showText = false }: OnlineStatusProps) {
    const dotClass = sizeClasses[size];

    if (showText) {
        return (
            <div className="flex items-center gap-1.5">
                <span
                    className={`${dotClass} rounded-full ${isOnline ? 'bg-green-500' : 'bg-gray-400'
                        }`}
                />
                <span className="text-xs text-gray-500">
                    {isOnline ? 'в сети' : lastSeenAt ? formatLastSeen(lastSeenAt) : 'не в сети'}
                </span>
            </div>
        );
    }

    return (
        <span
            className={`${dotClass} rounded-full ${isOnline ? 'bg-green-500' : 'bg-gray-400'
                }`}
            title={isOnline ? 'В сети' : lastSeenAt ? `Был(а) ${formatLastSeen(lastSeenAt)}` : 'Не в сети'}
        />
    );
}
