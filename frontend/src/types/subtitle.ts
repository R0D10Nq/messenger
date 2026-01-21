/**
 * Типы для субтитров видео
 */

export type SubtitleFormat = 'srt' | 'vtt' | 'ass';
export type SubtitleStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface SubtitleCue {
    id: number;
    start_time: number;
    end_time: number;
    text: string;
}

export interface SubtitleResponse {
    id: string;
    video_id: string;
    language: string;
    status: SubtitleStatus;
    format: SubtitleFormat;
    cues: SubtitleCue[] | null;
    created_at: string;
}

export interface SubtitleSettings {
    enabled: boolean;
    font_size: number;
    background_opacity: number;
    position: 'top' | 'bottom';
    text_color: string;
    background_color: string;
}

export const DEFAULT_SUBTITLE_SETTINGS: SubtitleSettings = {
    enabled: true,
    font_size: 16,
    background_opacity: 0.7,
    position: 'bottom',
    text_color: '#FFFFFF',
    background_color: '#000000',
};

export const SUBTITLE_LANGUAGES = [
    { code: 'ru', name: 'Русский' },
    { code: 'en', name: 'English' },
    { code: 'de', name: 'Deutsch' },
    { code: 'fr', name: 'Français' },
    { code: 'es', name: 'Español' },
];
