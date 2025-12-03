<script lang="ts" context="module">
    export type Product = {
        id: number;
        name: string;
        description: string | null;
        price: number;
        currency: string;
        created_at?: string;
        updated_at?: string;
    };
</script>

<script lang="ts">
    /**
     * ProductsTable Component
     */
    import type { Product as ProductType } from "$lib/utils/types";

    import * as Table from "$lib/components/ui/table";
    import * as Card from "$lib/components/ui/card";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import { Badge } from "$lib/components/ui/badge";
    import { Checkbox } from "$lib/components/ui/checkbox";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";

    import ChevronLeftIcon from "@tabler/icons-svelte/icons/chevron-left";
    import ChevronRightIcon from "@tabler/icons-svelte/icons/chevron-right";
    import LayoutColumnsIcon from "@tabler/icons-svelte/icons/layout-columns";
    import ChevronDownIcon from "@tabler/icons-svelte/icons/chevron-down";
    import SearchIcon from "@tabler/icons-svelte/icons/search";
    import PackageIcon from "@tabler/icons-svelte/icons/package";

    import EditProductDialog from "./edit-product-dialog.svelte";
    import DeleteProductDialog from "./delete-product-dialog.svelte";
    import ViewProductDialog from "./view-product-dialog.svelte";

    let {
        data,
        onProductUpdated,
        onProductDeleted,
        searchQuery = $bindable(""),
        currentPage = $bindable(0),
        pageSize = $bindable(10),
        totalCount = 0,
        allCount = 0,
    }: {
        data: ProductType[];
        onProductUpdated: () => void;
        onProductDeleted: () => void;
        searchQuery?: string;
        currentPage?: number;
        pageSize?: number;
        totalCount?: number;
        allCount?: number;
    } = $props();

    const products = $derived(data);

    let selectedIds = $state<number[]>([]);
    let localPageSize = $state(String(pageSize));

    let searchInput = $state(searchQuery);
    let searchTimeout: ReturnType<typeof setTimeout> | null = null;

    type ColumnKey = "id" | "name" | "description" | "price";
    let columnVisibility = $state<Record<ColumnKey, boolean>>({
        id: true,
        name: true,
        description: true,
        price: true,
    });

    $effect(() => {
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }

        searchTimeout = setTimeout(() => {
            if (searchQuery !== searchInput) {
                currentPage = 0;
            }
            searchQuery = searchInput;
        }, 300);
    });

    const selectedProducts = $derived(
        products.filter((p) => selectedIds.includes(p.id)),
    );

    const isAllSelected = $derived(
        products.length > 0 && selectedIds.length === products.length,
    );

    function toggleSelection(id: number) {
        if (selectedIds.includes(id)) {
            selectedIds = selectedIds.filter((sid: number) => sid !== id);
        } else {
            selectedIds = [...selectedIds, id];
        }
    }

    function toggleAll() {
        if (isAllSelected) {
            selectedIds = [];
        } else {
            selectedIds = products.map((p) => p.id);
        }
    }

    function nextPage() {
        currentPage++;
    }

    function prevPage() {
        if (currentPage > 0) currentPage--;
    }

    function changePageSize(size: number) {
        pageSize = size;
        currentPage = 0;
    }

    function formatPrice(price: number, currency: string) {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: currency,
        }).format(price);
    }
</script>

