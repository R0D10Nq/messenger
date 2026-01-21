/**
 * Компонент выбора стикеров и GIF
 */

import { useState, useEffect } from 'react';
import { stickerService } from '../../services/sticker';
import type { Gif, Sticker, StickerPack, StickerTab } from '../../types/sticker';

interface StickerPickerProps {
    onSelect: (url: string, type: 'sticker' | 'gif') => void;
    onClose: () => void;
}

export function StickerPicker({ onSelect, onClose }: StickerPickerProps) {
    const [activeTab, setActiveTab] = useState<StickerTab>('stickers');
    const [packs, setPacks] = useState<StickerPack[]>([]);
    const [selectedPack, setSelectedPack] = useState<string | null>(null);
    const [stickers, setStickers] = useState<Sticker[]>([]);
    const [recentStickers, setRecentStickers] = useState<Sticker[]>([]);
    const [gifs, setGifs] = useState<Gif[]>([]);
    const [gifQuery, setGifQuery] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadStickerPacks();
        loadRecentStickers();
    }, []);

    useEffect(() => {
        if (selectedPack) {
            loadPackStickers(selectedPack);
        }
    }, [selectedPack]);

    useEffect(() => {
        if (activeTab === 'gifs') {
            loadTrendingGifs();
        }
    }, [activeTab]);

    const loadStickerPacks = async () => {
        try {
            const data = await stickerService.getStickerPacks();
            setPacks(data.packs);
            if (data.packs.length > 0) {
                setSelectedPack(data.packs[0].id);
            }
        } catch (err) {
            console.error('Ошибка загрузки стикеров:', err);
        }
    };

    const loadRecentStickers = async () => {
        try {
            const data = await stickerService.getRecentStickers();
            setRecentStickers(data.stickers);
        } catch (err) {
            console.error('Ошибка загрузки недавних стикеров:', err);
        }
    };

    const loadPackStickers = async (packId: string) => {
        try {
            setLoading(true);
            const data = await stickerService.getStickerPack(packId);
            setStickers(data.stickers);
        } catch (err) {
            console.error('Ошибка загрузки стикеров:', err);
        } finally {
            setLoading(false);
        }
    };

    const loadTrendingGifs = async () => {
        try {
            setLoading(true);
            const data = await stickerService.getTrendingGifs();
            setGifs(data.gifs);
        } catch (err) {
            console.error('Ошибка загрузки GIF:', err);
        } finally {
            setLoading(false);
        }
    };

    const searchGifs = async () => {
        if (!gifQuery.trim()) {
            loadTrendingGifs();
            return;
        }
        try {
            setLoading(true);
            const data = await stickerService.searchGifs(gifQuery);
            setGifs(data.gifs);
        } catch (err) {
            console.error('Ошибка поиска GIF:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleStickerClick = (sticker: Sticker) => {
        onSelect(sticker.file_url, 'sticker');
    };

    const handleGifClick = (gif: Gif) => {
        onSelect(gif.url, 'gif');
    };

    return (
        <div className="absolute bottom-full left-0 mb-2 w-80 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div className="flex border-b border-gray-200 dark:border-gray-700">
                <button
                    onClick={() => setActiveTab('recent')}
                    className={`flex-1 py-2 text-sm font-medium transition-colors ${activeTab === 'recent'
                            ? 'text-blue-500 border-b-2 border-blue-500'
                            : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                        }`}
                >
                    Недавние
                </button>
                <button
                    onClick={() => setActiveTab('stickers')}
                    className={`flex-1 py-2 text-sm font-medium transition-colors ${activeTab === 'stickers'
                            ? 'text-blue-500 border-b-2 border-blue-500'
                            : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                        }`}
                >
                    Стикеры
                </button>
                <button
                    onClick={() => setActiveTab('gifs')}
                    className={`flex-1 py-2 text-sm font-medium transition-colors ${activeTab === 'gifs'
                            ? 'text-blue-500 border-b-2 border-blue-500'
                            : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                        }`}
                >
                    GIF
                </button>
                <button
                    onClick={onClose}
                    className="px-3 py-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            {activeTab === 'gifs' && (
                <div className="p-2 border-b border-gray-200 dark:border-gray-700">
                    <input
                        type="text"
                        value={gifQuery}
                        onChange={(e) => setGifQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && searchGifs()}
                        placeholder="Поиск GIF..."
                        className="w-full px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>
            )}

            <div className="h-64 overflow-y-auto">
                {loading ? (
                    <div className="flex items-center justify-center h-full">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500" />
                    </div>
                ) : activeTab === 'recent' ? (
                    <div className="grid grid-cols-4 gap-1 p-2">
                        {recentStickers.length === 0 ? (
                            <div className="col-span-4 text-center text-gray-500 py-8">
                                Нет недавних стикеров
                            </div>
                        ) : (
                            recentStickers.map((sticker) => (
                                <button
                                    key={sticker.id}
                                    onClick={() => handleStickerClick(sticker)}
                                    className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                                >
                                    <img
                                        src={sticker.file_url}
                                        alt={sticker.emoji}
                                        className="w-full h-auto object-contain"
                                        loading="lazy"
                                    />
                                </button>
                            ))
                        )}
                    </div>
                ) : activeTab === 'stickers' ? (
                    <div>
                        <div className="flex gap-1 p-2 border-b border-gray-200 dark:border-gray-700 overflow-x-auto">
                            {packs.map((pack) => (
                                <button
                                    key={pack.id}
                                    onClick={() => setSelectedPack(pack.id)}
                                    className={`flex-shrink-0 w-10 h-10 rounded-lg overflow-hidden border-2 transition-colors ${selectedPack === pack.id
                                            ? 'border-blue-500'
                                            : 'border-transparent hover:border-gray-300 dark:hover:border-gray-600'
                                        }`}
                                >
                                    {pack.cover_url ? (
                                        <img src={pack.cover_url} alt={pack.name} className="w-full h-full object-cover" />
                                    ) : (
                                        <div className="w-full h-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-xs">
                                            {pack.name.charAt(0)}
                                        </div>
                                    )}
                                </button>
                            ))}
                        </div>
                        <div className="grid grid-cols-4 gap-1 p-2">
                            {stickers.map((sticker) => (
                                <button
                                    key={sticker.id}
                                    onClick={() => handleStickerClick(sticker)}
                                    className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                                >
                                    <img
                                        src={sticker.file_url}
                                        alt={sticker.emoji}
                                        className="w-full h-auto object-contain"
                                        loading="lazy"
                                    />
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="grid grid-cols-2 gap-1 p-2">
                        {gifs.length === 0 ? (
                            <div className="col-span-2 text-center text-gray-500 py-8">
                                GIF не найдены
                            </div>
                        ) : (
                            gifs.map((gif) => (
                                <button
                                    key={gif.id}
                                    onClick={() => handleGifClick(gif)}
                                    className="rounded overflow-hidden hover:opacity-80 transition-opacity"
                                >
                                    <img
                                        src={gif.preview_url}
                                        alt={gif.title}
                                        className="w-full h-24 object-cover"
                                        loading="lazy"
                                    />
                                </button>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
