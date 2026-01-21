/**
 * Сервис для работы с голосовыми сообщениями
 */

import { api } from './api';
import type { VoiceTranscription, VoiceUploadResponse } from '../types/voice';

export const voiceService = {
    async uploadVoiceMessage(
        chatId: string,
        audioBlob: Blob,
        duration: number
    ): Promise<VoiceUploadResponse> {
        const formData = new FormData();
        formData.append('file', audioBlob, 'voice.webm');

        const response = await fetch(
            `${import.meta.env.VITE_API_URL || ''}/api/voice/upload?chat_id=${chatId}&duration=${duration}`,
            {
                method: 'POST',
                body: formData,
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`,
                },
            }
        );

        if (!response.ok) {
            throw new Error('Ошибка загрузки голосового сообщения');
        }

        return response.json();
    },

    async markAsListened(messageId: string): Promise<void> {
        return api.post(`/voice/${messageId}/listen`, {});
    },

    async getTranscription(messageId: string): Promise<VoiceTranscription> {
        return api.get<VoiceTranscription>(`/voice/${messageId}/transcribe`);
    },

    async getVoiceMessages(chatId: string, limit = 20, offset = 0): Promise<unknown[]> {
        return api.get(`/voice/chat/${chatId}?limit=${limit}&offset=${offset}`);
    },
};

export function formatDuration(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

export function generateWaveform(analyser: AnalyserNode): number[] {
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(dataArray);

    const samples = 50;
    const step = Math.floor(dataArray.length / samples);
    const waveform: number[] = [];

    for (let i = 0; i < samples; i++) {
        const value = dataArray[i * step];
        waveform.push(Math.round((value / 255) * 100));
    }

    return waveform;
}