<div class="space-y-4">
    <Card.Root>
        <Card.Header class="border-b bg-muted/50 transition-colors">
            <div class="flex items-center gap-2">
                <PackageIcon class="h-5 w-5 text-muted-foreground" />
                <Card.Title class="text-lg">Products Management</Card.Title>
            </div>
            <Card.Description>
                Manage your products and services catalog
            </Card.Description>
        </Card.Header>

        <Card.Content class="p-0">
            <div class="p-4 border-b space-y-4">
                <div class="relative max-w-sm">
                    <SearchIcon
                        class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground"
                    />
                    <Input
                        type="text"
                        placeholder="Search by name..."
                        bind:value={searchInput}
                        class="pl-9"
                    />
                </div>

                <div class="flex gap-2">
                    <Button variant="default" size="sm">
                        All
                        <Badge variant="secondary" class="ml-2">
                            {allCount}
                        </Badge>
                    </Button>
                </div>
            </div>

            <div class="flex items-center justify-between p-4 border-b">
                <div class="flex items-center gap-2">
                    <DropdownMenu.Root>
                        <DropdownMenu.Trigger>
                            {#snippet child({ props })}
                                <Button variant="outline" size="sm" {...props}>
                                    <LayoutColumnsIcon class="mr-2 h-4 w-4" />
                                    Customize Columns
                                    <ChevronDownIcon class="ml-2 h-4 w-4" />
                                </Button>
                            {/snippet}
                        </DropdownMenu.Trigger>
                        <DropdownMenu.Content align="start" class="w-56">
                            <DropdownMenu.Label
                                >Toggle Columns</DropdownMenu.Label
                            >
                            <DropdownMenu.Separator />
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.id}
                            >
                                ID
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.name}
                            >
                                Name
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.description}
                            >
                                Description
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.price}
                            >
                                Price
                            </DropdownMenu.CheckboxItem>
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>

                    {#if selectedProducts.length > 0}
                        <div class="flex items-center gap-2 ml-2">
                            <div class="h-6 w-px bg-border"></div>
                            <span class="text-sm text-muted-foreground ml-2">
                                {selectedProducts.length} selected
                            </span>
                            <DeleteProductDialog
                                products={selectedProducts}
                                onProductsDeleted={onProductDeleted}
                                variant="bulk"
                            />
                        </div>
                    {/if}
                </div>
            </div>

            <div class="overflow-hidden">
                <Table.Root>
                    <Table.Header>
                        <Table.Row>
                            <Table.Head class="w-[50px]">
                                <Checkbox
                                    checked={selectedIds.length ===
                                        products.length && products.length > 0}
                                    onCheckedChange={toggleAll}
                                    aria-label="Select all"
                                />
                            </Table.Head>
                            {#if columnVisibility.id}
                                <Table.Head class="w-[80px]">ID</Table.Head>
                            {/if}
                            {#if columnVisibility.name}
                                <Table.Head>Name</Table.Head>
                            {/if}
                            {#if columnVisibility.description}
                                <Table.Head>Description</Table.Head>
                            {/if}
                            {#if columnVisibility.price}
                                <Table.Head>Price</Table.Head>
                            {/if}
                            <Table.Head class="text-right">Actions</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each products as product (product.id)}
                            <Table.Row
                                data-state={selectedIds.includes(product.id)
                                    ? "selected"
                                    : undefined}
                            >
                                <Table.Cell>
                                    <Checkbox
                                        checked={selectedIds.includes(
                                            product.id,
                                        )}
                                        onCheckedChange={() =>
                                            toggleSelection(product.id)}
                                        aria-label="Select row"
                                    />
                                </Table.Cell>
                                {#if columnVisibility.id}
                                    <Table.Cell
                                        class="font-mono text-xs text-muted-foreground"
                                    >
                                        #{product.id}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.name}
                                    <Table.Cell class="font-medium"
                                        >{product.name}</Table.Cell
                                    >
                                {/if}
                                {#if columnVisibility.description}
                                    <Table.Cell
                                        class="text-muted-foreground max-w-xs truncate"
                                    >
                                        {product.description || "—"}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.price}
                                    <Table.Cell class="font-semibold">
                                        {formatPrice(
                                            product.price,
                                            product.currency,
                                        )}
                                    </Table.Cell>
                                {/if}
                                <Table.Cell class="text-right">
                                    <div class="flex justify-end gap-2">
                                        <ViewProductDialog {product} />
                                        <EditProductDialog
                                            {product}
                                            {onProductUpdated}
                                        />
                                        <DeleteProductDialog
                                            products={[product]}
                                            onProductsDeleted={onProductDeleted}
                                            variant="single"
                                        />
                                    </div>
                                </Table.Cell>
                            </Table.Row>
                        {:else}
                            <Table.Row>
                                <Table.Cell
                                    colspan={6}
                                    class="h-24 text-center"
                                >
                                    <div
                                        class="flex flex-col items-center justify-center gap-2 text-muted-foreground"
                                    >
                                        <p>No products found</p>
                                        <Button
                                            variant="link"
                                            onclick={onProductUpdated}
                                        >
                                            Refresh Data
                                        </Button>
                                    </div>
                                </Table.Cell>
                            </Table.Row>
                        {/each}
                    </Table.Body>
                </Table.Root>
            </div>
        </Card.Content>

        {#if products.length > 0}
            <Card.Footer class="flex items-center justify-between border-t p-4">
                <div class="flex items-center gap-4">
                    <div class="flex items-center gap-2">
                        <span class="text-sm text-muted-foreground"
                            >Per page:</span
                        >
                        <select
                            class="border rounded p-1 text-sm"
                            bind:value={localPageSize}
                            onchange={() =>
                                changePageSize(Number(localPageSize))}
                        >
                            <option value="5">5</option>
                            <option value="10">10</option>
                            <option value="25">25</option>
                            <option value="50">50</option>
                            <option value="100">100</option>
                        </select>
                    </div>

                    <div class="text-sm text-muted-foreground">
                        Showing
                        <span class="font-medium"
                            >{currentPage * pageSize + 1}</span
                        >
                        to
                        <span class="font-medium">
                            {Math.min((currentPage + 1) * pageSize, totalCount)}
                        </span>
                        of <span class="font-medium">{totalCount}</span> products
                    </div>
                </div>

                <div class="flex gap-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onclick={prevPage}
                        disabled={currentPage === 0}
                    >
                        <ChevronLeftIcon class="h-4 w-4 mr-1" />
                        Previous
                    </Button>

                    <span
                        class="flex items-center text-sm text-muted-foreground px-3"
                    >
                        Page {currentPage + 1}
                    </span>

                    <Button
                        variant="outline"
                        size="sm"
                        onclick={nextPage}
                        disabled={products.length < pageSize}
                    >
                        Next
                        <ChevronRightIcon class="h-4 w-4 ml-1" />
                    </Button>
                </div>
            </Card.Footer>
        {/if}
    </Card.Root>
</div>
