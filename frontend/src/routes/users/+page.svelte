<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { API_BASE_URL } from "$lib/config";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    import SiteHeader from "$lib/components/site-header.svelte";
    import UsersTable from "$lib/components/users-table.svelte";
    import CreateUserDialog from "$lib/components/create-user-dialog.svelte";

    let users = $state([]);
    let loading = $state(true);
    let error = $state("");

    async function fetchUsers() {
        const token = localStorage.getItem("token");
        if (!token) {
            goto("/login");
            return;
        }

        loading = true;
        error = "";
        try {
            const res = await fetch(`${API_BASE_URL}/api/v1/users/`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (!res.ok) {
                if (res.status === 401) {
                    localStorage.removeItem("token");
                    goto("/login");
                    return;
                }
                throw new Error("Failed to fetch users");
            }

            users = await res.json();
        } catch (err: any) {
            error = err.message;
        } finally {
            loading = false;
        }
    }

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
                                data={users}
                                onUserUpdated={fetchUsers}
                                onUserDeleted={fetchUsers}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </Sidebar.Inset>
</Sidebar.Provider>
