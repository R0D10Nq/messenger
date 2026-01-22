/**
 * Список контактов
 */

import { useEffect } from 'react';
import { useContactStore } from '../../store/contactStore';
import { useChatStore } from '../../store/chatStore';
import type { Contact } from '../../types/contact';

interface ContactItemProps {
    contact: Contact;
    onStartChat: (userId: string) => void;
    onDelete: (contactId: string) => void;
}

function ContactItem({ contact, onStartChat, onDelete }: ContactItemProps) {
    const displayName = contact.nickname || contact.contact_name;

    return (
        <div className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white font-semibold text-lg flex-shrink-0">
                {displayName[0]?.toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">{displayName}</p>
                <p className="text-sm text-gray-500 truncate">{contact.contact_email}</p>
            </div>
            <div className="flex items-center gap-2">
                <button
                    onClick={() => onStartChat(contact.contact_id)}
                    className="p-2 hover:bg-gray-200 rounded-full transition-colors"
                    title="Написать"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="w-5 h-5 text-blue-600"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M8.625 12a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H8.25m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0H12m4.125 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 0 1-2.555-.337A5.972 5.972 0 0 1 5.41 20.97a5.969 5.969 0 0 1-.474-.065 4.48 4.48 0 0 0 .978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25Z"
                        />
                    </svg>
                </button>
                <button
                    onClick={() => onDelete(contact.id)}
                    className="p-2 hover:bg-red-100 rounded-full transition-colors"
                    title="Удалить"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="w-5 h-5 text-red-600"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0"
                        />
                    </svg>
                </button>
            </div>
        </div>
    );
}

interface ContactListProps {
    onClose?: () => void;
}

export function ContactList({ onClose }: ContactListProps) {
    const { contacts, isLoading, loadContacts, deleteContact } = useContactStore();
    const { createDirectChat, selectChat } = useChatStore();

    useEffect(() => {
        loadContacts();
    }, [loadContacts]);

    const handleStartChat = async (userId: string) => {
        try {
            const chat = await createDirectChat(userId);
            selectChat(chat.id);
            onClose?.();
        } catch {
            // Ошибка обработана в store
        }
    };

    const handleDelete = async (contactId: string) => {
        if (confirm('Удалить контакт?')) {
            await deleteContact(contactId);
        }
    };

    if (isLoading && contacts.length === 0) {
        return (
            <div className="flex items-center justify-center p-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
            </div>
        );
    }

    if (contacts.length === 0) {
        return (
            <div className="text-center text-gray-500 p-8">
                <p>Нет контактов</p>
                <p className="text-sm mt-1">Добавьте контакты для общения</p>
            </div>
        );
    }

    return (
        <div className="space-y-1">
            {contacts.map((contact) => (
                <ContactItem
                    key={contact.id}
                    contact={contact}
                    onStartChat={handleStartChat}
                    onDelete={handleDelete}
                />
            ))}
        </div>
    );
}
