/**
 * Сервис звонков
 */

import { api } from './api';
import type { Call, CallActionRequest, CallType } from '../types/call';

export const callService = {
    async initiateCall(calleeId: string, callType: CallType): Promise<Call> {
        return api.post<Call>('/calls', { callee_id: calleeId, call_type: callType });
    },

    async getCall(callId: string): Promise<Call> {
        return api.get<Call>(`/calls/${callId}`);
    },

    async callAction(callId: string, action: CallActionRequest['action']): Promise<Call> {
        return api.post<Call>(`/calls/${callId}/action`, { action });
    },

    async getCallHistory(limit = 50, offset = 0): Promise<{ calls: Call[]; total: number }> {
        return api.get(`/calls?limit=${limit}&offset=${offset}`);
    },

    formatDuration(seconds: number | null): string {
        if (!seconds) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    },
};
