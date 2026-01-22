/**
 * Сервис аутентификации
 */

import { api } from './api';
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types/auth';

export const authService = {
    async login(data: LoginRequest): Promise<TokenResponse> {
        const response = await api.post<TokenResponse>('/auth/login', data, { skipAuth: true });
        this.saveTokens(response);
        return response;
    },

    async register(data: RegisterRequest): Promise<TokenResponse> {
        const response = await api.post<TokenResponse>('/auth/register', data, { skipAuth: true });
        this.saveTokens(response);
        return response;
    },

    async logout(): Promise<void> {
        try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                await api.post('/auth/logout', { refresh_token: refreshToken });
            }
        } finally {
            this.clearTokens();
        }
    },

    async refreshToken(): Promise<TokenResponse> {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            throw new Error('Токен обновления отсутствует');
        }

        const response = await api.post<TokenResponse>(
            '/auth/refresh',
            { refresh_token: refreshToken },
            { skipAuth: true }
        );
        this.saveTokens(response);
        return response;
    },

    async getCurrentUser(): Promise<User> {
        return api.get<User>('/profile/me');
    },

    saveTokens(response: TokenResponse): void {
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('refresh_token', response.refresh_token);
    },

    clearTokens(): void {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    },
};
