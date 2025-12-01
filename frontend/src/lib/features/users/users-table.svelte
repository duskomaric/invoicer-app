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

    // Icons
    import ChevronLeftIcon from "@tabler/icons-svelte/icons/chevron-left";
    import ChevronRightIcon from "@tabler/icons-svelte/icons/chevron-right";
    import UserIcon from "@tabler/icons-svelte/icons/user";
    import LayoutColumnsIcon from "@tabler/icons-svelte/icons/layout-columns";
    import ChevronDownIcon from "@tabler/icons-svelte/icons/chevron-down";

    // Feature Components
    import EditUserDialog from "./edit-user-dialog.svelte";
    import DeleteUserDialog from "./delete-user-dialog.svelte";
    import ViewUserDialog from "./view-user-dialog.svelte";

    // Props interface
    let {
        users,
        onUpdate,
    }: {
        users: User[];
        onUpdate: () => void;
    } = $props();

    // State
    let selectedIds = $state<number[]>([]);
    let currentPage = $state(0);
    const pageSize = 10;

    // Column Visibility State
    type ColumnKey = "id" | "email" | "full_name" | "is_active";
    let columnVisibility = $state<Record<ColumnKey, boolean>>({
        id: true,
        email: true,
        full_name: true,
        is_active: true,
    });

    // Derived state
    const totalPages = $derived(Math.ceil(users.length / pageSize));
    const paginatedUsers = $derived(
        users.slice(currentPage * pageSize, (currentPage + 1) * pageSize),
    );
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
     * Uses array spread to ensure Svelte 5 reactivity triggers.
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
        if (currentPage < totalPages - 1) currentPage++;
    }

    function prevPage() {
        if (currentPage > 0) currentPage--;
    }
</script>

<div class="space-y-4">
    <!-- Table Card -->
    <Card.Root>
        <Card.Header class="border-b bg-muted/50 transition-colors">
            <div class="flex items-center gap-2">
                <UserIcon class="h-5 w-5 text-muted-foreground" />
                <Card.Title class="text-lg">Users Management</Card.Title>
            </div>
            <Card.Description>
                Manage user accounts, permissions, and status
            </Card.Description>
        </Card.Header>

        <Card.Content class="p-0">
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
                        {#each paginatedUsers as user (user.id)}
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
                                            users={user}
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

        <!-- Pagination Footer -->
        {#if totalPages > 1}
            <Card.Footer class="flex items-center justify-between border-t p-4">
                <div class="text-sm text-muted-foreground">
                    Showing <span class="font-medium"
                        >{currentPage * pageSize + 1}</span
                    >
                    to
                    <span class="font-medium"
                        >{Math.min(
                            (currentPage + 1) * pageSize,
                            users.length,
                        )}</span
                    >
                    of <span class="font-medium">{users.length}</span> users
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
                    <Button
                        variant="outline"
                        size="sm"
                        onclick={nextPage}
                        disabled={currentPage >= totalPages - 1}
                    >
                        Next
                        <ChevronRightIcon class="h-4 w-4 ml-1" />
                    </Button>
                </div>
            </Card.Footer>
        {/if}
    </Card.Root>
</div>
