/**
 * Типы для системы локализации
 */

export type Locale = 'ru' | 'en' | 'de' | 'fr' | 'es';

export interface LocaleInfo {
    code: Locale;
    name: string;
    nativeName: string;
    flag: string;
    dateFormat: string;
    timeFormat: string;
}

export const SUPPORTED_LOCALES: LocaleInfo[] = [
    { code: 'ru', name: 'Russian', nativeName: 'Русский', flag: '🇷🇺', dateFormat: 'DD.MM.YYYY', timeFormat: 'HH:mm' },
    { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', dateFormat: 'MM/DD/YYYY', timeFormat: 'h:mm A' },
    { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪', dateFormat: 'DD.MM.YYYY', timeFormat: 'HH:mm' },
    { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷', dateFormat: 'DD/MM/YYYY', timeFormat: 'HH:mm' },
    { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸', dateFormat: 'DD/MM/YYYY', timeFormat: 'HH:mm' },
];

export const DEFAULT_LOCALE: Locale = 'ru';

export interface TranslationKeys {
    common: {
        loading: string;
        error: string;
        save: string;
        cancel: string;
        delete: string;
        edit: string;
        close: string;
        search: string;
        settings: string;
        profile: string;
        logout: string;
        back: string;
        next: string;
        done: string;
        yes: string;
        no: string;
    };
    auth: {
        login: string;
        register: string;
        email: string;
        password: string;
        confirmPassword: string;
        forgotPassword: string;
        loginButton: string;
        registerButton: string;
        noAccount: string;
        hasAccount: string;
    };
    chat: {
        newChat: string;
        newGroup: string;
        typeMessage: string;
        send: string;
        reply: string;
        forward: string;
        copy: string;
        pinMessage: string;
        deleteMessage: string;
        editMessage: string;
        translate: string;
        voiceMessage: string;
        attachFile: string;
        noMessages: string;
        typing: string;
    };
    settings: {
        general: string;
        notifications: string;
        privacy: string;
        security: string;
        appearance: string;
        language: string;
        dataSaver: string;
        about: string;
        theme: string;
        darkMode: string;
        lightMode: string;
        systemMode: string;
    };
    notifications: {
        newMessage: string;
        missedCall: string;
        groupInvite: string;
    };
    errors: {
        networkError: string;
        serverError: string;
        unauthorized: string;
        notFound: string;
        validationError: string;
    };
}

export type Translations = Record<Locale, TranslationKeys>;
