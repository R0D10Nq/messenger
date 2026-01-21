/**
 * Компонент настроек языка
 */

import { useTranslation, SUPPORTED_LOCALES } from '../../i18n';
import type { Locale } from '../../i18n';

interface LanguageSettingsProps {
    onClose?: () => void;
}

export function LanguageSettings({ onClose }: LanguageSettingsProps) {
    const { locale, setLocale, t } = useTranslation();

    const handleSelectLanguage = (newLocale: Locale) => {
        setLocale(newLocale);
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {t('settings', 'language')}
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            )}

            <div className="flex-1 overflow-y-auto p-4">
                <div className="space-y-2">
                    {SUPPORTED_LOCALES.map((localeInfo) => (
                        <button
                            key={localeInfo.code}
                            onClick={() => handleSelectLanguage(localeInfo.code)}
                            className={`w-full flex items-center gap-4 p-4 rounded-xl transition-colors ${locale === localeInfo.code
                                    ? 'bg-blue-50 dark:bg-blue-900/30 border-2 border-blue-500'
                                    : 'bg-gray-50 dark:bg-gray-700/50 border-2 border-transparent hover:bg-gray-100 dark:hover:bg-gray-700'
                                }`}
                        >
                            <span className="text-2xl">{localeInfo.flag}</span>
                            <div className="flex-1 text-left">
                                <div className="font-medium text-gray-900 dark:text-white">
                                    {localeInfo.nativeName}
                                </div>
                                <div className="text-sm text-gray-500 dark:text-gray-400">
                                    {localeInfo.name}
                                </div>
                            </div>
                            {locale === localeInfo.code && (
                                <svg className="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            )}
                        </button>
                    ))}
                </div>

                <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
                    <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                        Форматирование
                    </h3>
                    <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                        <p>
                            <span className="text-gray-500">Дата:</span>{' '}
                            {SUPPORTED_LOCALES.find((l) => l.code === locale)?.dateFormat}
                        </p>
                        <p>
                            <span className="text-gray-500">Время:</span>{' '}
                            {SUPPORTED_LOCALES.find((l) => l.code === locale)?.timeFormat}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
