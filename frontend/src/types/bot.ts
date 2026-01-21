/**
 * Типы для ботов
 */

export type BotStatus = 'active' | 'inactive' | 'suspended';

export interface BotResponse {
    id: string;
    name: string;
    username: string;
    description: string | null;
    about: string | null;
    owner_id: string;
    status: BotStatus;
    api_token: string | null;
    created_at: string;
}

export interface BotCommand {
    command: string;
    description: string;
}

export interface BotButton {
    text: string;
    callback_data?: string;
    url?: string;
}

export interface BotKeyboard {
    buttons: BotButton[][];
    resize?: boolean;
    one_time?: boolean;
}

export interface InlineButton {
    text: string;
    callback_data?: string;
    url?: string;
    switch_inline?: string;
}

export interface InlineKeyboard {
    buttons: InlineButton[][];
}

export interface CreateBotRequest {
    name: string;
    username: string;
    description?: string;
    about?: string;
}

export interface BotMessageRequest {
    chat_id: string;
    text: string;
    keyboard?: BotKeyboard;
    inline_keyboard?: InlineKeyboard;
    reply_to_message_id?: string;
}
