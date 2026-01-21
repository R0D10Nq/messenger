/**
 * Типы для onboarding
 */

export interface OnboardingStep {
    id: string;
    title: string;
    description: string;
    target?: string;
    placement?: 'top' | 'bottom' | 'left' | 'right';
    action?: string;
}

export interface OnboardingState {
    isActive: boolean;
    currentStep: number;
    completedSteps: string[];
    skipped: boolean;
}

export const ONBOARDING_STEPS: OnboardingStep[] = [
    {
        id: 'welcome',
        title: 'Добро пожаловать!',
        description: 'Это ваш новый мессенджер с E2E шифрованием. Давайте познакомимся с основными функциями.',
    },
    {
        id: 'chats',
        title: 'Список чатов',
        description: 'Здесь отображаются все ваши переписки. Нажмите на чат, чтобы открыть его.',
        target: '[data-onboarding="chat-list"]',
        placement: 'right',
    },
    {
        id: 'new-chat',
        title: 'Новый чат',
        description: 'Нажмите эту кнопку, чтобы начать новый разговор или создать группу.',
        target: '[data-onboarding="new-chat"]',
        placement: 'bottom',
    },
    {
        id: 'profile',
        title: 'Ваш профиль',
        description: 'Настройте свой профиль, аватар и статус.',
        target: '[data-onboarding="profile"]',
        placement: 'bottom',
    },
    {
        id: 'security',
        title: 'Безопасность',
        description: 'Включите двухфакторную аутентификацию для дополнительной защиты аккаунта.',
        target: '[data-onboarding="security"]',
        placement: 'left',
    },
    {
        id: 'complete',
        title: 'Готово!',
        description: 'Вы готовы к общению! Если нужна помощь, загляните в настройки.',
    },
];

export const FEATURE_TIPS = [
    {
        id: 'voice-message',
        title: 'Голосовые сообщения',
        description: 'Удерживайте кнопку микрофона для записи голосового сообщения.',
    },
    {
        id: 'reactions',
        title: 'Реакции',
        description: 'Дважды нажмите на сообщение, чтобы поставить реакцию.',
    },
    {
        id: 'translate',
        title: 'Перевод',
        description: 'Нажмите "Перевести" под сообщением на иностранном языке.',
    },
    {
        id: 'search',
        title: 'Поиск',
        description: 'Используйте поиск для нахождения сообщений и контактов.',
    },
];
