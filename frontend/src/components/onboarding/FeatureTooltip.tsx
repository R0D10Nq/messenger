/**
 * Компонент подсказки для функций
 */

import { useState } from 'react';

interface FeatureTooltipProps {
    id: string;
    title: string;
    description: string;
    children: React.ReactNode;
    show?: boolean;
    onDismiss?: () => void;
}

export function FeatureTooltip({
    id,
    title,
    description,
    children,
    show = false,
    onDismiss,
}: FeatureTooltipProps) {
    const [isVisible, setIsVisible] = useState(show);

    const handleDismiss = () => {
        setIsVisible(false);
        localStorage.setItem(`tooltip_${id}_dismissed`, 'true');
        onDismiss?.();
    };

    if (!isVisible) {
        return <>{children}</>;
    }

    return (
        <div className="relative inline-block">
            {children}
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 z-50">
                <div className="bg-gray-900 dark:bg-gray-700 text-white rounded-lg shadow-lg p-3">
                    <div className="flex items-start justify-between gap-2">
                        <div>
                            <h4 className="font-medium text-sm">{title}</h4>
                            <p className="text-xs text-gray-300 mt-1">{description}</p>
                        </div>
                        <button
                            onClick={handleDismiss}
                            className="text-gray-400 hover:text-white flex-shrink-0"
                        >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <button
                        onClick={handleDismiss}
                        className="mt-2 text-xs text-blue-400 hover:text-blue-300"
                    >
                        Понятно
                    </button>
                </div>
                <div className="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-gray-900 dark:border-t-gray-700" />
            </div>
        </div>
    );
}

export function useFeatureTooltip(id: string): boolean {
    const dismissed = localStorage.getItem(`tooltip_${id}_dismissed`);
    return !dismissed;
}
