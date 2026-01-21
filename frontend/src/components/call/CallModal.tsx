/**
 * Модальное окно звонка
 */

import { useState, useEffect } from 'react';
import { callService } from '../../services/call';
import type { Call } from '../../types/call';

interface CallModalProps {
    call: Call | null;
    onClose: () => void;
}

export function CallModal({ call, onClose }: CallModalProps) {
    const [currentCall, setCurrentCall] = useState<Call | null>(call);
    const [duration, setDuration] = useState(0);

    useEffect(() => {
        setCurrentCall(call);
    }, [call]);

    useEffect(() => {
        if (currentCall?.status === 'active') {
            const timer = setInterval(() => {
                setDuration((d) => d + 1);
            }, 1000);
            return () => clearInterval(timer);
        }
    }, [currentCall?.status]);

    const handleAction = async (action: 'accept' | 'decline' | 'end') => {
        if (!currentCall) return;

        try {
            const updated = await callService.callAction(currentCall.id, action);
            setCurrentCall(updated);
            if (action === 'decline' || action === 'end') {
                setTimeout(onClose, 1000);
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    };

    const formatDuration = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    if (!currentCall) return null;

    const isIncoming = currentCall.status === 'pending' || currentCall.status === 'ringing';
    const isActive = currentCall.status === 'active';
    const isEnded = ['ended', 'missed', 'declined', 'failed'].includes(currentCall.status);

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
            <div className="bg-gray-900 rounded-3xl p-8 w-full max-w-sm text-center">
                {/* Avatar */}
                <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-4xl font-bold mb-4">
                    {currentCall.caller_name[0]?.toUpperCase()}
                </div>

                {/* Name */}
                <h2 className="text-2xl font-bold text-white mb-2">
                    {currentCall.caller_name}
                </h2>

                {/* Status */}
                <p className="text-gray-400 mb-8">
                    {isIncoming && 'Входящий звонок...'}
                    {isActive && formatDuration(duration)}
                    {isEnded && (
                        currentCall.status === 'ended' ? 'Звонок завершён' :
                            currentCall.status === 'missed' ? 'Пропущенный' :
                                currentCall.status === 'declined' ? 'Отклонён' : 'Ошибка'
                    )}
                </p>

                {/* Call type indicator */}
                <div className="flex justify-center gap-2 mb-8">
                    {currentCall.call_type === 'video' ? (
                        <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="m15.75 10.5 4.72-4.72a.75.75 0 0 1 1.28.53v11.38a.75.75 0 0 1-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 0 0 2.25-2.25v-9a2.25 2.25 0 0 0-2.25-2.25h-9A2.25 2.25 0 0 0 2.25 7.5v9a2.25 2.25 0 0 0 2.25 2.25Z" />
                        </svg>
                    ) : (
                        <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                        </svg>
                    )}
                </div>

                {/* Action buttons */}
                <div className="flex justify-center gap-4">
                    {isIncoming && (
                        <>
                            <button
                                onClick={() => handleAction('decline')}
                                className="w-16 h-16 rounded-full bg-red-500 hover:bg-red-600 flex items-center justify-center transition-colors"
                            >
                                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                            <button
                                onClick={() => handleAction('accept')}
                                className="w-16 h-16 rounded-full bg-green-500 hover:bg-green-600 flex items-center justify-center transition-colors"
                            >
                                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
                                </svg>
                            </button>
                        </>
                    )}

                    {isActive && (
                        <button
                            onClick={() => handleAction('end')}
                            className="w-16 h-16 rounded-full bg-red-500 hover:bg-red-600 flex items-center justify-center transition-colors"
                        >
                            <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    )}

                    {isEnded && (
                        <button
                            onClick={onClose}
                            className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-full transition-colors"
                        >
                            Закрыть
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}
