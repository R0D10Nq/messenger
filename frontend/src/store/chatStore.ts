/**
 * Zustand store для чатов
 */

import { create } from 'zustand';
import type { Chat, Message, MessageStatus } from '../types/chat';
import { chatService } from '../services/chat';

interface ChatState {
    chats: Chat[];
    currentChat: Chat | null;
    messages: Message[];
    isLoading: boolean;
    isLoadingMessages: boolean;
    hasMoreMessages: boolean;
    error: string | null;
}

interface ChatActions {
    loadChats: () => Promise<void>;
    selectChat: (chatId: string) => Promise<void>;
    loadMessages: (chatId: string, loadMore?: boolean) => Promise<void>;
    sendMessage: (content: string, replyToId?: string) => Promise<void>;
    addMessage: (message: Message) => void;
    updateMessage: (message: Message) => void;
    updateMessageStatus: (messageId: string, status: MessageStatus) => void;
    createDirectChat: (participantId: string) => Promise<Chat>;
    clearError: () => void;
}

export const useChatStore = create<ChatState & ChatActions>((set, get) => ({
    chats: [],
    currentChat: null,
    messages: [],
    isLoading: false,
    isLoadingMessages: false,
    hasMoreMessages: true,
    error: null,

    loadChats: async () => {
        set({ isLoading: true, error: null });
        try {
            const response = await chatService.getChats();
            set({ chats: response.chats, isLoading: false });
        } catch (error) {
            set({
                isLoading: false,
                error: error instanceof Error ? error.message : 'Ошибка загрузки чатов',
            });
        }
    },

    selectChat: async (chatId: string) => {
        const { chats } = get();
        const chat = chats.find((c) => c.id === chatId);

        if (chat) {
            set({ currentChat: chat, messages: [], hasMoreMessages: true });
            await get().loadMessages(chatId);
        }
    },

    loadMessages: async (chatId: string, loadMore = false) => {
        const { messages, isLoadingMessages } = get();

        if (isLoadingMessages) return;

        set({ isLoadingMessages: true });
        try {
            const before = loadMore && messages.length > 0 ? messages[0].id : undefined;
            const response = await chatService.getMessages(chatId, 50, before);

            set({
                messages: loadMore
                    ? [...response.messages.reverse(), ...messages]
                    : response.messages.reverse(),
                hasMoreMessages: response.has_more,
                isLoadingMessages: false,
            });
        } catch (error) {
            set({
                isLoadingMessages: false,
                error: error instanceof Error ? error.message : 'Ошибка загрузки сообщений',
            });
        }
    },

    sendMessage: async (content: string, replyToId?: string) => {
        const { currentChat } = get();
        if (!currentChat) return;

        try {
            const message = await chatService.sendMessage(currentChat.id, {
                content,
                reply_to_id: replyToId,
            });
            get().addMessage(message);
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Ошибка отправки сообщения',
            });
        }
    },

    addMessage: (message: Message) => {
        const { messages, chats, currentChat } = get();

        if (currentChat && message.chat_id === currentChat.id) {
            set({ messages: [...messages, message] });
        }

        set({
            chats: chats.map((chat) =>
                chat.id === message.chat_id
                    ? { ...chat, last_message: message }
                    : chat
            ),
        });
    },

    updateMessage: (message: Message) => {
        const { messages } = get();
        set({
            messages: messages.map((m) => (m.id === message.id ? message : m)),
        });
    },

    updateMessageStatus: (messageId: string, status: MessageStatus) => {
        const { messages } = get();
        set({
            messages: messages.map((m) =>
                m.id === messageId ? { ...m, status } : m
            ),
        });
    },

    createDirectChat: async (participantId: string) => {
        const chat = await chatService.createDirectChat({ user_id: participantId });
        const { chats } = get();
        set({ chats: [chat, ...chats] });
        return chat;
    },

    clearError: () => set({ error: null }),
}));
