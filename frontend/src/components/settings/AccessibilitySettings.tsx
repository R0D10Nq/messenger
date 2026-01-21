/**
 * Компонент настроек доступности
 */

import { useState, useEffect } from 'react';
import { accessibilityService } from '../../services/accessibility';
import type { AccessibilitySettings as AccessibilitySettingsType, FontSize, ColorBlindMode } from '../../types/accessibility';
import { FONT_SIZE_LABELS, COLOR_BLIND_LABELS } from '../../types/accessibility';

interface AccessibilitySettingsProps {
    onClose?: () => void;
}

export function AccessibilitySettings({ onClose }: AccessibilitySettingsProps) {
    const [settings, setSettings] = useState<AccessibilitySettingsType>(accessibilityService.getSettings());

    useEffect(() => {
        const unsubscribe = accessibilityService.subscribe(() => {
            setSettings(accessibilityService.getSettings());
        });
        return unsubscribe;
    }, []);

    const handleToggle = (key: keyof AccessibilitySettingsType) => {
        const current = settings[key];
        if (typeof current === 'boolean') {
            accessibilityService.updateSettings({ [key]: !current });
        }
    };

    const handleFontSizeChange = (fontSize: FontSize) => {
        accessibilityService.updateSettings({ fontSize });
    };

    const handleColorBlindChange = (colorBlindMode: ColorBlindMode) => {
        accessibilityService.updateSettings({ colorBlindMode });
    };

    const handleReset = () => {
        accessibilityService.resetSettings();
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Доступность
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                        aria-label="Закрыть"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            )}

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Внешний вид
                    </h3>
                    <div className="space-y-3">
                        <ToggleOption
                            label="Высокий контраст"
                            description="Увеличивает контрастность для лучшей читаемости"
                            checked={settings.highContrast}
                            onChange={() => handleToggle('highContrast')}
                        />
                        <ToggleOption
                            label="Крупный текст"
                            description="Увеличивает размер текста во всём приложении"
                            checked={settings.largeText}
                            onChange={() => handleToggle('largeText')}
                        />
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Размер шрифта
                    </h3>
                    <div className="space-y-2">
                        {(Object.keys(FONT_SIZE_LABELS) as FontSize[]).map((size) => (
                            <label
                                key={size}
                                className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors ${settings.fontSize === size
                                        ? 'bg-blue-50 dark:bg-blue-900/30 border-2 border-blue-500'
                                        : 'bg-gray-50 dark:bg-gray-700/50 border-2 border-transparent'
                                    }`}
                            >
                                <input
                                    type="radio"
                                    name="fontSize"
                                    value={size}
                                    checked={settings.fontSize === size}
                                    onChange={() => handleFontSizeChange(size)}
                                    className="sr-only"
                                />
                                <span className="text-gray-900 dark:text-white">{FONT_SIZE_LABELS[size]}</span>
                            </label>
                        ))}
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Движение и анимации
                    </h3>
                    <ToggleOption
                        label="Уменьшить движение"
                        description="Отключает анимации и переходы"
                        checked={settings.reduceMotion}
                        onChange={() => handleToggle('reduceMotion')}
                    />
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Навигация
                    </h3>
                    <div className="space-y-3">
                        <ToggleOption
                            label="Индикаторы фокуса"
                            description="Показывает чёткие рамки при навигации клавиатурой"
                            checked={settings.focusIndicators}
                            onChange={() => handleToggle('focusIndicators')}
                        />
                        <ToggleOption
                            label="Оптимизация для экранных читалок"
                            description="Улучшает совместимость с VoiceOver, NVDA, JAWS"
                            checked={settings.screenReaderOptimized}
                            onChange={() => handleToggle('screenReaderOptimized')}
                        />
                    </div>
                </section>

                <section>
                    <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Коррекция цвета
                    </h3>
                    <select
                        value={settings.colorBlindMode}
                        onChange={(e) => handleColorBlindChange(e.target.value as ColorBlindMode)}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                        aria-label="Режим цветокоррекции"
                    >
                        {(Object.keys(COLOR_BLIND_LABELS) as ColorBlindMode[]).map((mode) => (
                            <option key={mode} value={mode}>{COLOR_BLIND_LABELS[mode]}</option>
                        ))}
                    </select>
                </section>

                <button
                    onClick={handleReset}
                    className="w-full py-2 px-4 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                >
                    Сбросить настройки
                </button>
            </div>
        </div>
    );
}

interface ToggleOptionProps {
    label: string;
    description: string;
    checked: boolean;
    onChange: () => void;
}

function ToggleOption({ label, description, checked, onChange }: ToggleOptionProps) {
    return (
        <label className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg cursor-pointer">
            <div>
                <span className="text-gray-900 dark:text-white font-medium">{label}</span>
                <p className="text-xs text-gray-500 dark:text-gray-400">{description}</p>
            </div>
            <button
                role="switch"
                aria-checked={checked}
                onClick={onChange}
                className={`relative w-12 h-6 rounded-full transition-colors ${checked ? 'bg-blue-500' : 'bg-gray-300 dark:bg-gray-600'
                    }`}
            >
                <span
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${checked ? 'left-7' : 'left-1'
                        }`}
                />
            </button>
        </label>
    );
}
