/**
 * Сервис для экспорта переписок
 */

import { api } from './api';
import type {
    ExportChatRequest,
    ExportJob,
    ExportListResponse,
    ExportProgress,
} from '../types/export';

export const exportService = {
    async startExport(request: ExportChatRequest): Promise<ExportJob> {
        return api.post<ExportJob>('/export/chat', request);
    },

    async getExports(): Promise<ExportListResponse> {
        return api.get<ExportListResponse>('/export/jobs');
    },

    async getExportStatus(jobId: string): Promise<ExportJob> {
        return api.get<ExportJob>(`/export/jobs/${jobId}`);
    },

    async getExportProgress(jobId: string): Promise<ExportProgress> {
        return api.get<ExportProgress>(`/export/jobs/${jobId}/progress`);
    },

    async downloadExport(jobId: string): Promise<void> {
        const token = localStorage.getItem('access_token');
        const response = await fetch(
            `${import.meta.env.VITE_API_URL || ''}/api/export/jobs/${jobId}/download`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        if (!response.ok) {
            throw new Error('Ошибка скачивания экспорта');
        }

        const blob = await response.blob();
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition?.match(/filename=(.+)/)?.[1] || 'export.json';

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    },

    async deleteExport(jobId: string): Promise<void> {
        return api.delete(`/export/jobs/${jobId}`);
    },
};
