/**
 * Сервис профиля и контактов
 */

import { api } from './api';
import type { User } from '../types/auth';
import type {
    Contact,
    ContactListResponse,
    CreateContactRequest,
    ProfileUpdateRequest,
    UpdateContactRequest,
} from '../types/contact';

export const profileService = {
    async getProfile(): Promise<User> {
        return api.get<User>('/profile/me');
    },

    async updateProfile(data: ProfileUpdateRequest): Promise<User> {
        return api.put<User>('/profile/me', data);
    },

    async searchUsers(query: string): Promise<User[]> {
        return api.get<User[]>(`/profile/search?q=${encodeURIComponent(query)}`);
    },

    async getContacts(): Promise<ContactListResponse> {
        return api.get<ContactListResponse>('/profile/contacts');
    },

    async addContact(data: CreateContactRequest): Promise<Contact> {
        return api.post<Contact>('/profile/contacts', data);
    },

    async updateContact(contactId: string, data: UpdateContactRequest): Promise<Contact> {
        return api.put<Contact>(`/profile/contacts/${contactId}`, data);
    },

    async deleteContact(contactId: string): Promise<void> {
        return api.delete(`/profile/contacts/${contactId}`);
    },
};
