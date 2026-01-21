/**
 * Сервис для работы со стикерами и GIF
 */

import { api } from './api';
import type {
    GifSearchResponse,
    RecentStickersResponse,
    StickerPackDetail,
    StickerPacksResponse,
    TrendingGifsResponse,
} from '../types/sticker';

export const stickerService = {
    async getStickerPacks(): Promise<StickerPacksResponse> {
        return api.get<StickerPacksResponse>('/stickers/packs');
    },

    async getStickerPack(packId: string): Promise<StickerPackDetail> {
        return api.get<StickerPackDetail>(`/stickers/packs/${packId}`);
    },

    async getRecentStickers(limit = 20): Promise<RecentStickersResponse> {
        return api.get<RecentStickersResponse>(`/stickers/recent?limit=${limit}`);
    },

    async addStickerPack(packId: string): Promise<void> {
        return api.post(`/stickers/packs/${packId}/add`, {});
    },

    async removeStickerPack(packId: string): Promise<void> {
        return api.delete(`/stickers/packs/${packId}/remove`);
    },

    async searchStickerPacks(query: string): Promise<StickerPacksResponse> {
        return api.get<StickerPacksResponse>(`/stickers/search?query=${encodeURIComponent(query)}`);
    },

    async searchGifs(query: string, limit = 20, offset = 0): Promise<GifSearchResponse> {
        return api.get<GifSearchResponse>(
            `/stickers/gifs/search?query=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}`
        );
    },

    async getTrendingGifs(limit = 20): Promise<TrendingGifsResponse> {
        return api.get<TrendingGifsResponse>(`/stickers/gifs/trending?limit=${limit}`);
    },
};
