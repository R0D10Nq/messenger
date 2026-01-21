/**
 * Сервис чатов
 */

import { api } from './api';
import type {
    Chat,
    ChatListResponse,
    CreateDirectChatRequest,
    CreateGroupChatRequest,
    Message,
    MessageListResponse,
    SendMessageRequest,
} from '../types/chat';

export const chatService = {
    async getChats(limit = 50, offset = 0): Promise<ChatListResponse> {
        return api.get<ChatListResponse>(`/chats?limit=${limit}&offset=${offset}`);
    },

    async getChat(chatId: string): Promise<Chat> {
        return api.get<Chat>(`/chats/${chatId}`);
    },

    async createDirectChat(data: CreateDirectChatRequest): Promise<Chat> {
        return api.post<Chat>('/chats/direct', data);
    },

    async createGroupChat(data: CreateGroupChatRequest): Promise<Chat> {
        return api.post<Chat>('/chats/group', data);
    },

    async getMessages(
        chatId: string,
        limit = 50,
        before?: string
    ): Promise<MessageListResponse> {
        let url = `/chats/${chatId}/messages?limit=${limit}`;
        if (before) {
            url += `&before=${before}`;
        }
        return api.get<MessageListResponse>(url);
    },

    async sendMessage(chatId: string, data: SendMessageRequest): Promise<Message> {
        return api.post<Message>(`/chats/${chatId}/messages`, data);
    },

    async editMessage(
        chatId: string,
        messageId: string,
        content: string
    ): Promise<Message> {
        return api.put<Message>(`/chats/${chatId}/messages/${messageId}`, { content });
    },

    async deleteMessage(chatId: string, messageId: string): Promise<void> {
        return api.delete(`/chats/${chatId}/messages/${messageId}`);
    },

    async markAsRead(chatId: string, messageId: string): Promise<void> {
        return api.post(`/chats/${chatId}/messages/${messageId}/read`);
    },
};
