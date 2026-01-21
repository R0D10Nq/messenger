/**
 * Компонент клавиатуры бота
 */

import type { BotKeyboard as BotKeyboardType, InlineKeyboard } from '../../types/bot';

interface BotKeyboardProps {
    keyboard: BotKeyboardType;
    onButtonClick: (callbackData: string) => void;
}

export function BotKeyboard({ keyboard, onButtonClick }: BotKeyboardProps) {
    return (
        <div className={`flex flex-col gap-2 p-2 bg-gray-100 dark:bg-gray-800 ${keyboard.resize ? '' : 'min-h-[200px]'}`}>
            {keyboard.buttons.map((row, rowIdx) => (
                <div key={rowIdx} className="flex gap-2">
                    {row.map((button, btnIdx) => (
                        <button
                            key={btnIdx}
                            onClick={() => {
                                if (button.url) {
                                    window.open(button.url, '_blank');
                                } else if (button.callback_data) {
                                    onButtonClick(button.callback_data);
                                }
                            }}
                            className="flex-1 py-3 px-4 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg text-gray-900 dark:text-white font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                        >
                            {button.text}
                        </button>
                    ))}
                </div>
            ))}
        </div>
    );
}

interface InlineKeyboardProps {
    keyboard: InlineKeyboard;
    onButtonClick: (callbackData: string) => void;
}

export function InlineKeyboardComponent({ keyboard, onButtonClick }: InlineKeyboardProps) {
    return (
        <div className="flex flex-col gap-1 mt-2">
            {keyboard.buttons.map((row, rowIdx) => (
                <div key={rowIdx} className="flex gap-1">
                    {row.map((button, btnIdx) => (
                        <button
                            key={btnIdx}
                            onClick={() => {
                                if (button.url) {
                                    window.open(button.url, '_blank');
                                } else if (button.callback_data) {
                                    onButtonClick(button.callback_data);
                                }
                            }}
                            className="flex-1 py-2 px-3 bg-blue-500/10 border border-blue-500/30 rounded text-blue-500 text-sm font-medium hover:bg-blue-500/20 transition-colors flex items-center justify-center gap-1"
                        >
                            {button.url && (
                                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                            )}
                            {button.text}
                        </button>
                    ))}
                </div>
            ))}
        </div>
    );
}

interface BotCommandsMenuProps {
    commands: Array<{ command: string; description: string }>;
    onSelect: (command: string) => void;
    onClose: () => void;
}

export function BotCommandsMenu({ commands, onSelect, onClose }: BotCommandsMenuProps) {
    if (commands.length === 0) {
        return null;
    }

    return (
        <div className="absolute bottom-full left-0 right-0 mb-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg overflow-hidden">
            <div className="flex items-center justify-between px-3 py-2 border-b border-gray-200 dark:border-gray-700">
                <span className="text-sm font-medium text-gray-900 dark:text-white">Команды</span>
                <button
                    onClick={onClose}
                    className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
                >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div className="max-h-48 overflow-y-auto">
                {commands.map((cmd) => (
                    <button
                        key={cmd.command}
                        onClick={() => onSelect(`/${cmd.command}`)}
                        className="w-full px-3 py-2 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                        <span className="text-blue-500 font-medium">/{cmd.command}</span>
                        <span className="text-gray-500 dark:text-gray-400 ml-2 text-sm">{cmd.description}</span>
                    </button>
                ))}
            </div>
        </div>
    );
}
