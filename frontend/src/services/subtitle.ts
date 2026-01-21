/**
 * Сервис для работы с субтитрами
 */

import { api } from './api';
import type { SubtitleResponse, SubtitleSettings } from '../types/subtitle';

export const subtitleService = {
    async generateSubtitles(videoId: string, language = 'ru'): Promise<SubtitleResponse> {
        return api.post<SubtitleResponse>('/subtitles/generate', {
            video_id: videoId,
            language,
            auto_detect: true,
        });
    },

    async listVideoSubtitles(videoId: string): Promise<{ subtitles: SubtitleResponse[]; video_id: string }> {
        return api.get(`/subtitles/video/${videoId}`);
    },

    async getSubtitle(subtitleId: string): Promise<SubtitleResponse> {
        return api.get<SubtitleResponse>(`/subtitles/${subtitleId}`);
    },

    async uploadSubtitles(videoId: string, language: string, content: string): Promise<SubtitleResponse> {
        return api.post<SubtitleResponse>('/subtitles/upload', {
            video_id: videoId,
            language,
            content,
            format: 'vtt',
        });
    },

    async deleteSubtitle(subtitleId: string): Promise<void> {
        return api.delete(`/subtitles/${subtitleId}`);
    },

    async getSettings(): Promise<SubtitleSettings> {
        return api.get<SubtitleSettings>('/subtitles/settings');
    },

    async updateSettings(settings: SubtitleSettings): Promise<SubtitleSettings> {
        return api.put<SubtitleSettings>('/subtitles/settings', settings);
    },
};
