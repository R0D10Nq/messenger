/**
 * Сервис для поиска по сообщениям
 */

import { api } from './api';
import type { SearchParams, SearchResponse } from '../types/search';

export const searchService = {
    async search(params: SearchParams): Promise<SearchResponse> {
        const queryParams = new URLSearchParams();
        queryParams.set('q', params.q);

        if (params.chat_id) queryParams.set('chat_id', params.chat_id);
        if (params.search_type) queryParams.set('search_type', params.search_type);
        if (params.sender_id) queryParams.set('sender_id', params.sender_id);
        if (params.limit) queryParams.set('limit', params.limit.toString());
        if (params.offset) queryParams.set('offset', params.offset.toString());

        return api.get<SearchResponse>(`/search?${queryParams.toString()}`);
    },
};
