/**
 * Сервис для перевода сообщений
 */

import { api } from './api';
import type {
    DetectLanguageResponse,
    SupportedLanguagesResponse,
    TranslateResponse,
    TranslateTextRequest,
} from '../types/translate';

export const translateService = {
    async translateMessage(messageId: string, targetLanguage: string): Promise<TranslateResponse> {
        return api.post<TranslateResponse>('/translate/message', {
            message_id: messageId,
            target_language: targetLanguage,
        });
    },

    async translateText(request: TranslateTextRequest): Promise<TranslateResponse> {
        return api.post<TranslateResponse>('/translate/text', request);
    },

    async detectLanguage(text: string): Promise<DetectLanguageResponse> {
        return api.post<DetectLanguageResponse>('/translate/detect', { text });
    },

    async getSupportedLanguages(): Promise<SupportedLanguagesResponse> {
        return api.get<SupportedLanguagesResponse>('/translate/languages');
    },
};
