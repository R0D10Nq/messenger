/**
 * Сервис для работы с приглашениями
 */

import { api } from './api';
import type {
    CreateInviteRequest,
    InviteJoinResponse,
    InviteListResponse,
    InvitePreviewResponse,
    InviteResponse,
} from '../types/invite';

export const inviteService = {
    async createInvite(request: CreateInviteRequest): Promise<InviteResponse> {
        return api.post<InviteResponse>('/invites', request);
    },

    async getPreview(code: string): Promise<InvitePreviewResponse> {
        return api.get<InvitePreviewResponse>(`/invites/preview/${code}`);
    },

    async joinByInvite(code: string): Promise<InviteJoinResponse> {
        return api.post<InviteJoinResponse>('/invites/join', { code });
    },

    async listChatInvites(chatId: string): Promise<InviteListResponse> {
        return api.get<InviteListResponse>(`/invites/chat/${chatId}`);
    },

    async revokeInvite(code: string): Promise<void> {
        return api.delete(`/invites/${code}`);
    },

    generateInviteLink(code: string): string {
        const baseUrl = window.location.origin;
        return `${baseUrl}/invite/${code}`;
    },

    async copyInviteLink(code: string): Promise<boolean> {
        try {
            const link = this.generateInviteLink(code);
            await navigator.clipboard.writeText(link);
            return true;
        } catch {
            return false;
        }
    },
};
