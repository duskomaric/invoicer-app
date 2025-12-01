<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { API_BASE_URL } from "$lib/config";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    import SiteHeader from "$lib/components/site-header.svelte";
    import ClientsTable from "$lib/components/clients-table.svelte";
    import CreateClientDialog from "$lib/components/create-client-dialog.svelte";

    let clients = $state([]);
    let loading = $state(true);
    let error = $state("");

    async function fetchClients() {
        const token = localStorage.getItem("token");
        if (!token) {
            goto("/login");
            return;
        }

        loading = true;
        error = "";
        try {
            const res = await fetch(`${API_BASE_URL}/api/v1/clients/`, {
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
                throw new Error("Failed to fetch clients");
            }

            clients = await res.json();
        } catch (err: any) {
            error = err.message;
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        fetchClients();
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
                            <h1 class="text-2xl font-bold">Clients</h1>
                            <CreateClientDialog
                                onClientCreated={fetchClients}
                            />
                        </div>
                        {#if loading}
                            <div>Loading...</div>
                        {:else if error}
                            <div class="text-red-500">{error}</div>
                        {:else}
                            <ClientsTable
                                data={clients}
                                onClientUpdated={fetchClients}
                                onClientDeleted={fetchClients}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </Sidebar.Inset>
</Sidebar.Provider>
