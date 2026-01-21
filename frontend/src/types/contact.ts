/**
 * Типы для контактов и профиля
 */

export type ContactStatus = 'pending' | 'accepted' | 'blocked';

export interface Contact {
    id: string;
    user_id: string;
    contact_user_id: string;
    nickname: string | null;
    status: ContactStatus;
    contact_name: string;
    contact_email: string;
    contact_avatar: string | null;
    created_at: string;
}

export interface ContactListResponse {
    contacts: Contact[];
    total: number;
}

export interface CreateContactRequest {
    contact_user_id: string;
    nickname?: string;
}

export interface UpdateContactRequest {
    nickname?: string;
    status?: ContactStatus;
}

export interface ProfileUpdateRequest {
    name?: string;
    bio?: string;
    avatar_url?: string;
}
