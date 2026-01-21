/**
 * Типы для поиска
 */

export type SearchType = 'all' | 'text' | 'media' | 'voice';

export interface SearchResultItem {
    message_id: string;
    chat_id: string;
    chat_name: string;
    sender_id: string;
    sender_name: string;
    content: string;
    highlight: string;
    created_at: string;
    has_media: boolean;
}

export interface SearchResponse {
    query: string;
    total_count: number;
    results: SearchResultItem[];
    has_more: boolean;
}

export interface SearchParams {
    q: string;
    chat_id?: string;
    search_type?: SearchType;
    sender_id?: string;
    limit?: number;
    offset?: number;
}
