/**
 * Сервис для работы с каналами
 */

import { api } from './api';
import type {
    ChannelMember,
    ChannelPost,
    ChannelResponse,
    ChannelStats,
    CreateChannelRequest,
    CreatePostRequest,
} from '../types/channel';

export const channelService = {
    async createChannel(request: CreateChannelRequest): Promise<ChannelResponse> {
        return api.post<ChannelResponse>('/channels', request);
    },

    async getChannel(channelId: string): Promise<ChannelResponse> {
        return api.get<ChannelResponse>(`/channels/${channelId}`);
    },

    async updateChannel(channelId: string, updates: Partial<CreateChannelRequest>): Promise<ChannelResponse> {
        return api.put<ChannelResponse>(`/channels/${channelId}`, updates);
    },

    async getChannelStats(channelId: string): Promise<ChannelStats> {
        return api.get<ChannelStats>(`/channels/${channelId}/stats`);
    },

    async createPost(channelId: string, request: CreatePostRequest): Promise<ChannelPost> {
        return api.post<ChannelPost>(`/channels/${channelId}/posts`, request);
    },

    async getMembers(channelId: string): Promise<ChannelMember[]> {
        return api.get<ChannelMember[]>(`/channels/${channelId}/members`);
    },

    async subscribe(channelId: string): Promise<void> {
        return api.post(`/channels/${channelId}/subscribe`, {});
    },

    async unsubscribe(channelId: string): Promise<void> {
        return api.delete(`/channels/${channelId}/subscribe`);
    },
};
