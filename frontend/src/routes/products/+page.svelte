<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import { api } from "$lib/utils/api";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import AppSidebar from "$lib/components/app-sidebar.svelte";
    import SiteHeader from "$lib/components/site-header.svelte";
    import ProductsTable from "$lib/features/products/products-table.svelte";
    import CreateProductDialog from "$lib/features/products/create-product-dialog.svelte";
    import type { Product } from "$lib/features/products/products-table.svelte";

    let products = $state<Product[]>([]);
    let loading = $state(true);
    let error = $state("");

    // Pagination and Search state
    let totalCount = $state(0);
    let allCount = $state(0);
    let currentPage = $state(0);
    let pageSize = $state(10);
    let searchQuery = $state("");

    async function fetchProducts() {
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

            const response = await api.get<{
                data: Product[];
                meta: {
                    total: number;
                    page: number;
                    limit: number;
                    filters: {
                        all_count: number;
                    };
                };
            }>(`/api/v1/products/?${queryParams.toString()}`);

            products = response.data;
            totalCount = response.meta.total;
            allCount = response.meta.filters.all_count;
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

        // Fetch data
        fetchProducts();
    });

    function onProductCreated() {
        fetchProducts();
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
                            <h1 class="text-2xl font-bold">Products</h1>
                            <CreateProductDialog {onProductCreated} />
                        </div>
                        {#if loading && products.length === 0}
                            <div>Loading...</div>
                        {:else if error}
                            <div class="text-red-500">{error}</div>
                        {:else}
                            <ProductsTable
                                data={products}
                                {totalCount}
                                {allCount}
                                bind:currentPage
                                bind:pageSize
                                bind:searchQuery
                                onProductUpdated={fetchProducts}
                                onProductDeleted={fetchProducts}
                            />
                        {/if}
                    </div>
                </div>
            </div>
        </div>
    </Sidebar.Inset>
</Sidebar.Provider>
