/**
 * Модальное окно добавления контакта
 */

import { useState } from 'react';
import { useContactStore } from '../../store/contactStore';
import { profileService } from '../../services/profile';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import type { User } from '../../types/auth';

interface AddContactModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export function AddContactModal({ isOpen, onClose }: AddContactModalProps) {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState<User[]>([]);
    const [isSearching, setIsSearching] = useState(false);
    const [isAdding, setIsAdding] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { addContact } = useContactStore();

    if (!isOpen) return null;

    const handleSearch = async () => {
        if (searchQuery.length < 2) return;

        setIsSearching(true);
        setError(null);
        try {
            const users = await profileService.searchUsers(searchQuery);
            setSearchResults(users);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка поиска');
        } finally {
            setIsSearching(false);
        }
    };

    const handleAddContact = async (user: User) => {
        setIsAdding(true);
        setError(null);
        try {
            await addContact(user.id);
            setSearchResults((prev) => prev.filter((u) => u.id !== user.id));
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка добавления');
        } finally {
            setIsAdding(false);
        }
    };

    const handleClose = () => {
        setSearchQuery('');
        setSearchResults([]);
        setError(null);
        onClose();
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/50" onClick={handleClose} />
            <div className="relative bg-white rounded-2xl shadow-xl w-full max-w-md mx-4 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Добавить контакт</h2>

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-4">
                        {error}
                    </div>
                )}

                <div className="flex gap-2 mb-4">
                    <Input
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Поиск по имени или email"
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    />
                    <Button onClick={handleSearch} isLoading={isSearching}>
                        Найти
                    </Button>
                </div>

                <div className="max-h-64 overflow-y-auto">
                    {searchResults.length === 0 ? (
                        <p className="text-center text-gray-500 py-4">
                            {searchQuery ? 'Пользователи не найдены' : 'Введите запрос для поиска'}
                        </p>
                    ) : (
                        <div className="space-y-2">
                            {searchResults.map((user) => (
                                <div
                                    key={user.id}
                                    className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
                                >
                                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-semibold">
                                        {user.name[0]?.toUpperCase()}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <p className="font-medium text-gray-900 truncate">{user.name}</p>
                                        <p className="text-sm text-gray-500 truncate">{user.email}</p>
                                    </div>
                                    <Button
                                        size="sm"
                                        onClick={() => handleAddContact(user)}
                                        isLoading={isAdding}
                                    >
                                        Добавить
                                    </Button>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                <div className="mt-6">
                    <Button variant="outline" className="w-full" onClick={handleClose}>
                        Закрыть
                    </Button>
                </div>
            </div>
        </div>
    );
}
