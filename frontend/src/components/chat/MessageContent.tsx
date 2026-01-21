/**
 * Компонент отображения контента сообщения с mentions и ссылками
 */

import { useMemo } from 'react';
import type { MentionData, LinkPreview } from '../../types/mention';

const URL_REGEX = /https?:\/\/[^\s]+/g;
const MENTION_REGEX = /@(\w+)/g;

interface MessageContentProps {
    content: string;
    mentions?: MentionData[];
    linkPreviews?: LinkPreview[];
    onMentionClick?: (userId: string) => void;
}

interface TextPart {
    type: 'text' | 'mention' | 'link';
    value: string;
    userId?: string;
    url?: string;
}

function parseContent(content: string, mentions: MentionData[]): TextPart[] {
    const parts: TextPart[] = [];
    let lastIndex = 0;

    const mentionMap = new Map(mentions.map(m => [m.offset, m]));

    const regex = new RegExp(`(${URL_REGEX.source})|(${MENTION_REGEX.source})`, 'g');
    let match;

    while ((match = regex.exec(content)) !== null) {
        if (match.index > lastIndex) {
            parts.push({ type: 'text', value: content.slice(lastIndex, match.index) });
        }

        if (match[1]) {
            parts.push({ type: 'link', value: match[1], url: match[1] });
        } else if (match[2]) {
            const mention = mentionMap.get(match.index);
            if (mention) {
                parts.push({ type: 'mention', value: match[2], userId: mention.user_id });
            } else {
                parts.push({ type: 'text', value: match[2] });
            }
        }

        lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
        parts.push({ type: 'text', value: content.slice(lastIndex) });
    }

    return parts;
}

export function MessageContent({ content, mentions = [], linkPreviews = [], onMentionClick }: MessageContentProps) {
    const parts = useMemo(() => parseContent(content, mentions), [content, mentions]);

    return (
        <div>
            <p className="whitespace-pre-wrap break-words">
                {parts.map((part, i) => {
                    if (part.type === 'mention') {
                        return (
                            <button
                                key={i}
                                onClick={() => part.userId && onMentionClick?.(part.userId)}
                                className="text-blue-600 hover:underline font-medium"
                            >
                                {part.value}
                            </button>
                        );
                    }

                    if (part.type === 'link') {
                        return (
                            <a
                                key={i}
                                href={part.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:underline"
                            >
                                {part.value}
                            </a>
                        );
                    }

                    return <span key={i}>{part.value}</span>;
                })}
            </p>

            {linkPreviews.length > 0 && (
                <div className="mt-2 space-y-2">
                    {linkPreviews.map((preview, i) => (
                        <a
                            key={i}
                            href={preview.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                        >
                            {preview.image_url && (
                                <img
                                    src={preview.image_url}
                                    alt=""
                                    className="w-full h-32 object-cover rounded mb-2"
                                />
                            )}
                            {preview.site_name && (
                                <p className="text-xs text-gray-500 uppercase">{preview.site_name}</p>
                            )}
                            {preview.title && (
                                <p className="font-medium text-gray-900 line-clamp-2">{preview.title}</p>
                            )}
                            {preview.description && (
                                <p className="text-sm text-gray-600 line-clamp-2">{preview.description}</p>
                            )}
                        </a>
                    ))}
                </div>
            )}
        </div>
    );
}
