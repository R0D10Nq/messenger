/**
 * Мастер onboarding для новых пользователей
 */

import { useState } from 'react';
import { ONBOARDING_STEPS } from '../../types/onboarding';

interface OnboardingWizardProps {
    onComplete: () => void;
    onSkip: () => void;
}

export function OnboardingWizard({ onComplete, onSkip }: OnboardingWizardProps) {
    const [currentStep, setCurrentStep] = useState(0);
    const step = ONBOARDING_STEPS[currentStep];

    const handleNext = () => {
        if (currentStep < ONBOARDING_STEPS.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            onComplete();
        }
    };

    const handlePrev = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const isFirstStep = currentStep === 0;
    const isLastStep = currentStep === ONBOARDING_STEPS.length - 1;

    return (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex gap-1">
                            {ONBOARDING_STEPS.map((_, index) => (
                                <div
                                    key={index}
                                    className={`w-2 h-2 rounded-full transition-colors ${index === currentStep
                                        ? 'bg-blue-500'
                                        : index < currentStep
                                            ? 'bg-blue-300'
                                            : 'bg-gray-300 dark:bg-gray-600'
                                        }`}
                                />
                            ))}
                        </div>
                        <button
                            onClick={onSkip}
                            className="text-sm text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
                        >
                            Пропустить
                        </button>
                    </div>

                    <div className="text-center py-8">
                        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                            {isFirstStep && (
                                <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                                </svg>
                            )}
                            {isLastStep && (
                                <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                            )}
                            {!isFirstStep && !isLastStep && (
                                <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            )}
                        </div>

                        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                            {step.title}
                        </h2>
                        <p className="text-gray-600 dark:text-gray-400">
                            {step.description}
                        </p>
                    </div>
                </div>

                <div className="flex gap-3 p-4 bg-gray-50 dark:bg-gray-900/50 border-t border-gray-200 dark:border-gray-700">
                    <button
                        onClick={handlePrev}
                        disabled={isFirstStep}
                        className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${isFirstStep
                            ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                            }`}
                    >
                        Назад
                    </button>
                    <button
                        onClick={handleNext}
                        className="flex-1 py-2 px-4 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors"
                    >
                        {isLastStep ? 'Начать' : 'Далее'}
                    </button>
                </div>
            </div>
        </div>
    );
}
