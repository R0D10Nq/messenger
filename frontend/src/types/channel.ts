/**
 * Типы для каналов
 */

export type ChannelType = 'public' | 'private';
export type ChannelRole = 'owner' | 'admin' | 'moderator' | 'subscriber';

export interface CreateChannelRequest {
    name: string;
    username: string;
    description?: string;
    channel_type?: ChannelType;
    allow_comments?: boolean;
}

export interface ChannelResponse {
    id: string;
    name: string;
    username: string;
    description: string | null;
    channel_type: ChannelType;
    owner_id: string;
    subscriber_count: number;
    allow_comments: boolean;
    created_at: string;
}

export interface ChannelStats {
    subscriber_count: number;
    total_posts: number;
    total_views: number;
    avg_views_per_post: number;
    growth_rate: number;
    top_posts: ChannelPost[];
}

export interface ChannelPost {
    id: string;
    channel_id: string;
    content: string;
    author_id: string;
    views: number;
    is_pinned: boolean;
    created_at: string;
}

export interface ChannelMember {
    user_id: string;
    username: string;
    role: ChannelRole;
    joined_at: string;
}

export interface CreatePostRequest {
    content: string;
    silent?: boolean;
    schedule_at?: string;
    pin?: boolean;
}
