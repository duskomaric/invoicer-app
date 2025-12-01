export type User = {
    id: number;
    email: string;
    full_name: string;
    is_active: boolean;
    created_at?: string;
    updated_at?: string;
};

export type UserCreate = {
    email: string;
    full_name: string;
    password: string;
};

export type UserUpdate = {
    email?: string;
    full_name?: string;
    is_active?: boolean;
};

export type Client = {
    id: number;
    name: string;
    email: string;
    address: string | null;
    created_at?: string;
    updated_at?: string;
    user_id?: number;
};

export type ClientCreate = {
    name: string;
    email: string;
    address?: string | null;
};

export type ClientUpdate = {
    name?: string;
    email?: string;
    address?: string | null;
};
