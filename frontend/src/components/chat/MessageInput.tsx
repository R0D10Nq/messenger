/**
 * Поле ввода сообщения
 */

import { useState, useRef, useEffect, useCallback } from 'react';
import { useChatStore } from '../../store/chatStore';
import { wsService } from '../../services/websocket';
import { AttachmentButton } from './AttachmentButton';
import { VoiceRecorder } from './VoiceRecorder';
import { SmartReplies } from './SmartReplies';
import { StickerPicker } from './StickerPicker';

export function MessageInput() {
    const [content, setContent] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [showStickers, setShowStickers] = useState(false);
    const [showSmartReplies, setShowSmartReplies] = useState(true);
    const { currentChat, messages, sendMessage } = useChatStore();
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const lastMessage = messages.length > 0 ? messages[messages.length - 1] : null;

    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
        }
    }, [content]);

    const handleTyping = useCallback(() => {
        if (!currentChat) return;

        if (!isTyping) {
            setIsTyping(true);
            wsService.startTyping(currentChat.id);
        }

        if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
        }

        typingTimeoutRef.current = setTimeout(() => {
            setIsTyping(false);
            if (currentChat) {
                wsService.stopTyping(currentChat.id);
            }
        }, 2000);
    }, [currentChat, isTyping]);

    useEffect(() => {
        return () => {
            if (typingTimeoutRef.current) {
                clearTimeout(typingTimeoutRef.current);
            }
            if (currentChat && isTyping) {
                wsService.stopTyping(currentChat.id);
            }
        };
    }, [currentChat, isTyping]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const trimmed = content.trim();
        if (!trimmed || !currentChat) return;

        if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
        }
        if (isTyping) {
            setIsTyping(false);
            wsService.stopTyping(currentChat.id);
        }

        setContent('');
        await sendMessage(trimmed);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    if (!currentChat) return null;

    const handleAttachment = (url: string, mediaType: string) => {
        sendMessage(`[${mediaType}] ${url}`);
    };

    const handleVoice = (url: string) => {
        sendMessage(`[voice] ${url}`);
    };

    const handleSmartReply = (reply: string) => {
        setContent(reply);
        textareaRef.current?.focus();
    };

    const handleStickerSelect = (stickerUrl: string) => {
        sendMessage(`[sticker] ${stickerUrl}`);
        setShowStickers(false);
    };

    return (
        <div className="border-t bg-white">
            {showSmartReplies && lastMessage && lastMessage.sender_id !== currentChat?.id && (
                <SmartReplies
                    messageText={lastMessage.content}
                    messageId={lastMessage.id}
                    onSelect={handleSmartReply}
                    onHide={() => setShowSmartReplies(false)}
                />
            )}
            <form onSubmit={handleSubmit} className="p-4">
                <div className="flex items-end gap-2">
                    <AttachmentButton onUpload={handleAttachment} />
                    <button
                        type="button"
                        onClick={() => setShowStickers(!showStickers)}
                        className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full transition-colors"
                        title="Стикеры"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </button>
                    <textarea
                        ref={textareaRef}
                        value={content}
                        onChange={(e) => {
                            setContent(e.target.value);
                            handleTyping();
                        }}
                        onKeyDown={handleKeyDown}
                        placeholder="Напишите сообщение..."
                        rows={1}
                        className="flex-1 resize-none rounded-2xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    {content.trim() ? (
                        <button
                            type="submit"
                            className="bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600 transition-colors"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="currentColor"
                                className="w-6 h-6"
                            >
                                <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
                            </svg>
                        </button>
                    ) : (
                        <VoiceRecorder onRecorded={handleVoice} />
                    )}
                </div>
            </form>
            {showStickers && (
                <StickerPicker
                    onSelect={handleStickerSelect}
                    onClose={() => setShowStickers(false)}
                />
            )}
        </div>
    );
}
