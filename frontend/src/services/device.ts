/**
 * Сервис для работы с устройствами
 */

import { api } from './api';
import type {
    DeviceListResponse,
    DeviceResponse,
    RegisterDeviceRequest,
    SessionResponse,
} from '../types/device';

export const deviceService = {
    async registerDevice(request: RegisterDeviceRequest): Promise<DeviceResponse> {
        return api.post<DeviceResponse>('/devices', request);
    },

    async listDevices(): Promise<DeviceListResponse> {
        return api.get<DeviceListResponse>('/devices');
    },

    async getDevice(deviceId: string): Promise<DeviceResponse> {
        return api.get<DeviceResponse>(`/devices/${deviceId}`);
    },

    async updateDevice(deviceId: string, deviceName: string): Promise<DeviceResponse> {
        return api.put<DeviceResponse>(`/devices/${deviceId}`, { device_name: deviceName });
    },

    async removeDevice(deviceId: string): Promise<void> {
        return api.delete(`/devices/${deviceId}`);
    },

    async listActiveSessions(): Promise<SessionResponse[]> {
        return api.get<SessionResponse[]>('/devices/sessions/active');
    },

    async terminateSession(deviceId: string): Promise<void> {
        return api.post('/devices/sessions/terminate', { device_ids: [deviceId] });
    },

    async terminateAllOtherSessions(): Promise<void> {
        return api.post('/devices/sessions/terminate', { terminate_all_except_current: true });
    },

    getDeviceName(): string {
        const ua = navigator.userAgent;
        if (/Windows/.test(ua)) return 'Windows PC';
        if (/Macintosh/.test(ua)) return 'Mac';
        if (/Linux/.test(ua) && !/Android/.test(ua)) return 'Linux PC';
        if (/Android/.test(ua)) return 'Android';
        if (/iPhone|iPad/.test(ua)) return 'iPhone';
        return 'Браузер';
    },
};
