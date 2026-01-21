/**
 * Сервис медиафайлов
 */

import type { MediaFile, UploadResponse } from '../types/media';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const mediaService = {
    async upload(file: File): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append('file', file);

        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/media/upload`, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${token}`,
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ message: 'Ошибка загрузки' }));
            throw new Error(error.detail?.message || error.message || 'Ошибка загрузки файла');
        }

        return response.json();
    },

    async getFile(fileId: string): Promise<MediaFile> {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/media/${fileId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Файл не найден');
        }

        return response.json();
    },

    async deleteFile(fileId: string): Promise<void> {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE_URL}/media/${fileId}`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Ошибка удаления файла');
        }
    },

    getDownloadUrl(fileId: string): string {
        return `${API_BASE_URL}/media/${fileId}/download`;
    },

    formatFileSize(bytes: number): string {
        if (bytes === 0) return '0 Б';
        const k = 1024;
        const sizes = ['Б', 'КБ', 'МБ', 'ГБ'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    },
};
