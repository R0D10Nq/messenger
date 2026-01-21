/**
 * Типы для упоминаний и превью ссылок
 */

export interface MentionData {
    user_id: string;
    user_name: string;
    offset: number;
    length: number;
}

export interface LinkPreview {
    url: string;
    title?: string;
    description?: string;
    image_url?: string;
    site_name?: string;
}

export interface ParsedMessage {
    content: string;
    mentions: MentionData[];
    urls: string[];
}
