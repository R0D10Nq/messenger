/**
 * Хук для использования переводов в компонентах
 */

import { useState, useEffect, useCallback } from 'react';
import { i18n } from './i18n';
import type { Locale, TranslationKeys } from './types';

export function useTranslation() {
    const [, forceUpdate] = useState({});

    useEffect(() => {
        const unsubscribe = i18n.subscribe(() => forceUpdate({}));
        return unsubscribe;
    }, []);

    const t = useCallback(
        <K extends keyof TranslationKeys>(
            section: K,
            key: keyof TranslationKeys[K]
        ): string => {
            return i18n.t(section, key);
        },
        []
    );

    const setLocale = useCallback((locale: Locale) => {
        i18n.setLocale(locale);
    }, []);

    const getLocale = useCallback((): Locale => {
        return i18n.getLocale();
    }, []);

    const formatDate = useCallback((date: Date): string => {
        return i18n.formatDate(date);
    }, []);

    const formatTime = useCallback((date: Date): string => {
        return i18n.formatTime(date);
    }, []);

    return {
        t,
        setLocale,
        getLocale,
        formatDate,
        formatTime,
        locale: i18n.getLocale(),
    };
}
