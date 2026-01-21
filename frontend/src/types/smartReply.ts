/**
 * Типы для smart replies
 */

export interface SmartReplyRequest {
    message_id: string;
    context_messages?: number;
}

export interface SmartReplyResponse {
    replies: string[];
    confidence?: number[];
}

export interface SmartReplySettings {
    enabled: boolean;
    max_suggestions: number;
    include_emoji: boolean;
    formal_style: boolean;
}

export const DEFAULT_SMART_REPLY_SETTINGS: SmartReplySettings = {
    enabled: true,
    max_suggestions: 3,
    include_emoji: true,
    formal_style: false,
};
