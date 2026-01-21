/**
 * Сервис для управления onboarding
 */

const ONBOARDING_KEY = 'onboarding_completed';
const ONBOARDING_SKIPPED_KEY = 'onboarding_skipped';

export const onboardingService = {
    isCompleted(): boolean {
        return localStorage.getItem(ONBOARDING_KEY) === 'true';
    },

    isSkipped(): boolean {
        return localStorage.getItem(ONBOARDING_SKIPPED_KEY) === 'true';
    },

    shouldShow(): boolean {
        return !this.isCompleted() && !this.isSkipped();
    },

    complete(): void {
        localStorage.setItem(ONBOARDING_KEY, 'true');
    },

    skip(): void {
        localStorage.setItem(ONBOARDING_SKIPPED_KEY, 'true');
    },

    reset(): void {
        localStorage.removeItem(ONBOARDING_KEY);
        localStorage.removeItem(ONBOARDING_SKIPPED_KEY);
        this.resetTooltips();
    },

    resetTooltips(): void {
        const keys = Object.keys(localStorage);
        keys.forEach((key) => {
            if (key.startsWith('tooltip_') && key.endsWith('_dismissed')) {
                localStorage.removeItem(key);
            }
        });
    },

    isTooltipDismissed(tooltipId: string): boolean {
        return localStorage.getItem(`tooltip_${tooltipId}_dismissed`) === 'true';
    },

    dismissTooltip(tooltipId: string): void {
        localStorage.setItem(`tooltip_${tooltipId}_dismissed`, 'true');
    },
};
