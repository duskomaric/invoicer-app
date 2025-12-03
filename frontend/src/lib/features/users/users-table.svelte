<script lang="ts">
    /**
     * UsersTable Component
     *
     * Displays a paginated table of users with selection, sorting, and actions.
     * Acts as a reference implementation for other data tables in the application.
     */
    import type { User } from "$lib/utils/types";

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

    // Feature Components
    import EditUserDialog from "./edit-user-dialog.svelte";
    import DeleteUserDialog from "./delete-user-dialog.svelte";
    import ViewUserDialog from "./view-user-dialog.svelte";
    import UsersIcon from "@tabler/icons-svelte/icons/users";
    import ChevronsRightIcon from "@tabler/icons-svelte/icons/chevrons-right";
    import ChevronsLeftIcon from "@tabler/icons-svelte/icons/chevrons-left";

    // Props interface
    let {
        users,
        onUpdate,
        searchQuery = $bindable(""),
        statusFilter = $bindable<"all" | "active" | "inactive">("all"),
        currentPage = $bindable(0),
        pageSize = $bindable(10),
        totalCount = 0,
        activeCount = 0,
        inactiveCount = 0,
    }: {
        users: User[];
        onUpdate: () => void;
        searchQuery?: string;
        statusFilter?: "all" | "active" | "inactive";
        currentPage?: number;
        pageSize?: number;
        totalCount?: number;
        activeCount?: number;
        inactiveCount?: number;
    } = $props();

    // State
    let selectedIds = $state<number[]>([]);
    let localPageSize = $state(String(pageSize));

    // Local search input state (debounced)
    let searchInput = $state(searchQuery);
    let searchTimeout: ReturnType<typeof setTimeout> | null = null;

    // Column Visibility State
    type ColumnKey = "id" | "email" | "full_name" | "is_active";
    let columnVisibility = $state<Record<ColumnKey, boolean>>({
        id: true,
        email: true,
        full_name: true,
        is_active: true,
    });

    // Debounced search: update searchQuery after user stops typing
    $effect(() => {
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }

        searchTimeout = setTimeout(() => {
            // If search actually changed, reset to page 0
            if (searchQuery !== searchInput) {
                currentPage = 0;
            }
            searchQuery = searchInput;
        }, 300);
    });

    // Derived state - users are already filtered by backend
    const selectedUsers = $derived(
        users.filter((u) => selectedIds.includes(u.id)),
    );

    // Checkbox states
    const isAllSelected = $derived(
        users.length > 0 && selectedIds.length === users.length,
    );

    const isIndeterminate = $derived(
        selectedIds.length > 0 && selectedIds.length < users.length,
    );

    /**
     * Toggles selection of a single user.
     */
    function toggleSelection(id: number) {
        if (selectedIds.includes(id)) {
            selectedIds = selectedIds.filter((sid: number) => sid !== id);
        } else {
            selectedIds = [...selectedIds, id];
        }
    }

    /**
     * Toggles selection of all users.
     */
    function toggleAll() {
        if (isAllSelected) {
            selectedIds = [];
        } else {
            selectedIds = users.map((u) => u.id);
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
                <UsersIcon class="h-5 w-5 text-muted-foreground" />
                <Card.Title class="text-lg">Users Management</Card.Title>
            </div>
            <Card.Description>
                Manage user accounts, permissions, and status
            </Card.Description>
        </Card.Header>

        <Card.Content class="p-0">
            <!-- Search and Filter Section -->
            <div class="p-4 border-b space-y-4">
                <!-- Search Input -->
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

                <!-- Status Filter Buttons -->
                <div class="flex gap-2">
                    <Button
                        variant={statusFilter === "all" ? "default" : "outline"}
                        size="sm"
                        onclick={() => {
                            if (statusFilter !== "all") {
                                currentPage = 0;
                            }
                            statusFilter = "all";
                        }}
                    >
                        All
                        <Badge variant="secondary" class="ml-2">
                            {totalCount}
                        </Badge>
                    </Button>
                    <Button
                        variant={statusFilter === "active"
                            ? "default"
                            : "outline"}
                        size="sm"
                        onclick={() => {
                            if (statusFilter !== "active") {
                                currentPage = 0;
                            }
                            statusFilter = "active";
                        }}
                    >
                        Active
                        <Badge variant="secondary" class="ml-2">
                            {activeCount}
                        </Badge>
                    </Button>
                    <Button
                        variant={statusFilter === "inactive"
                            ? "default"
                            : "outline"}
                        size="sm"
                        onclick={() => {
                            if (statusFilter !== "inactive") {
                                currentPage = 0;
                            }
                            statusFilter = "inactive";
                        }}
                    >
                        Inactive
                        <Badge variant="secondary" class="ml-2">
                            {inactiveCount}
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
                                bind:checked={columnVisibility.email}
                            >
                                Email
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.full_name}
                            >
                                Full Name
                            </DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem
                                bind:checked={columnVisibility.is_active}
                            >
                                Status
                            </DropdownMenu.CheckboxItem>
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>

                    {#if selectedUsers.length > 0}
                        <div class="flex items-center gap-2 ml-2">
                            <div class="h-6 w-px bg-border"></div>
                            <span class="text-sm text-muted-foreground ml-2">
                                {selectedUsers.length} selected
                            </span>
                            <DeleteUserDialog
                                users={selectedUsers}
                                onUsersDeleted={onUpdate}
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
                                        users.length && users.length > 0}
                                    onCheckedChange={toggleAll}
                                    aria-label="Select all"
                                />
                            </Table.Head>
                            {#if columnVisibility.id}
                                <Table.Head class="w-[80px]">ID</Table.Head>
                            {/if}
                            {#if columnVisibility.email}
                                <Table.Head>Email</Table.Head>
                            {/if}
                            {#if columnVisibility.full_name}
                                <Table.Head>Full Name</Table.Head>
                            {/if}
                            {#if columnVisibility.is_active}
                                <Table.Head>Status</Table.Head>
                            {/if}
                            <Table.Head class="text-right">Actions</Table.Head>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {#each users as user (user.id)}
                            <Table.Row
                                data-state={selectedIds.includes(user.id)
                                    ? "selected"
                                    : undefined}
                            >
                                <Table.Cell>
                                    <Checkbox
                                        checked={selectedIds.includes(user.id)}
                                        onCheckedChange={() =>
                                            toggleSelection(user.id)}
                                        aria-label="Select row"
                                    />
                                </Table.Cell>
                                {#if columnVisibility.id}
                                    <Table.Cell
                                        class="font-mono text-xs text-muted-foreground"
                                    >
                                        #{user.id}
                                    </Table.Cell>
                                {/if}
                                {#if columnVisibility.email}
                                    <Table.Cell>{user.email}</Table.Cell>
                                {/if}
                                {#if columnVisibility.full_name}
                                    <Table.Cell class="font-medium"
                                        >{user.full_name}</Table.Cell
                                    >
                                {/if}
                                {#if columnVisibility.is_active}
                                    <Table.Cell>
                                        <Badge
                                            variant={user.is_active
                                                ? "default"
                                                : "secondary"}
                                        >
                                            {user.is_active
                                                ? "Active"
                                                : "Inactive"}
                                        </Badge>
                                    </Table.Cell>
                                {/if}
                                <Table.Cell class="text-right">
                                    <div class="flex justify-end gap-2">
                                        <ViewUserDialog {user} />
                                        <EditUserDialog
                                            {user}
                                            onUserUpdated={onUpdate}
                                        />
                                        <DeleteUserDialog
                                            users={[user]}
                                            onUsersDeleted={onUpdate}
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
                                        <p>No users found</p>
                                        <Button
                                            variant="link"
                                            onclick={onUpdate}
                                            >Refresh Data</Button
                                        >
                                    </div>
                                </Table.Cell>
                            </Table.Row>
                        {/each}
                    </Table.Body>
                </Table.Root>
            </div>
        </Card.Content>

        <!-- Pagination Footer - Always show if there are users -->
        {#if users.length > 0}
            <Card.Footer class="flex items-center justify-between border-t p-4">
                <!-- Left side: perPage + info -->
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
                        of <span class="font-medium">{totalCount}</span> users
                    </div>
                </div>

                <!-- Right side: pagination buttons -->
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
                        disabled={users.length < pageSize}
                    >
                        Next
                        <ChevronRightIcon class="h-4 w-4 ml-1" />
                    </Button>
                </div>
            </Card.Footer>
        {/if}
    </Card.Root>
</div>
