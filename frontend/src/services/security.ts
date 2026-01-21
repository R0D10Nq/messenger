/**
 * Сервис безопасности (2FA)
 */

import { api } from './api';
import type { Setup2FAResponse, TwoFactorStatus, Verify2FAResponse } from '../types/security';

export const securityService = {
    async get2FAStatus(): Promise<TwoFactorStatus> {
        return api.get<TwoFactorStatus>('/2fa/status');
    },

    async setup2FA(): Promise<Setup2FAResponse> {
        return api.post<Setup2FAResponse>('/2fa/setup');
    },

    async verify2FA(code: string): Promise<Verify2FAResponse> {
        return api.post<Verify2FAResponse>('/2fa/verify', { code });
    },

    async disable2FA(code: string): Promise<Verify2FAResponse> {
        return api.post<Verify2FAResponse>('/2fa/disable', { code });
    },
};
