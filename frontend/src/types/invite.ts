/**
 * Типы для приглашений
 */

export type InviteType = 'chat' | 'group' | 'channel';
export type InviteVisibility = 'none' | 'basic' | 'messages';

export interface CreateInviteRequest {
    chat_id: string;
    expires_in_hours?: number;
    max_uses?: number;
    preview_visibility?: InviteVisibility;
    preview_message_count?: number;
}

export interface InviteResponse {
    id: string;
    code: string;
    chat_id: string;
    invite_type: InviteType;
    created_by: string;
    expires_at: string | null;
    max_uses: number | null;
    use_count: number;
    preview_visibility: InviteVisibility;
    is_active: boolean;
    created_at: string;
}

export interface InvitePreviewResponse {
    code: string;
    chat_name: string;
    chat_type: InviteType;
    member_count: number;
    avatar_url: string | null;
    description: string | null;
    preview_messages: Array<{ content: string; sender: string }> | null;
    is_expired: boolean;
    requires_approval: boolean;
}

export interface InviteJoinResponse {
    success: boolean;
    chat_id: string;
    message: string;
}

export interface InviteListResponse {
    invites: InviteResponse[];
    total: number;
}
