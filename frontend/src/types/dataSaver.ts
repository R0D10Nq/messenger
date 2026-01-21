/**
 * Типы для режима экономии данных
 */

export interface DataSaverSettings {
    enabled: boolean;
    autoDownloadImages: boolean;
    autoDownloadVideos: boolean;
    autoDownloadAudio: boolean;
    autoDownloadDocuments: boolean;
    imageQuality: ImageQuality;
    videoQuality: VideoQuality;
    preloadMedia: boolean;
    reducedAnimations: boolean;
    compressUploads: boolean;
}

export type ImageQuality = 'low' | 'medium' | 'high' | 'original';
export type VideoQuality = 'low' | 'medium' | 'high';

export const IMAGE_QUALITY_LABELS: Record<ImageQuality, string> = {
    low: 'Низкое (экономия трафика)',
    medium: 'Среднее',
    high: 'Высокое',
    original: 'Оригинал',
};

export const VIDEO_QUALITY_LABELS: Record<VideoQuality, string> = {
    low: '360p (экономия трафика)',
    medium: '720p',
    high: '1080p',
};

export const DEFAULT_DATA_SAVER_SETTINGS: DataSaverSettings = {
    enabled: false,
    autoDownloadImages: true,
    autoDownloadVideos: false,
    autoDownloadAudio: true,
    autoDownloadDocuments: true,
    imageQuality: 'high',
    videoQuality: 'medium',
    preloadMedia: true,
    reducedAnimations: false,
    compressUploads: false,
};

export const DATA_SAVER_PRESET: DataSaverSettings = {
    enabled: true,
    autoDownloadImages: false,
    autoDownloadVideos: false,
    autoDownloadAudio: false,
    autoDownloadDocuments: false,
    imageQuality: 'low',
    videoQuality: 'low',
    preloadMedia: false,
    reducedAnimations: true,
    compressUploads: true,
};
