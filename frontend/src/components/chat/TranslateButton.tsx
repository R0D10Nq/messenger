/**
 * Кнопка перевода сообщения
 */

import { useState } from 'react';
import { translateService } from '../../services/translate';
import { COMMON_LANGUAGES } from '../../types/translate';

interface TranslateButtonProps {
    messageId: string;
    originalText: string;
    onTranslate?: (translatedText: string) => void;
}

export function TranslateButton({ messageId, originalText: _originalText, onTranslate }: TranslateButtonProps) {
    const [showMenu, setShowMenu] = useState(false);
    const [loading, setLoading] = useState(false);
    const [translation, setTranslation] = useState<string | null>(null);
    const [sourceLang, setSourceLang] = useState<string | null>(null);

    const handleTranslate = async (targetLang: string) => {
        try {
            setLoading(true);
            setShowMenu(false);

            const result = await translateService.translateMessage(messageId, targetLang);
            setTranslation(result.translated_text);
            setSourceLang(result.source_language);

            if (onTranslate) {
                onTranslate(result.translated_text);
            }
        } catch (err) {
            console.error('Ошибка перевода:', err);
        } finally {
            setLoading(false);
        }
    };

    const clearTranslation = () => {
        setTranslation(null);
        setSourceLang(null);
    };

    if (translation) {
        return (
            <div className="mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-sm">
                <div className="flex items-center justify-between mb-1">
                    <span className="text-xs text-blue-600 dark:text-blue-400 font-medium">
                        Перевод с {sourceLang?.toUpperCase()}
                    </span>
                    <button
                        onClick={clearTranslation}
                        className="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                    >
                        Скрыть
                    </button>
                </div>
                <p className="text-gray-800 dark:text-gray-200">{translation}</p>
            </div>
        );
    }

    return (
        <div className="relative inline-block">
            <button
                onClick={() => setShowMenu(!showMenu)}
                disabled={loading}
                className="text-xs text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 transition-colors flex items-center gap-1"
                title="Перевести"
            >
                {loading ? (
                    <span className="animate-pulse">Перевод...</span>
                ) : (
                    <>
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
                        </svg>
                        <span>Перевести</span>
                    </>
                )}
            </button>

            {showMenu && (
                <div className="absolute bottom-full left-0 mb-1 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 min-w-[140px] z-10">
                    <div className="px-2 py-1 text-xs text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">
                        Перевести на:
                    </div>
                    {COMMON_LANGUAGES.map((lang) => (
                        <button
                            key={lang.code}
                            onClick={() => handleTranslate(lang.code)}
                            className="w-full px-3 py-1.5 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                        >
                            {lang.name}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
