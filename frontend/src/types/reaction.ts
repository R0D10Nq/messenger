/**
 * Типы для реакций на сообщения
 */

export interface ReactionSummary {
    emoji: string;
    count: number;
    users: string[];
    reacted_by_me: boolean;
}

export interface MessageReactions {
    message_id: string;
    reactions: ReactionSummary[];
    total_count: number;
}

export interface ReactionCreate {
    emoji: string;
}
