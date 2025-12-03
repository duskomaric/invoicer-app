<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { api } from "$lib/utils/api";
    import type { User } from "$lib/utils/types";
    import * as Sidebar from "$lib/components/ui/sidebar";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    import SiteHeader from "$lib/components/site-header.svelte";
    import UsersTable from "$lib/features/users/users-table.svelte";
    import CreateUserDialog from "$lib/features/users/create-user-dialog.svelte";

    let users = $state<User[]>([]);
    let loading = $state(true);
    let error = $state("");

    // Filter and pagination state
    let searchQuery = $state("");
    let statusFilter = $state<"all" | "active" | "inactive">("all");
    let currentPage = $state(0);
    let pageSize = $state(10);

    // Counts from API meta
    let totalCount = $state(0);
    let activeCount = $state(0);
    let inactiveCount = $state(0);

    async function fetchUsers() {
        const token = localStorage.getItem("token");
        if (!token) {
            goto("/login");
            return;
        }

        loading = true;
        error = "";
        try {
            // Build query parameters
            const params: Record<string, string | number | boolean> = {
                skip: currentPage * pageSize,
                limit: pageSize,
            };

            if (searchQuery.trim()) {
                params.search = searchQuery.trim();
            }

            if (statusFilter === "active") {
                params.is_active = true;
            } else if (statusFilter === "inactive") {
                params.is_active = false;
            }

            // Make API call with query params
            const queryString = new URLSearchParams(
                Object.entries(params).map(([key, value]) => [
                    key,
                    String(value),
                ]),
            ).toString();

            const response = await api.get<{
                data: User[];
                meta: {
                    total: number;
                    page: number;
                    limit: number;
                    filters: {
                        all_count: number;
                        active_count: number;
                        inactive_count: number;
                    };
                };
            }>(`/api/v1/users/?${queryString}`);

            // Extract data and meta
            users = response.data;
            totalCount = response.meta.filters.all_count;
            activeCount = response.meta.filters.active_count;
            inactiveCount = response.meta.filters.inactive_count;
        } catch (err: any) {
            if (err.message.includes("401")) {
                localStorage.removeItem("token");
                goto("/login");
                return;
            }
            error = err.message;
        } finally {
            loading = false;
        }
    }

    // Fetch when filters, page, or pageSize change
    $effect(() => {
        // Track dependencies
        const _search = searchQuery;
        const _filter = statusFilter;
        const _page = currentPage;
        const _size = pageSize;

        fetchUsers();
    });

    onMount(() => {
        fetchUsers();
    });
</script>

<Sidebar.Provider
    style="--sidebar-width: calc(var(--spacing) * 72); --header-height: calc(var(--spacing) * 12);"
>
    <AppSidebar variant="inset" />
    <Sidebar.Inset>
        <SiteHeader />
        <div class="flex flex-1 flex-col">
            <div class="@container/main flex flex-1 flex-col gap-2">
                <div class="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
                    <div class="px-4 lg:px-6">
                        <div class="flex justify-between items-center mb-4">
                            <h1 class="text-2xl font-bold">Users</h1>
                            <CreateUserDialog onUserCreated={fetchUsers} />
                        </div>
                        {#if loading}
                            <div>Loading...</div>
                        {:else if error}
                            <div class="text-red-500">{error}</div>
                        {:else}
                            <UsersTable
                                {users}
                                onUpdate={fetchUsers}
                                bind:searchQuery
                                bind:statusFilter
                                bind:currentPage
                                bind:pageSize
                                {totalCount}
                                {activeCount}
                                {inactiveCount}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </Sidebar.Inset>
</Sidebar.Provider>
