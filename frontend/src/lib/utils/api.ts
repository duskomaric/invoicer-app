import { API_BASE_URL } from '$lib/config';

export async function apiRequest<T = any>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const token = localStorage.getItem('token');

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            ...options.headers
        }
    });

    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
        return undefined as T;
    }

    return response.json();
}

export const api = {
    get: <T = any>(endpoint: string) => apiRequest<T>(endpoint, { method: 'GET' }),

    post: <T = any>(endpoint: string, data: any) =>
        apiRequest<T>(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        }),

    put: <T = any>(endpoint: string, data: any) =>
        apiRequest<T>(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        }),

    delete: <T = any>(endpoint: string) =>
        apiRequest<T>(endpoint, { method: 'DELETE' })
};
