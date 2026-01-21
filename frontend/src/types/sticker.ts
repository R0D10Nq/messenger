/**
 * Типы для стикеров и GIF
 */

export interface Sticker {
    id: string;
    pack_id: string;
    emoji: string;
    file_url: string;
    is_animated: boolean;
}

export interface StickerPack {
    id: string;
    name: string;
    description: string | null;
    cover_url: string | null;
    is_animated: boolean;
    sticker_count: number;
    author_id: string;
    is_official: boolean;
    created_at: string;
}

export interface StickerPackDetail extends StickerPack {
    stickers: Sticker[];
}

export interface StickerPacksResponse {
    packs: StickerPack[];
    total: number;
}

export interface RecentStickersResponse {
    stickers: Sticker[];
}

export interface Gif {
    id: string;
    title: string;
    url: string;
    preview_url: string;
    width: number;
    height: number;
}

export interface GifSearchResponse {
    gifs: Gif[];
    total: number;
    next_offset: number | null;
}

export interface TrendingGifsResponse {
    gifs: Gif[];
}

export type StickerTab = 'recent' | 'stickers' | 'gifs';
