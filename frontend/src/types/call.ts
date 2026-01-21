/**
 * Типы для звонков
 */

export type CallType = 'audio' | 'video';
export type CallStatus = 'pending' | 'ringing' | 'active' | 'ended' | 'missed' | 'declined' | 'failed';

export interface Call {
    id: string;
    caller_id: string;
    caller_name: string;
    callee_id: string;
    callee_name: string;
    call_type: CallType;
    status: CallStatus;
    started_at: string | null;
    ended_at: string | null;
    duration_seconds: number | null;
    created_at: string;
}

export interface InitiateCallRequest {
    callee_id: string;
    call_type: CallType;
}

export interface CallActionRequest {
    action: 'accept' | 'decline' | 'end';
}
