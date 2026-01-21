/**
 * Типы для экспорта переписок
 */

export type ExportFormat = 'json' | 'html' | 'txt';

export type ExportStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface ExportChatRequest {
    chat_id: string;
    format: ExportFormat;
    include_media: boolean;
    start_date?: string;
    end_date?: string;
}

export interface ExportJob {
    id: string;
    chat_id: string;
    user_id: string;
    format: ExportFormat;
    status: ExportStatus;
    include_media: boolean;
    file_url: string | null;
    file_size: number | null;
    message_count: number | null;
    error_message: string | null;
    created_at: string;
    completed_at: string | null;
}

export interface ExportListResponse {
    exports: ExportJob[];
    total: number;
}

export interface ExportProgress {
    job_id: string;
    status: ExportStatus;
    progress: number;
    message_count: number | null;
    current_message: number | null;
}

export const FORMAT_LABELS: Record<ExportFormat, string> = {
    json: 'JSON',
    html: 'HTML',
    txt: 'Текстовый файл',
};

export const STATUS_LABELS: Record<ExportStatus, string> = {
    pending: 'Ожидание',
    processing: 'Обработка',
    completed: 'Завершено',
    failed: 'Ошибка',
};
