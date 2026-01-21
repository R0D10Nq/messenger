/**
 * WebSocket сервис для real-time коммуникации
 */

import { io, Socket } from 'socket.io-client';

const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:8000';

type MessageHandler = (data: unknown) => void;

interface WebSocketEvents {
    connect: () => void;
    disconnect: () => void;
    new_message: MessageHandler;
    message_delivered: MessageHandler;
    message_read: MessageHandler;
    typing_start: MessageHandler;
    typing_stop: MessageHandler;
    user_online: MessageHandler;
    user_offline: MessageHandler;
    call_incoming: MessageHandler;
    call_accepted: MessageHandler;
    call_declined: MessageHandler;
    call_ended: MessageHandler;
}

class WebSocketService {
    private socket: Socket | null = null;
    private handlers: Partial<Record<keyof WebSocketEvents, MessageHandler[]>> = {};
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    connect(token: string): void {
        if (this.socket?.connected) return;

        this.socket = io(WS_URL, {
            path: '/ws/socket.io',
            auth: { token },
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionAttempts: this.maxReconnectAttempts,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
        });

        this.socket.on('connect', () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.emit('connect');
        });

        this.socket.on('disconnect', (reason) => {
            console.log('WebSocket disconnected:', reason);
            this.emit('disconnect');
        });

        this.socket.on('connect_error', (error) => {
            console.error('WebSocket connection error:', error);
            this.reconnectAttempts++;
        });

        this.setupEventListeners();
    }

    disconnect(): void {
        if (this.socket) {
            this.socket.disconnect();
            this.socket = null;
        }
    }

    private setupEventListeners(): void {
        if (!this.socket) return;

        const events: (keyof WebSocketEvents)[] = [
            'new_message',
            'message_delivered',
            'message_read',
            'typing_start',
            'typing_stop',
            'user_online',
            'user_offline',
            'call_incoming',
            'call_accepted',
            'call_declined',
            'call_ended',
        ];

        events.forEach((event) => {
            this.socket?.on(event, (data: unknown) => {
                this.emit(event, data);
            });
        });
    }

    on<K extends keyof WebSocketEvents>(event: K, handler: MessageHandler): void {
        if (!this.handlers[event]) {
            this.handlers[event] = [];
        }
        this.handlers[event]!.push(handler);
    }

    off<K extends keyof WebSocketEvents>(event: K, handler: MessageHandler): void {
        const eventHandlers = this.handlers[event];
        if (eventHandlers) {
            const index = eventHandlers.indexOf(handler);
            if (index > -1) {
                eventHandlers.splice(index, 1);
            }
        }
    }

    private emit<K extends keyof WebSocketEvents>(event: K, data?: unknown): void {
        const eventHandlers = this.handlers[event];
        if (eventHandlers) {
            eventHandlers.forEach((handler) => handler(data));
        }
    }

    sendMessage(chatId: string, content: string, replyToId?: string): void {
        this.socket?.emit('send_message', { chat_id: chatId, content, reply_to_id: replyToId });
    }

    markDelivered(messageId: string): void {
        this.socket?.emit('mark_delivered', { message_id: messageId });
    }

    markRead(chatId: string): void {
        this.socket?.emit('mark_read', { chat_id: chatId });
    }

    startTyping(chatId: string): void {
        this.socket?.emit('typing_start', { chat_id: chatId });
    }

    stopTyping(chatId: string): void {
        this.socket?.emit('typing_stop', { chat_id: chatId });
    }

    joinChat(chatId: string): void {
        this.socket?.emit('join_chat', { chat_id: chatId });
    }

    leaveChat(chatId: string): void {
        this.socket?.emit('leave_chat', { chat_id: chatId });
    }

    get isConnected(): boolean {
        return this.socket?.connected ?? false;
    }
}

export const wsService = new WebSocketService();
