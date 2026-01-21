/**
 * Сервис для защиты контента
 */

import type { ContentProtectionSettings, ProtectionLevel } from '../types/contentProtection';
import { DEFAULT_PROTECTION_SETTINGS, PROTECTION_LEVEL_CONFIG } from '../types/contentProtection';

const STORAGE_KEY = 'content_protection_settings';

class ContentProtectionService {
    private settings: ContentProtectionSettings = DEFAULT_PROTECTION_SETTINGS;
    private listeners: Set<() => void> = new Set();

    constructor() {
        this.loadSettings();
        this.setupProtection();
    }

    private loadSettings(): void {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                this.settings = { ...DEFAULT_PROTECTION_SETTINGS, ...JSON.parse(stored) };
            } catch {
                this.settings = DEFAULT_PROTECTION_SETTINGS;
            }
        }
    }

    private saveSettings(): void {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.settings));
    }

    private setupProtection(): void {
        document.addEventListener('contextmenu', this.handleContextMenu);
        document.addEventListener('copy', this.handleCopy);
        document.addEventListener('keydown', this.handleKeyDown);

        if (this.settings.preventScreenshot) {
            this.enableScreenshotProtection();
        }
    }

    private handleContextMenu = (e: MouseEvent): void => {
        const target = e.target as HTMLElement;
        if (target.closest('[data-protected="true"]') && this.settings.preventCopy) {
            e.preventDefault();
        }
    };

    private handleCopy = (e: ClipboardEvent): void => {
        const selection = window.getSelection();
        const target = selection?.anchorNode?.parentElement;
        if (target?.closest('[data-protected="true"]') && this.settings.preventCopy) {
            e.preventDefault();
        }
    };

    private handleKeyDown = (e: KeyboardEvent): void => {
        const target = e.target as HTMLElement;
        const isProtected = target.closest('[data-protected="true"]');

        if (isProtected && this.settings.preventCopy) {
            if ((e.ctrlKey || e.metaKey) && (e.key === 'c' || e.key === 'C')) {
                e.preventDefault();
            }
        }

        if (this.settings.preventScreenshot) {
            if (e.key === 'PrintScreen') {
                e.preventDefault();
                this.showScreenshotWarning();
            }
        }
    };

    private enableScreenshotProtection(): void {
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
    }

    private handleVisibilityChange = (): void => {
        if (document.hidden && this.settings.preventScreenshot) {
            this.blurProtectedContent();
        } else {
            this.unblurProtectedContent();
        }
    };

    private blurProtectedContent(): void {
        const protectedElements = document.querySelectorAll('[data-protected="true"]');
        protectedElements.forEach((el) => {
            (el as HTMLElement).style.filter = 'blur(20px)';
        });
    }

    private unblurProtectedContent(): void {
        const protectedElements = document.querySelectorAll('[data-protected="true"]');
        protectedElements.forEach((el) => {
            (el as HTMLElement).style.filter = '';
        });
    }

    private showScreenshotWarning(): void {
        console.warn('Скриншоты защищённого контента запрещены');
    }

    getSettings(): ContentProtectionSettings {
        return { ...this.settings };
    }

    updateSettings(updates: Partial<ContentProtectionSettings>): void {
        this.settings = { ...this.settings, ...updates };
        this.saveSettings();

        if (updates.preventScreenshot !== undefined) {
            if (updates.preventScreenshot) {
                this.enableScreenshotProtection();
            }
        }

        this.notifyListeners();
    }

    setProtectionLevel(level: ProtectionLevel): void {
        const config = PROTECTION_LEVEL_CONFIG[level];
        this.updateSettings(config);
    }

    isContentProtected(): boolean {
        return this.settings.preventCopy || this.settings.preventScreenshot;
    }

    canForward(): boolean {
        return !this.settings.preventForward;
    }

    getWatermarkText(userId: string): string {
        if (!this.settings.watermarkEnabled) return '';
        return `ID: ${userId.slice(0, 8)}`;
    }

    subscribe(listener: () => void): () => void {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }

    private notifyListeners(): void {
        this.listeners.forEach((listener) => listener());
    }

    destroy(): void {
        document.removeEventListener('contextmenu', this.handleContextMenu);
        document.removeEventListener('copy', this.handleCopy);
        document.removeEventListener('keydown', this.handleKeyDown);
        document.removeEventListener('visibilitychange', this.handleVisibilityChange);
    }
}

export const contentProtectionService = new ContentProtectionService();
