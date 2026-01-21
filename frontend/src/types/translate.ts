/**
 * Типы для перевода сообщений
 */

export interface TranslateRequest {
    message_id: string;
    target_language: string;
}

export interface TranslateTextRequest {
    text: string;
    target_language: string;
    source_language?: string;
}

export interface TranslateResponse {
    original_text: string;
    translated_text: string;
    source_language: string;
    target_language: string;
    confidence: number | null;
}

export interface DetectLanguageResponse {
    language: string;
    confidence: number;
    language_name: string;
}

export interface Language {
    code: string;
    name: string;
}

export interface SupportedLanguagesResponse {
    languages: Language[];
}

export const COMMON_LANGUAGES: Language[] = [
    { code: 'ru', name: 'Русский' },
    { code: 'en', name: 'English' },
    { code: 'de', name: 'Deutsch' },
    { code: 'fr', name: 'Français' },
    { code: 'es', name: 'Español' },
    { code: 'zh', name: '中文' },
    { code: 'ja', name: '日本語' },
];
