/**
 * Экспорт всех локализаций
 */

import { ru } from './ru';
import { en } from './en';
import type { Translations } from '../types';

export const translations: Translations = {
    ru,
    en,
    de: en,
    fr: en,
    es: en,
};
