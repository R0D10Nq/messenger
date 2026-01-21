/**
 * Компонент защищённого контента
 */

import { useState, useEffect, useRef } from 'react';
import { contentProtectionService } from '../../services/contentProtection';

interface ProtectedContentProps {
    children: React.ReactNode;
    userId?: string;
    viewOnce?: boolean;
    onViewed?: () => void;
    expiresInSeconds?: number;
}

export function ProtectedContent({
    children,
    userId,
    viewOnce = false,
    onViewed,
    expiresInSeconds,
}: ProtectedContentProps) {
    const [isViewed, setIsViewed] = useState(false);
    const [isExpired, setIsExpired] = useState(false);
    const [timeLeft, setTimeLeft] = useState(expiresInSeconds || 0);
    const containerRef = useRef<HTMLDivElement>(null);

    const settings = contentProtectionService.getSettings();
    const watermark = userId ? contentProtectionService.getWatermarkText(userId) : '';

    useEffect(() => {
        if (viewOnce && !isViewed) {
            setIsViewed(true);
            onViewed?.();
        }
    }, [viewOnce, isViewed, onViewed]);

    useEffect(() => {
        if (expiresInSeconds && expiresInSeconds > 0) {
            const interval = setInterval(() => {
                setTimeLeft((prev) => {
                    if (prev <= 1) {
                        setIsExpired(true);
                        clearInterval(interval);
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);

            return () => clearInterval(interval);
        }
    }, [expiresInSeconds]);

    if (isExpired) {
        return (
            <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-center">
                <div className="text-gray-500 dark:text-gray-400">
                    <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <p className="text-sm">Контент удалён</p>
                </div>
            </div>
        );
    }

    return (
        <div
            ref={containerRef}
            data-protected="true"
            className="relative select-none"
            style={{
                WebkitUserSelect: settings.preventCopy ? 'none' : 'auto',
                userSelect: settings.preventCopy ? 'none' : 'auto',
            }}
        >
            {children}

            {settings.watermarkEnabled && watermark && (
                <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-10">
                    <span className="text-2xl font-bold text-gray-500 transform -rotate-45">
                        {watermark}
                    </span>
                </div>
            )}

            {expiresInSeconds && timeLeft > 0 && (
                <div className="absolute top-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded">
                    {timeLeft}с
                </div>
            )}

            {viewOnce && (
                <div className="absolute bottom-2 left-2 flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    <span>Одноразовый просмотр</span>
                </div>
            )}

            {settings.preventScreenshot && (
                <div className="absolute top-2 left-2 flex items-center gap-1 text-xs text-red-500">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                    <span>Защищено</span>
                </div>
            )}
        </div>
    );
}

export function ViewOnceImage({ src, alt }: { src: string; alt?: string }) {
    const [revealed, setRevealed] = useState(false);
    const [viewed, setViewed] = useState(false);

    const handleReveal = () => {
        if (!viewed) {
            setRevealed(true);
            setViewed(true);
        }
    };

    if (viewed && !revealed) {
        return (
            <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-center">
                <p className="text-sm text-gray-500 dark:text-gray-400">Изображение просмотрено</p>
            </div>
        );
    }

    if (!revealed) {
        return (
            <button
                onClick={handleReveal}
                className="w-full p-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg text-white text-center"
            >
                <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <p className="font-medium">Нажмите для просмотра</p>
                <p className="text-xs opacity-75">Одноразовое изображение</p>
            </button>
        );
    }

    return (
        <ProtectedContent viewOnce onViewed={() => setRevealed(false)}>
            <img
                src={src}
                alt={alt}
                className="max-w-full rounded-lg"
                onContextMenu={(e) => e.preventDefault()}
                draggable={false}
            />
        </ProtectedContent>
    );
}
