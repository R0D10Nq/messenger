/**
 * Типы для медиафайлов
 */

export type MediaType = 'image' | 'video' | 'audio' | 'voice' | 'file';

export interface MediaFile {
    id: string;
    user_id: string;
    filename: string;
    original_filename: string;
    media_type: MediaType;
    mime_type: string;
    size_bytes: number;
    url: string;
    created_at: string;
}

export interface UploadResponse {
    id: string;
    url: string;
    filename: string;
    media_type: MediaType;
    size_bytes: number;
}

export interface Attachment {
    id: string;
    media_file: MediaFile;
}
