/**
 * Типы для чатов и сообщений
 */

export type ChatType = 'direct' | 'group';
export type MessageStatus = 'sent' | 'delivered' | 'read';
export type MemberRole = 'owner' | 'admin' | 'member';

export interface ChatMember {
    user_id: string;
    name: string;
    avatar_url: string | null;
    role: MemberRole;
    joined_at: string;
}

export interface ReactionSummary {
    emoji: string;
    count: number;
    users: string[];
    reacted_by_me: boolean;
}

export interface Message {
    id: string;
    chat_id: string;
    sender_id: string;
    sender_name: string;
    sender_avatar: string | null;
    content: string;
    status: MessageStatus;
    reply_to_id: string | null;
    reactions: ReactionSummary[];
    created_at: string;
    updated_at: string | null;
    is_edited: boolean;
}

export interface Chat {
    id: string;
    chat_type: ChatType;
    name: string;
    description: string | null;
    avatar_url: string | null;
    members: ChatMember[];
    last_message: Message | null;
    unread_count: number;
    created_at: string;
}

export interface ChatListResponse {
    chats: Chat[];
    total: number;
}

export interface MessageListResponse {
    messages: Message[];
    total: number;
    has_more: boolean;
}

export interface SendMessageRequest {
    content: string;
    reply_to_id?: string;
}

export interface CreateDirectChatRequest {
    user_id: string;
}

export interface CreateGroupChatRequest {
    name: string;
    description?: string;
    member_ids: string[];
}
