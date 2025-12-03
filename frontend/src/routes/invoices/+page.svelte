<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { api } from "$lib/utils/api";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    import SiteHeader from "$lib/components/site-header.svelte";
    import InvoicesTable from "$lib/features/invoices/invoices-table.svelte";
    import CreateInvoiceDialog from "$lib/features/invoices/create-invoice-dialog.svelte";
    import type { Invoice } from "$lib/utils/types";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Button } from "$lib/components/ui/button/index.js";

    let invoices = $state<Invoice[]>([]);
    let loading = $state(true);
    let error = $state("");

    // Pagination and Search state
    let totalCount = $state(0);
    let allCount = $state(0);
    let draftCount = $state(0);
    let sentCount = $state(0);
    let paidCount = $state(0);
    let cancelledCount = $state(0);

    let currentPage = $state(0);
    let pageSize = $state(10);
    let searchQuery = $state("");
    let statusFilter = $state<string>("all");

    async function fetchInvoices() {
        loading = true;
        error = "";
        try {
            const queryParams = new URLSearchParams({
                skip: (currentPage * pageSize).toString(),
                limit: pageSize.toString(),
            });

            if (searchQuery) {
                queryParams.append("search", searchQuery);
            }

            if (statusFilter !== "all") {
                queryParams.append("status", statusFilter);
            }

            const response = await api.get<{
                data: Invoice[];
                meta: {
                    total: number;
                    page: number;
                    limit: number;
                    filters: {
                        all_count: number;
                        draft_count: number;
                        sent_count: number;
                        paid_count: number;
                        cancelled_count: number;
                    };
                };
            }>(`/api/v1/invoices/?${queryParams.toString()}`);

            invoices = response.data;
            totalCount = response.meta.total;
            allCount = response.meta.filters.all_count;
            draftCount = response.meta.filters.draft_count;
            sentCount = response.meta.filters.sent_count;
            paidCount = response.meta.filters.paid_count;
            cancelledCount = response.meta.filters.cancelled_count;
        } catch (err: any) {
            error = err.message;
            if (err.message === "Unauthorized") {
                goto("/login");
            }
        } finally {
            loading = false;
        }
    }

    // Reactivity for fetching data
    $effect(() => {
        // Track dependencies
        const _page = currentPage;
        const _size = pageSize;
        const _search = searchQuery;
        const _status = statusFilter;

        // Fetch data
        fetchInvoices();
    });

    function onInvoiceCreated() {
        fetchInvoices();
    }
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
                            <h1 class="text-2xl font-bold">Invoices</h1>
                            <CreateInvoiceDialog {onInvoiceCreated} />
                        </div>

                        <!-- Status Filters -->
                        <div class="flex gap-2 mb-4 overflow-x-auto pb-2">
                            <Button
                                variant={statusFilter === "all"
                                    ? "default"
                                    : "outline"}
                                size="sm"
                                onclick={() => {
                                    statusFilter = "all";
                                    currentPage = 0;
                                }}
                            >
                                All <Badge variant="secondary" class="ml-2"
                                    >{allCount}</Badge
                                >
                            </Button>
                            <Button
                                variant={statusFilter === "draft"
                                    ? "default"
                                    : "outline"}
                                size="sm"
                                onclick={() => {
                                    statusFilter = "draft";
                                    currentPage = 0;
                                }}
                            >
                                Draft <Badge variant="secondary" class="ml-2"
                                    >{draftCount}</Badge
                                >
                            </Button>
                            <Button
                                variant={statusFilter === "sent"
                                    ? "default"
                                    : "outline"}
                                size="sm"
                                onclick={() => {
                                    statusFilter = "sent";
                                    currentPage = 0;
                                }}
                            >
                                Sent <Badge variant="secondary" class="ml-2"
                                    >{sentCount}</Badge
                                >
                            </Button>
                            <Button
                                variant={statusFilter === "paid"
                                    ? "default"
                                    : "outline"}
                                size="sm"
                                onclick={() => {
                                    statusFilter = "paid";
                                    currentPage = 0;
                                }}
                            >
                                Paid <Badge variant="secondary" class="ml-2"
                                    >{paidCount}</Badge
                                >
                            </Button>
                            <Button
                                variant={statusFilter === "cancelled"
                                    ? "default"
                                    : "outline"}
                                size="sm"
                                onclick={() => {
                                    statusFilter = "cancelled";
                                    currentPage = 0;
                                }}
                            >
                                Cancelled <Badge
                                    variant="secondary"
                                    class="ml-2">{cancelledCount}</Badge
                                >
                            </Button>
                        </div>

                        {#if loading && invoices.length === 0}
                            <div>Loading...</div>
                        {:else if error}
                            <div class="text-red-500">{error}</div>
                        {:else}
                            <InvoicesTable
                                data={invoices}
                                {totalCount}
                                {allCount}
                                bind:currentPage
                                bind:pageSize
                                bind:searchQuery
                                onInvoiceUpdated={fetchInvoices}
                                onInvoiceDeleted={fetchInvoices}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </Sidebar.Inset>
</Sidebar.Provider>
