<script lang="ts">
    /**
     * InvoicesTable Component
     */
    import type { Invoice as InvoiceType } from "$lib/utils/types";

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
    import FileInvoiceIcon from "@tabler/icons-svelte/icons/file-invoice";

    import EditInvoiceDialog from "./edit-invoice-dialog.svelte";
    import DeleteInvoiceDialog from "./delete-invoice-dialog.svelte";
    import ViewInvoiceDialog from "./view-invoice-dialog.svelte";

    let {
        data,
        onInvoiceUpdated,
        onInvoiceDeleted,
        searchQuery = $bindable(""),
        currentPage = $bindable(0),
        pageSize = $bindable(10),
        totalCount = 0,
        allCount = 0,
    }: {
        data: InvoiceType[];
        onInvoiceUpdated: () => void;
        onInvoiceDeleted: () => void;
        searchQuery?: string;
        currentPage?: number;
        pageSize?: number;
        totalCount?: number;
        allCount?: number;
    } = $props();

    const invoices = $derived(data);

    let selectedIds = $state<number[]>([]);
    let localPageSize = $state(String(pageSize));

    let searchInput = $state(searchQuery);
    let searchTimeout: ReturnType<typeof setTimeout> | null = null;

    type ColumnKey =
        | "id"
        | "client_name"
        | "status"
        | "due_date"
        | "total_amount"
        | "created_at"
        | "is_recurring";

    let columnVisibility = $state<Record<ColumnKey, boolean>>({
        id: true,
        client_name: true,
        status: true,
        due_date: true,
        total_amount: true,
        created_at: false,
        is_recurring: false,
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

    const selectedInvoices = $derived(
        invoices.filter((inv) => selectedIds.includes(inv.id)),
    );

    const isAllSelected = $derived(
        invoices.length > 0 && selectedIds.length === invoices.length,
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
            selectedIds = invoices.map((inv) => inv.id);
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

    function formatDate(dateString: string) {
        if (!dateString) return "-";
        return new Date(dateString).toLocaleDateString();
    }

    function getStatusVariant(status: string) {
        switch (status) {
            case "paid":
                return "default";
            case "sent":
                return "secondary";
            case "draft":
                return "outline";
            case "cancelled":
                return "destructive";
            default:
                return "secondary";
        }
    }
</script>

<div class="space-y-4">
    <Card.Root>
        <Card.Header class="border-b bg-muted/50 transition-colors">
            <div class="flex items-center gap-2">
                <FileInvoiceIcon class="h-5 w-5 text-muted-foreground" />
                <Card.Title class="text-lg">Invoices Management</Card.Title>
            </div>
            <Card.Description>
                Manage your invoices and track payments
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
                        placeholder="Search invoices..."
                        bind:value={searchInput}
                        class="pl-9"
                    />
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
                                bind:checked={columnVisibility.client_name}
                            >
                                Client
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.status}
                            >
                                Status
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.due_date}
                            >
                                Due Date
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.total_amount}
                            >
                                Total Amount
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.created_at}
                            >
                                Created At
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.is_recurring}
                            >
                                Recurring
                            </DropdownMenu.CheckboxItem>
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>

                    {#if selectedInvoices.length > 0}
                        <div class="flex items-center gap-2 ml-2">
                            <div class="h-6 w-px bg-border"></div>
                            <span class="text-sm text-muted-foreground ml-2">
                                {selectedInvoices.length} selected
                            </span>
                            <DeleteInvoiceDialog
                                invoices={selectedInvoices}
                                onInvoicesDeleted={onInvoiceDeleted}
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
                                        invoices.length && invoices.length > 0}
                                    onCheckedChange={toggleAll}
                                    aria-label="Select all"
                                />
                            </Table.Head>
                            {#if columnVisibility.id}
                                <Table.Head class="w-[80px]">ID</Table.Head>
                            {/if}
                            {#if columnVisibility.client_name}
                                <Table.Head>Client Name</Table.Head>
                            {/if}
                            {#if columnVisibility.status}
                                <Table.Head>Status</Table.Head>
                            {/if}
                            {#if columnVisibility.due_date}
                                <Table.Head>Due Date</Table.Head>
                            {/if}
                            {#if columnVisibility.created_at}
                                <Table.Head>Created At</Table.Head>
                            {/if}
                            {#if columnVisibility.is_recurring}
                                <Table.Head>Recurring</Table.Head>
                            {/if}
                            {#if columnVisibility.total_amount}
                                <Table.Head>Total</Table.Head>
                            {/if}
                            <Table.Head class="text-right">Actions</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each invoices as invoice (invoice.id)}
                            <Table.Row
                                data-state={selectedIds.includes(invoice.id)
                                    ? "selected"
                                    : undefined}
                            >
                                <Table.Cell>
                                    <Checkbox
                                        checked={selectedIds.includes(
                                            invoice.id,
                                        )}
                                        onCheckedChange={() =>
                                            toggleSelection(invoice.id)}
                                        aria-label="Select row"
                                    />
                                </Table.Cell>
                                {#if columnVisibility.id}
                                    <Table.Cell
                                        class="font-mono text-xs text-muted-foreground"
                                    >
                                        #{invoice.id}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.client_name}
                                    <Table.Cell>
                                        {invoice.client?.name ||
                                            `Client #${invoice.client_id}`}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.status}
                                    <Table.Cell>
                                        <Badge
                                            variant={getStatusVariant(
                                                invoice.status,
                                            )}
                                        >
                                            {invoice.status.toUpperCase()}
                                        </Badge>
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.due_date}
                                    <Table.Cell>
                                        {formatDate(invoice.due_date)}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.created_at}
                                    <Table.Cell>
                                        {formatDate(invoice.created_at || "")}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.is_recurring}
                                    <Table.Cell>
                                        {#if invoice.is_recurring}
                                            <Badge variant="outline">Yes</Badge>
                                        {:else}
                                            <span class="text-muted-foreground"
                                                >-</span
                                            >
                                        {/if}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.total_amount}
                                    <Table.Cell class="font-semibold">
                                        {formatPrice(
                                            invoice.total_amount,
                                            invoice.currency,
                                        )}
                                    </Table.Cell>
                                {/if}
                                <Table.Cell class="text-right">
                                    <div class="flex justify-end gap-2">
                                        <ViewInvoiceDialog {invoice} />
                                        <EditInvoiceDialog
                                            {invoice}
                                            {onInvoiceUpdated}
                                        />
                                        <DeleteInvoiceDialog
                                            invoices={[invoice]}
                                            onInvoicesDeleted={onInvoiceDeleted}
                                            variant="single"
                                        />
                                    </div>
                                </Table.Cell>
                            </Table.Row>
                        {:else}
                            <Table.Row>
                                <Table.Cell
                                    colspan={7}
                                    class="h-24 text-center"
                                >
                                    <div
                                        class="flex flex-col items-center justify-center gap-2 text-muted-foreground"
                                    >
                                        <p>No invoices found</p>
                                        <Button
                                            variant="link"
                                            onclick={onInvoiceUpdated}
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

        {#if invoices.length > 0}
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
                        of <span class="font-medium">{totalCount}</span> invoices
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
                        disabled={invoices.length < pageSize}
                    >
                        Next
                        <ChevronRightIcon class="h-4 w-4 ml-1" />
                    </Button>
                </div>
            </Card.Footer>
        {/if}
    </Card.Root>
</div>
