/**
 * Типы для контактов и профиля
 */

export type ContactStatus = 'pending' | 'accepted' | 'blocked';

export interface Contact {
    id: string;
    contact_id: string;
    nickname: string | null;
    status: ContactStatus;
    contact_name: string;
    contact_email: string;
    contact_avatar_url: string | null;
    contact_status_message: string | null;
    created_at: string;
}

export interface ContactListResponse {
    contacts: Contact[];
    total: number;
}

export interface CreateContactRequest {
    contact_id: string;
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
