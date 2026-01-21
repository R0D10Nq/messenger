/**
 * Панель поиска по сообщениям
 */

import { useState, useCallback } from 'react';
import { searchService } from '../../services/search';
import type { SearchResultItem, SearchType } from '../../types/search';

interface SearchPanelProps {
    chatId?: string;
    onResultClick?: (result: SearchResultItem) => void;
    onClose?: () => void;
}

export function SearchPanel({ chatId, onResultClick, onClose }: SearchPanelProps) {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResultItem[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [searchType, setSearchType] = useState<SearchType>('all');
    const [totalCount, setTotalCount] = useState(0);
    const [hasMore, setHasMore] = useState(false);

    const handleSearch = useCallback(async (offset = 0) => {
        if (!query.trim()) return;

        setIsLoading(true);
        try {
            const response = await searchService.search({
                q: query,
                chat_id: chatId,
                search_type: searchType,
                offset,
            });

            if (offset === 0) {
                setResults(response.results);
            } else {
                setResults((prev) => [...prev, ...response.results]);
            }
            setTotalCount(response.total_count);
            setHasMore(response.has_more);
        } catch (error) {
            console.error('Ошибка поиска:', error);
        } finally {
            setIsLoading(false);
        }
    }, [query, chatId, searchType]);

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const formatDate = (dateStr: string) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className="flex flex-col h-full bg-white">
            <div className="p-4 border-b">
                <div className="flex items-center gap-2 mb-3">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Поиск сообщений..."
                        className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                        onClick={() => handleSearch()}
                        disabled={isLoading || !query.trim()}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                    >
                        {isLoading ? '...' : 'Найти'}
                    </button>
                    {onClose && (
                        <button
                            onClick={onClose}
                            className="p-2 text-gray-500 hover:text-gray-700"
                        >
                            ✕
                        </button>
                    )}
                </div>

                <div className="flex gap-2">
                    {(['all', 'text', 'media', 'voice'] as SearchType[]).map((type) => (
                        <button
                            key={type}
                            onClick={() => setSearchType(type)}
                            className={`px-3 py-1 text-sm rounded-full ${searchType === type
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            {type === 'all' && 'Все'}
                            {type === 'text' && 'Текст'}
                            {type === 'media' && 'Медиа'}
                            {type === 'voice' && 'Голос'}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex-1 overflow-y-auto">
                {totalCount > 0 && (
                    <div className="px-4 py-2 text-sm text-gray-500 border-b">
                        Найдено: {totalCount}
                    </div>
                )}

                {results.map((result) => (
                    <button
                        key={result.message_id}
                        onClick={() => onResultClick?.(result)}
                        className="w-full p-4 text-left hover:bg-gray-50 border-b"
                    >
                        <div className="flex justify-between items-start mb-1">
                            <span className="font-medium text-gray-900">{result.chat_name}</span>
                            <span className="text-xs text-gray-500">{formatDate(result.created_at)}</span>
                        </div>
                        <div className="text-sm text-gray-600 mb-1">{result.sender_name}</div>
                        <div className="text-sm text-gray-800">{result.highlight}</div>
                        {result.has_media && (
                            <span className="inline-block mt-1 px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded">
                                Медиа
                            </span>
                        )}
                    </button>
                ))}

                {hasMore && (
                    <button
                        onClick={() => handleSearch(results.length)}
                        disabled={isLoading}
                        className="w-full p-4 text-center text-blue-500 hover:bg-gray-50"
                    >
                        {isLoading ? 'Загрузка...' : 'Загрузить ещё'}
                    </button>
                )}

                {!isLoading && results.length === 0 && query && (
                    <div className="p-8 text-center text-gray-500">
                        Ничего не найдено
                    </div>
                )}
            </div>
        </div>
    );
}
