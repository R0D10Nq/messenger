/**
 * Zustand store для контактов
 */

import { create } from 'zustand';
import type { Contact } from '../types/contact';
import { profileService } from '../services/profile';

interface ContactState {
    contacts: Contact[];
    isLoading: boolean;
    error: string | null;
}

interface ContactActions {
    loadContacts: () => Promise<void>;
    addContact: (userId: string, nickname?: string) => Promise<Contact>;
    updateContact: (contactId: string, nickname: string) => Promise<void>;
    deleteContact: (contactId: string) => Promise<void>;
    clearError: () => void;
}

export const useContactStore = create<ContactState & ContactActions>((set, get) => ({
    contacts: [],
    isLoading: false,
    error: null,

    loadContacts: async () => {
        set({ isLoading: true, error: null });
        try {
            const response = await profileService.getContacts();
            set({ contacts: response.contacts, isLoading: false });
        } catch (error) {
            set({
                isLoading: false,
                error: error instanceof Error ? error.message : 'Ошибка загрузки контактов',
            });
        }
    },

    addContact: async (userId: string, nickname?: string) => {
        try {
            const contact = await profileService.addContact({
                contact_user_id: userId,
                nickname,
            });
            const { contacts } = get();
            set({ contacts: [...contacts, contact] });
            return contact;
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Ошибка добавления контакта',
            });
            throw error;
        }
    },

    updateContact: async (contactId: string, nickname: string) => {
        try {
            const updated = await profileService.updateContact(contactId, { nickname });
            const { contacts } = get();
            set({
                contacts: contacts.map((c) => (c.id === contactId ? updated : c)),
            });
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Ошибка обновления контакта',
            });
            throw error;
        }
    },

    deleteContact: async (contactId: string) => {
        try {
            await profileService.deleteContact(contactId);
            const { contacts } = get();
            set({ contacts: contacts.filter((c) => c.id !== contactId) });
        } catch (error) {
            set({
                error: error instanceof Error ? error.message : 'Ошибка удаления контакта',
            });
            throw error;
        }
    },

    clearError: () => set({ error: null }),
}));
