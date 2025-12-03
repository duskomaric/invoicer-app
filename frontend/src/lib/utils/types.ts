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

export type Product = {
    id: number;
    name: string;
    description: string | null;
    price: number;
    currency: string;
    created_at?: string;
    updated_at?: string;
    user_id?: number;
};

export type ProductCreate = {
    name: string;
    description?: string | null;
    price: number;
    currency?: string;
};

export type ProductUpdate = {
    name?: string;
    description?: string | null;
    price?: number;
    currency?: string;
};

export type InvoiceItem = {
    id: number;
    invoice_id: number;
    product_id: number;
    quantity: number;
    unit_price: number;
};

export type InvoiceItemCreate = {
    product_id: number;
    quantity: number;
    unit_price: number;
};

export type Invoice = {
    id: number;
    client_id: number;
    user_id: number;
    status: string;
    due_date: string;
    total_amount: number;
    currency: string;
    is_recurring: boolean;
    recurring_interval: string | null;
    created_at?: string;
    updated_at?: string;
    items: InvoiceItem[];
    client?: Client;
};

export type InvoiceCreate = {
    client_id: number;
    due_date: string;
    status?: string;
    currency?: string;
    is_recurring?: boolean;
    recurring_interval?: string | null;
    items: InvoiceItemCreate[];
};

export type InvoiceUpdate = {
    client_id?: number;
    status?: string;
    due_date?: string;
    is_recurring?: boolean;
    recurring_interval?: string | null;
    items?: InvoiceItemCreate[];
};
