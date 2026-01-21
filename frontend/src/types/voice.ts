/**
 * Типы для голосовых сообщений
 */

export interface VoiceMessageCreate {
    chat_id: string;
    duration: number;
    waveform?: number[];
}

export interface VoiceMessageResponse {
    id: string;
    message_id: string;
    chat_id: string;
    sender_id: string;
    file_url: string;
    duration: number;
    waveform: number[] | null;
    is_listened: boolean;
    created_at: string;
}

export interface VoiceUploadResponse {
    message_id: string;
    chat_id: string;
    duration: number;
    created_at: string;
}

export interface VoiceTranscription {
    message_id: string;
    text: string;
    language: string | null;
    confidence: number | null;
}

export interface RecordingState {
    isRecording: boolean;
    isPaused: boolean;
    duration: number;
    waveform: number[];
}
