/**
 * Сервис локализации
 */

import { translations } from './locales';
import type { Locale, TranslationKeys } from './types';
import { DEFAULT_LOCALE, SUPPORTED_LOCALES } from './types';

const STORAGE_KEY = 'app_locale';

class I18nService {
    private currentLocale: Locale = DEFAULT_LOCALE;
    private listeners: Set<() => void> = new Set();

    constructor() {
        this.loadLocale();
    }

    private loadLocale(): void {
        const stored = localStorage.getItem(STORAGE_KEY) as Locale | null;
        if (stored && SUPPORTED_LOCALES.some((l) => l.code === stored)) {
            this.currentLocale = stored;
        } else {
            const browserLang = navigator.language.split('-')[0] as Locale;
            if (SUPPORTED_LOCALES.some((l) => l.code === browserLang)) {
                this.currentLocale = browserLang;
            }
        }
    }

    getLocale(): Locale {
        return this.currentLocale;
    }

    setLocale(locale: Locale): void {
        if (SUPPORTED_LOCALES.some((l) => l.code === locale)) {
            this.currentLocale = locale;
            localStorage.setItem(STORAGE_KEY, locale);
            this.notifyListeners();
        }
    }

    getTranslations(): TranslationKeys {
        return translations[this.currentLocale] || translations[DEFAULT_LOCALE];
    }

    t<K extends keyof TranslationKeys>(
        section: K,
        key: keyof TranslationKeys[K]
    ): string {
        const t = this.getTranslations();
        const sectionData = t[section];
        if (sectionData && key in sectionData) {
            return sectionData[key] as string;
        }
        return `${String(section)}.${String(key)}`;
    }

    subscribe(listener: () => void): () => void {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }

    private notifyListeners(): void {
        this.listeners.forEach((listener) => listener());
    }

    formatDate(date: Date): string {
        const localeInfo = SUPPORTED_LOCALES.find((l) => l.code === this.currentLocale);
        if (!localeInfo) return date.toLocaleDateString();

        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();

        return localeInfo.dateFormat
            .replace('DD', day)
            .replace('MM', month)
            .replace('YYYY', year.toString());
    }

    formatTime(date: Date): string {
        const localeInfo = SUPPORTED_LOCALES.find((l) => l.code === this.currentLocale);
        if (!localeInfo) return date.toLocaleTimeString();

        const hours24 = date.getHours();
        const hours12 = hours24 % 12 || 12;
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const ampm = hours24 >= 12 ? 'PM' : 'AM';

        if (localeInfo.timeFormat.includes('A')) {
            return `${hours12}:${minutes} ${ampm}`;
        }
        return `${hours24.toString().padStart(2, '0')}:${minutes}`;
    }
}

export const i18n = new I18nService();
