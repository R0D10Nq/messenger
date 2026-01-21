/**
 * Сервис для управления режимом экономии данных
 */

import type { DataSaverSettings } from '../types/dataSaver';
import { DATA_SAVER_PRESET, DEFAULT_DATA_SAVER_SETTINGS } from '../types/dataSaver';

const STORAGE_KEY = 'data_saver_settings';

export const dataSaverService = {
    getSettings(): DataSaverSettings {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                return { ...DEFAULT_DATA_SAVER_SETTINGS, ...JSON.parse(stored) };
            } catch {
                return DEFAULT_DATA_SAVER_SETTINGS;
            }
        }
        return DEFAULT_DATA_SAVER_SETTINGS;
    },

    saveSettings(settings: DataSaverSettings): void {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    },

    isEnabled(): boolean {
        return this.getSettings().enabled;
    },

    enableDataSaver(): void {
        this.saveSettings(DATA_SAVER_PRESET);
    },

    disableDataSaver(): void {
        this.saveSettings(DEFAULT_DATA_SAVER_SETTINGS);
    },

    shouldAutoDownload(mediaType: 'images' | 'videos' | 'audio' | 'documents'): boolean {
        const settings = this.getSettings();
        switch (mediaType) {
            case 'images':
                return settings.autoDownloadImages;
            case 'videos':
                return settings.autoDownloadVideos;
            case 'audio':
                return settings.autoDownloadAudio;
            case 'documents':
                return settings.autoDownloadDocuments;
            default:
                return true;
        }
    },

    getImageQualityParam(): string {
        const settings = this.getSettings();
        switch (settings.imageQuality) {
            case 'low':
                return 'w=400&q=60';
            case 'medium':
                return 'w=800&q=80';
            case 'high':
                return 'w=1200&q=90';
            default:
                return '';
        }
    },

    shouldReduceAnimations(): boolean {
        return this.getSettings().reducedAnimations;
    },

    shouldPreloadMedia(): boolean {
        return this.getSettings().preloadMedia;
    },
};
