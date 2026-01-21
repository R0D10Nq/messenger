/**
 * Типы для мульти-устройств
 */

export type DeviceType = 'desktop' | 'mobile' | 'tablet' | 'web' | 'unknown';
export type DevicePlatform = 'windows' | 'macos' | 'linux' | 'android' | 'ios' | 'web' | 'unknown';

export interface DeviceResponse {
    id: string;
    user_id: string;
    device_name: string;
    device_type: DeviceType;
    platform: DevicePlatform;
    is_current: boolean;
    last_active_at: string;
    ip_address: string | null;
    location: string | null;
    created_at: string;
}

export interface DeviceListResponse {
    devices: DeviceResponse[];
    current_device_id: string | null;
}

export interface RegisterDeviceRequest {
    device_name: string;
    device_type?: DeviceType;
    platform?: DevicePlatform;
    push_token?: string;
}

export interface SessionResponse {
    device_id: string;
    device_name: string;
    device_type: DeviceType;
    platform: DevicePlatform;
    is_current: boolean;
    last_active_at: string;
    ip_address: string | null;
    location: string | null;
}

export const DEVICE_TYPE_ICONS: Record<DeviceType, string> = {
    desktop: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    mobile: 'M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z',
    tablet: 'M12 18h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    web: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9',
    unknown: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
};

export const PLATFORM_NAMES: Record<DevicePlatform, string> = {
    windows: 'Windows',
    macos: 'macOS',
    linux: 'Linux',
    android: 'Android',
    ios: 'iOS',
    web: 'Браузер',
    unknown: 'Неизвестно',
};
