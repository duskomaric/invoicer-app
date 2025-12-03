<script lang="ts">
    /**
     * ClientsTable Component
     *
     * Displays a paginated table of clients with selection, sorting, and actions.
     */
    import type { Client } from "$lib/utils/types";

    // UI Components
    import * as Table from "$lib/components/ui/table";
    import * as Card from "$lib/components/ui/card";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import { Badge } from "$lib/components/ui/badge";
    import { Checkbox } from "$lib/components/ui/checkbox";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";

    // Icons
    import ChevronLeftIcon from "@tabler/icons-svelte/icons/chevron-left";
    import ChevronRightIcon from "@tabler/icons-svelte/icons/chevron-right";
    import LayoutColumnsIcon from "@tabler/icons-svelte/icons/layout-columns";
    import ChevronDownIcon from "@tabler/icons-svelte/icons/chevron-down";
    import SearchIcon from "@tabler/icons-svelte/icons/search";
    import BuildingIcon from "@tabler/icons-svelte/icons/building";

    // Feature Components
    import EditClientDialog from "./edit-client-dialog.svelte";
    import DeleteClientDialog from "./delete-client-dialog.svelte";
    import ViewClientDialog from "./view-client-dialog.svelte";

    // Props interface
    let {
        data,
        onClientUpdated,
        onClientDeleted,
        searchQuery = $bindable(""),
        currentPage = $bindable(0),
        pageSize = $bindable(10),
        totalCount = 0,
        allCount = 0,
    }: {
        data: Client[];
        onClientUpdated: () => void;
        onClientDeleted: () => void;
        searchQuery?: string;
        currentPage?: number;
        pageSize?: number;
        totalCount?: number;
        allCount?: number;
    } = $props();

    // Use consistent naming internally
    const clients = $derived(data);

    // State
    let selectedIds = $state<number[]>([]);
    let localPageSize = $state(String(pageSize));

    // Local search input state (debounced)
    let searchInput = $state(searchQuery);
    let searchTimeout: ReturnType<typeof setTimeout> | null = null;

    // Column Visibility State
    type ColumnKey = "id" | "name" | "email" | "address";
    let columnVisibility = $state<Record<ColumnKey, boolean>>({
        id: true,
        name: true,
        email: true,
        address: true,
    });

    // Debounced search
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

    // Derived state
    const selectedClients = $derived(
        clients.filter((c) => selectedIds.includes(c.id)),
    );

    // Checkbox states
    const isAllSelected = $derived(
        clients.length > 0 && selectedIds.length === clients.length,
    );

    const isIndeterminate = $derived(
        selectedIds.length > 0 && selectedIds.length < clients.length,
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
            selectedIds = clients.map((c) => c.id);
        }
    }

    // Pagination handlers
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
</script>

<div class="space-y-4">
    <!-- Table Card -->
    <Card.Root>
        <Card.Header class="border-b bg-muted/50 transition-colors">
            <div class="flex items-center gap-2">
                <BuildingIcon class="h-5 w-5 text-muted-foreground" />
                <Card.Title class="text-lg">Clients Management</Card.Title>
            </div>
            <Card.Description>
                Manage your clients and their contact information
            </Card.Description>
        </Card.Header>

        <Card.Content class="p-0">
            <!-- Search Section -->
            <div class="p-4 border-b space-y-4">
                <div class="relative max-w-sm">
                    <SearchIcon
                        class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground"
                    />
                    <Input
                        type="text"
                        placeholder="Search by name or email..."
                        bind:value={searchInput}
                        class="pl-9"
                    />
                </div>

                <!-- All Filter Button -->
                <div class="flex gap-2">
                    <Button variant="default" size="sm">
                        All
                        <Badge variant="secondary" class="ml-2">
                            {allCount}
                        </Badge>
                    </Button>
                </div>
            </div>

            <!-- Toolbar -->
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
                                bind:checked={columnVisibility.email}
                            >
                                Email
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.address}
                            >
                                Address
                            </DropdownMenu.CheckboxItem>
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>

                    {#if selectedClients.length > 0}
                        <div class="flex items-center gap-2 ml-2">
                            <div class="h-6 w-px bg-border"></div>
                            <span class="text-sm text-muted-foreground ml-2">
                                {selectedClients.length} selected
                            </span>
                            <DeleteClientDialog
                                clients={selectedClients}
                                onClientsDeleted={onClientDeleted}
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
                                        clients.length && clients.length > 0}
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
                            {#if columnVisibility.email}
                                <Table.Head>Email</Table.Head>
                            {/if}
                            {#if columnVisibility.address}
                                <Table.Head>Address</Table.Head>
                            {/if}
                            <Table.Head class="text-right">Actions</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each clients as client (client.id)}
                            <Table.Row
                                data-state={selectedIds.includes(client.id)
                                    ? "selected"
                                    : undefined}
                            >
                                <Table.Cell>
                                    <Checkbox
                                        checked={selectedIds.includes(
                                            client.id,
                                        )}
                                        onCheckedChange={() =>
                                            toggleSelection(client.id)}
                                        aria-label="Select row"
                                    />
                                </Table.Cell>
                                {#if columnVisibility.id}
                                    <Table.Cell
                                        class="font-mono text-xs text-muted-foreground"
                                    >
                                        #{client.id}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.name}
                                    <Table.Cell class="font-medium"
                                        >{client.name}</Table.Cell
                                    >
                                {/if}
                                {#if columnVisibility.email}
                                    <Table.Cell>{client.email}</Table.Cell>
                                {/if}
                                {#if columnVisibility.address}
                                    <Table.Cell class="text-muted-foreground">
                                        {client.address || "—"}
                                    </Table.Cell>
                                {/if}
                                <Table.Cell class="text-right">
                                    <div class="flex justify-end gap-2">
                                        <ViewClientDialog {client} />
                                        <EditClientDialog
                                            {client}
                                            {onClientUpdated}
                                        />
                                        <DeleteClientDialog
                                            clients={[client]}
                                            onClientsDeleted={onClientDeleted}
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
                                        <p>No clients found</p>
                                        <Button
                                            variant="link"
                                            onclick={onClientUpdated}
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

        <!-- Pagination Footer -->
        {#if clients.length > 0}
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
                        of <span class="font-medium">{totalCount}</span> clients
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
                        disabled={clients.length < pageSize}
                    >
                        Next
                        <ChevronRightIcon class="h-4 w-4 ml-1" />
                    </Button>
                </div>
            </Card.Footer>
        {/if}
    </Card.Root>
</div>
