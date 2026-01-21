/**
 * Типы для закреплённых сообщений
 */

export interface PinnedMessage {
    id: string;
    chat_id: string;
    message_id: string;
    message_content: string;
    pinned_by_id: string;
    pinned_by_name: string;
    pinned_at: string;
}

export interface PinnedMessagesList {
    chat_id: string;
    pinned_messages: PinnedMessage[];
    count: number;
}
