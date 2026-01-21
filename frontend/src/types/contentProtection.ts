/**
 * Типы для защиты контента
 */

export interface ContentProtectionSettings {
    preventScreenshot: boolean;
    preventCopy: boolean;
    preventForward: boolean;
    watermarkEnabled: boolean;
    autoDeleteEnabled: boolean;
    autoDeleteAfterSeconds: number;
}

export interface ProtectedMessageSettings {
    isProtected: boolean;
    viewOnce: boolean;
    expiresAt: string | null;
    preventScreenshot: boolean;
    preventForward: boolean;
}

export const DEFAULT_PROTECTION_SETTINGS: ContentProtectionSettings = {
    preventScreenshot: false,
    preventCopy: false,
    preventForward: false,
    watermarkEnabled: false,
    autoDeleteEnabled: false,
    autoDeleteAfterSeconds: 30,
};

export type ProtectionLevel = 'none' | 'basic' | 'high' | 'maximum';

export const PROTECTION_LEVEL_CONFIG: Record<ProtectionLevel, Partial<ContentProtectionSettings>> = {
    none: {
        preventScreenshot: false,
        preventCopy: false,
        preventForward: false,
    },
    basic: {
        preventCopy: true,
        preventForward: false,
        preventScreenshot: false,
    },
    high: {
        preventCopy: true,
        preventForward: true,
        preventScreenshot: true,
    },
    maximum: {
        preventCopy: true,
        preventForward: true,
        preventScreenshot: true,
        watermarkEnabled: true,
        autoDeleteEnabled: true,
        autoDeleteAfterSeconds: 30,
    },
};
