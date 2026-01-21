/**
 * Сервис для управления настройками доступности
 */

import type { AccessibilitySettings } from '../types/accessibility';
import { DEFAULT_ACCESSIBILITY_SETTINGS, FONT_SIZE_VALUES } from '../types/accessibility';

const STORAGE_KEY = 'accessibility_settings';

class AccessibilityService {
    private settings: AccessibilitySettings = DEFAULT_ACCESSIBILITY_SETTINGS;
    private listeners: Set<() => void> = new Set();

    constructor() {
        this.loadSettings();
        this.applySettings();
        this.detectSystemPreferences();
    }

    private loadSettings(): void {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
            try {
                this.settings = { ...DEFAULT_ACCESSIBILITY_SETTINGS, ...JSON.parse(stored) };
            } catch {
                this.settings = DEFAULT_ACCESSIBILITY_SETTINGS;
            }
        }
    }

    private detectSystemPreferences(): void {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.settings.reduceMotion = true;
        }

        if (window.matchMedia('(prefers-contrast: more)').matches) {
            this.settings.highContrast = true;
        }

        this.applySettings();
    }

    getSettings(): AccessibilitySettings {
        return { ...this.settings };
    }

    updateSettings(updates: Partial<AccessibilitySettings>): void {
        this.settings = { ...this.settings, ...updates };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.settings));
        this.applySettings();
        this.notifyListeners();
    }

    resetSettings(): void {
        this.settings = DEFAULT_ACCESSIBILITY_SETTINGS;
        localStorage.removeItem(STORAGE_KEY);
        this.applySettings();
        this.notifyListeners();
    }

    private applySettings(): void {
        const root = document.documentElement;

        root.style.setProperty('--base-font-size', `${FONT_SIZE_VALUES[this.settings.fontSize]}px`);

        root.classList.toggle('high-contrast', this.settings.highContrast);
        root.classList.toggle('large-text', this.settings.largeText);
        root.classList.toggle('reduce-motion', this.settings.reduceMotion);
        root.classList.toggle('focus-visible-enhanced', this.settings.focusIndicators);

        root.setAttribute('data-color-blind-mode', this.settings.colorBlindMode);

        if (this.settings.screenReaderOptimized) {
            root.setAttribute('role', 'application');
        } else {
            root.removeAttribute('role');
        }
    }

    subscribe(listener: () => void): () => void {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }

    private notifyListeners(): void {
        this.listeners.forEach((listener) => listener());
    }

    shouldReduceMotion(): boolean {
        return this.settings.reduceMotion;
    }

    getFontSize(): number {
        return FONT_SIZE_VALUES[this.settings.fontSize];
    }

    isHighContrast(): boolean {
        return this.settings.highContrast;
    }

    announceToScreenReader(message: string, priority: 'polite' | 'assertive' = 'polite'): void {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', priority);
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;

        document.body.appendChild(announcement);
        setTimeout(() => document.body.removeChild(announcement), 1000);
    }
}

export const accessibilityService = new AccessibilityService();
