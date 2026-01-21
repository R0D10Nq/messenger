/**
 * Типы для 2FA и безопасности
 */

export interface TwoFactorStatus {
    enabled: boolean;
    verified_at: string | null;
}

export interface Setup2FAResponse {
    secret: string;
    qr_code_base64: string;
    provisioning_uri: string;
}

export interface Verify2FARequest {
    code: string;
}

export interface Verify2FAResponse {
    success: boolean;
    message: string;
}
