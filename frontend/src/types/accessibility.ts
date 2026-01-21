/**
 * Типы для настроек доступности
 */

export interface AccessibilitySettings {
    highContrast: boolean;
    largeText: boolean;
    reduceMotion: boolean;
    screenReaderOptimized: boolean;
    focusIndicators: boolean;
    keyboardNavigation: boolean;
    fontSize: FontSize;
    colorBlindMode: ColorBlindMode;
}

export type FontSize = 'small' | 'medium' | 'large' | 'extra-large';
export type ColorBlindMode = 'none' | 'protanopia' | 'deuteranopia' | 'tritanopia';

export const FONT_SIZE_VALUES: Record<FontSize, number> = {
    small: 14,
    medium: 16,
    large: 18,
    'extra-large': 20,
};

export const FONT_SIZE_LABELS: Record<FontSize, string> = {
    small: 'Мелкий (14px)',
    medium: 'Обычный (16px)',
    large: 'Крупный (18px)',
    'extra-large': 'Очень крупный (20px)',
};

export const COLOR_BLIND_LABELS: Record<ColorBlindMode, string> = {
    none: 'Без коррекции',
    protanopia: 'Протанопия (красный)',
    deuteranopia: 'Дейтеранопия (зелёный)',
    tritanopia: 'Тританопия (синий)',
};

export const DEFAULT_ACCESSIBILITY_SETTINGS: AccessibilitySettings = {
    highContrast: false,
    largeText: false,
    reduceMotion: false,
    screenReaderOptimized: false,
    focusIndicators: true,
    keyboardNavigation: true,
    fontSize: 'medium',
    colorBlindMode: 'none',
};
