/**
 * Компонент реакций на сообщение
 */

import { useState, useCallback } from 'react';
import { reactionService } from '../../services/reaction';
import type { ReactionSummary } from '../../types/reaction';

const EMOJI_LIST = ['👍', '❤️', '😂', '😮', '😢', '🎉'];

interface MessageReactionsProps {
    messageId: string;
    reactions: ReactionSummary[];
    onReactionChange?: () => void;
}

export function MessageReactions({ messageId, reactions, onReactionChange }: MessageReactionsProps) {
    const [showPicker, setShowPicker] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const handleAddReaction = useCallback(async (emoji: string) => {
        setIsLoading(true);
        try {
            await reactionService.addReaction(messageId, { emoji });
            onReactionChange?.();
        } catch (error) {
            console.error('Ошибка добавления реакции:', error);
        } finally {
            setIsLoading(false);
            setShowPicker(false);
        }
    }, [messageId, onReactionChange]);

    const handleRemoveReaction = useCallback(async (emoji: string) => {
        setIsLoading(true);
        try {
            await reactionService.removeReaction(messageId, emoji);
            onReactionChange?.();
        } catch (error) {
            console.error('Ошибка удаления реакции:', error);
        } finally {
            setIsLoading(false);
        }
    }, [messageId, onReactionChange]);

    const handleReactionClick = useCallback((reaction: ReactionSummary) => {
        if (reaction.reacted_by_me) {
            handleRemoveReaction(reaction.emoji);
        } else {
            handleAddReaction(reaction.emoji);
        }
    }, [handleAddReaction, handleRemoveReaction]);

    return (
        <div className="flex items-center gap-1 mt-1 flex-wrap">
            {reactions.map((reaction) => (
                <button
                    key={reaction.emoji}
                    onClick={() => handleReactionClick(reaction)}
                    disabled={isLoading}
                    className={`
            inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs
            transition-colors cursor-pointer
            ${reaction.reacted_by_me
                            ? 'bg-blue-100 text-blue-700 border border-blue-300'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }
          `}
                    title={reaction.users.join(', ')}
                >
                    <span>{reaction.emoji}</span>
                    <span>{reaction.count}</span>
                </button>
            ))}

            <div className="relative">
                <button
                    onClick={() => setShowPicker(!showPicker)}
                    className="w-6 h-6 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-500 text-sm"
                    title="Добавить реакцию"
                >
                    +
                </button>

                {showPicker && (
                    <div className="absolute bottom-full left-0 mb-1 bg-white rounded-lg shadow-lg border p-2 flex gap-1 z-10">
                        {EMOJI_LIST.map((emoji) => (
                            <button
                                key={emoji}
                                onClick={() => handleAddReaction(emoji)}
                                disabled={isLoading}
                                className="w-8 h-8 hover:bg-gray-100 rounded flex items-center justify-center text-lg"
                            >
                                {emoji}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
