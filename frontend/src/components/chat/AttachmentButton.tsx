/**
 * Кнопка прикрепления файла
 */

import { useRef, useState } from 'react';
import { mediaService } from '../../services/media';

interface AttachmentButtonProps {
    onUpload: (url: string, mediaType: string) => void;
}

export function AttachmentButton({ onUpload }: AttachmentButtonProps) {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [isUploading, setIsUploading] = useState(false);

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setIsUploading(true);
        try {
            const result = await mediaService.upload(file);
            onUpload(result.url, result.media_type);
        } catch (error) {
            console.error('Ошибка загрузки:', error);
        } finally {
            setIsUploading(false);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    return (
        <>
            <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
                className="hidden"
                accept="image/*,video/*,audio/*,.pdf,.doc,.docx,.txt"
            />
            <button
                type="button"
                onClick={handleClick}
                disabled={isUploading}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors disabled:opacity-50"
                title="Прикрепить файл"
            >
                {isUploading ? (
                    <div className="w-6 h-6 animate-spin rounded-full border-2 border-gray-300 border-t-blue-500" />
                ) : (
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="w-6 h-6 text-gray-500"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13"
                        />
                    </svg>
                )}
            </button>
        </>
    );
}
