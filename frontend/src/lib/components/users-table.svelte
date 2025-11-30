<script lang="ts" module>
	import type { ColumnDef } from "@tanstack/table-core";
	import { renderComponent, renderSnippet } from "$lib/components/ui/data-table/index.js";
	import DataTableCheckbox from "$lib/components/data-table-checkbox.svelte";
	import { createRawSnippet } from "svelte";
	import EditUserDialog from "$lib/components/edit-user-dialog.svelte";
	import DeleteUserDialog from "$lib/components/delete-user-dialog.svelte";
	import ViewUserDialog from "$lib/components/view-user-dialog.svelte";

	export type User = {
		id: number;
		email: string;
		full_name: string;
		is_active: boolean;
	};

	export const columns: ColumnDef<User>[] = [
		{
			id: "select",
			header: ({ table }) =>
				renderComponent(DataTableCheckbox, {
					checked: table.getIsAllPageRowsSelected(),
					indeterminate:
						table.getIsSomePageRowsSelected() && !table.getIsAllPageRowsSelected(),
					onCheckedChange: (value) => table.toggleAllPageRowsSelected(!!value),
					"aria-label": "Select all",
				}),
			cell: ({ row }) =>
				renderComponent(DataTableCheckbox, {
					checked: row.getIsSelected(),
					onCheckedChange: (value) => row.toggleSelected(!!value),
					"aria-label": "Select row",
				}),
			enableSorting: false,
			enableHiding: false,
		},
		{
			accessorKey: "id",
			header: "ID",
		},
		{
			accessorKey: "email",
			header: "Email",
		},
		{
			accessorKey: "full_name",
			header: "Full Name",
		},
		{
			accessorKey: "is_active",
			header: "Status",
			cell: ({ row }) =>
				renderSnippet(
					createRawSnippet(() => ({
						render: () => `<div class="${row.original.is_active ? 'text-green-600' : 'text-red-600'}">${row.original.is_active ? 'Active' : 'Inactive'}</div>`,
					}))
				),
		},
		{
			id: "actions",
			header: "Actions",
			cell: ({ row }) =>
				renderSnippet(
					createRawSnippet(() => ({
						render: () => `<div class="flex gap-2" data-user-actions="${row.original.id}"></div>`,
					}))
				),
			enableSorting: false,
			enableHiding: false,
		},
	];
</script>

<script lang="ts">
	import {
		getCoreRowModel,
		getFacetedRowModel,
		getFacetedUniqueValues,
		getFilteredRowModel,
		getPaginationRowModel,
		getSortedRowModel,
		type ColumnFiltersState,
		type PaginationState,
		type RowSelectionState,
		type SortingState,
		type VisibilityState,
	} from "@tanstack/table-core";
	import { createSvelteTable } from "$lib/components/ui/data-table/data-table.svelte.js";
	import * as Table from "$lib/components/ui/table/index.js";
	import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import * as Select from "$lib/components/ui/select/index.js";
	import { Label } from "$lib/components/ui/label/index.js";
	import {
		FlexRender,
	} from "$lib/components/ui/data-table/index.js";
	import LayoutColumnsIcon from "@tabler/icons-svelte/icons/layout-columns";
	import ChevronDownIcon from "@tabler/icons-svelte/icons/chevron-down";
	import ChevronLeftIcon from "@tabler/icons-svelte/icons/chevron-left";
	import ChevronRightIcon from "@tabler/icons-svelte/icons/chevron-right";
	import ChevronsLeftIcon from "@tabler/icons-svelte/icons/chevrons-left";
	import ChevronsRightIcon from "@tabler/icons-svelte/icons/chevrons-right";

	let { 
		data,
		onUserUpdated,
		onUserDeleted 
	}: { 
		data: User[];
		onUserUpdated: () => void;
		onUserDeleted: () => void;
	} = $props();
	let pagination = $state<PaginationState>({ pageIndex: 0, pageSize: 10 });
	let sorting = $state<SortingState>([]);
	let columnFilters = $state<ColumnFiltersState>([]);
	let rowSelection = $state<RowSelectionState>({});
	let columnVisibility = $state<VisibilityState>({});

	const table = createSvelteTable({
		get data() {
			return data;
		},
		columns,
		state: {
			get pagination() {
				return pagination;
			},
			get sorting() {
				return sorting;
			},
			get columnVisibility() {
				return columnVisibility;
			},
			get rowSelection() {
				return rowSelection;
			},
			get columnFilters() {
				return columnFilters;
			},
		},
		getRowId: (row) => row.id.toString(),
		enableRowSelection: true,
		getCoreRowModel: getCoreRowModel(),
		getPaginationRowModel: getPaginationRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getFacetedRowModel: getFacetedRowModel(),
		getFacetedUniqueValues: getFacetedUniqueValues(),
		getFilteredRowModel: getFilteredRowModel(),
		onPaginationChange: (updater) => {
			if (typeof updater === "function") {
				pagination = updater(pagination);
			} else {
				pagination = updater;
			}
		},
		onSortingChange: (updater) => {
			if (typeof updater === "function") {
				sorting = updater(sorting);
			} else {
				sorting = updater;
			}
		},
		onColumnFiltersChange: (updater) => {
			if (typeof updater === "function") {
				columnFilters = updater(columnFilters);
			} else {
				columnFilters = updater;
			}
		},
		onColumnVisibilityChange: (updater) => {
			if (typeof updater === "function") {
				columnVisibility = updater(columnVisibility);
			} else {
				columnVisibility = updater;
			}
		},
		onRowSelectionChange: (updater) => {
			if (typeof updater === "function") {
				rowSelection = updater(rowSelection);
			} else {
				rowSelection = updater;
			}
		},
	});

	// Get selected users for bulk delete
	const selectedUsers = $derived(
		Object.keys(rowSelection)
			.map(id => data.find(user => user.id.toString() === id))
			.filter(Boolean) as User[]
	);
</script>

<div class="flex flex-col gap-4">
	<div class="flex items-center justify-between">
		<div class="flex items-center gap-2">
			<DropdownMenu.Root>
				<DropdownMenu.Trigger>
					{#snippet child({ props })}
						<Button variant="outline" size="sm" {...props}>
							<LayoutColumnsIcon />
							<span class="hidden lg:inline">Customize Columns</span>
							<span class="lg:hidden">Columns</span>
							<ChevronDownIcon />
						</Button>
					{/snippet}
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="end" class="w-56">
					{#each table
						.getAllColumns()
						.filter((col) => typeof col.accessorFn !== "undefined" && col.getCanHide()) as column (column.id)}
						<DropdownMenu.CheckboxItem
							class="capitalize"
							checked={column.getIsVisible()}
							onCheckedChange={(value) => column.toggleVisibility(!!value)}
						>
							{column.id}
						</DropdownMenu.CheckboxItem>
					{/each}
				</DropdownMenu.Content>
			</DropdownMenu.Root>
			{#if selectedUsers.length > 0}
				<DeleteUserDialog users={selectedUsers} onUsersDeleted={onUserDeleted} variant="bulk" />
			{/if}
		</div>
	</div>
	<div class="overflow-hidden rounded-lg border">
		<Table.Root>
			<Table.Header class="bg-muted sticky top-0 z-10">
				{#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
					<Table.Row>
						{#each headerGroup.headers as header (header.id)}
							<Table.Head colspan={header.colSpan}>
								{#if !header.isPlaceholder}
									<FlexRender
										content={header.column.columnDef.header}
										context={header.getContext()}
									/>
								{/if}
							</Table.Head>
						{/each}
					</Table.Row>
				{/each}
			</Table.Header>
			<Table.Body class="**:data-[slot=table-cell]:first:w-8">
				{#if table.getRowModel().rows?.length}
					{#each table.getRowModel().rows as row, index (row.id)}
						<Table.Row data-state={row.getIsSelected() && "selected"}>
							{#each row.getVisibleCells() as cell (cell.id)}
								<Table.Cell>
									{#if cell.column.id === "actions"}
										<div class="flex gap-2">
											<ViewUserDialog user={row.original} />
											<EditUserDialog user={row.original} onUserUpdated={onUserUpdated} />
											<DeleteUserDialog users={row.original} onUsersDeleted={onUserDeleted} variant="single" />
										</div>
									{:else}
										<FlexRender
											content={cell.column.columnDef.cell}
											context={cell.getContext()}
										/>
									{/if}
								</Table.Cell>
							{/each}
						</Table.Row>
					{/each}
				{:else}
					<Table.Row>
						<Table.Cell colspan={columns.length} class="h-24 text-center">
							No results.
						</Table.Cell>
					</Table.Row>
				{/if}
			</Table.Body>
		</Table.Root>
	</div>
	<div class="flex items-center justify-between">
		<div class="text-muted-foreground hidden flex-1 text-sm lg:flex">
			{table.getFilteredSelectedRowModel().rows.length} of
			{table.getFilteredRowModel().rows.length} row(s) selected.
		</div>
		<div class="flex w-full items-center gap-8 lg:w-fit">
			<div class="hidden items-center gap-2 lg:flex">
				<Label for="rows-per-page" class="text-sm font-medium">Rows per page</Label>
				<Select.Root
					type="single"
					bind:value={
						() => `${table.getState().pagination.pageSize}`,
						(v) => table.setPageSize(Number(v))
					}
				>
					<Select.Trigger size="sm" class="w-20" id="rows-per-page">
						{table.getState().pagination.pageSize}
					</Select.Trigger>
					<Select.Content side="top">
						{#each [10, 20, 30, 40, 50] as pageSize (pageSize)}
							<Select.Item value={pageSize.toString()}>
								{pageSize}
							</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>
			</div>
			<div class="flex w-fit items-center justify-center text-sm font-medium">
				Page {table.getState().pagination.pageIndex + 1} of
				{table.getPageCount()}
			</div>
			<div class="ms-auto flex items-center gap-2 lg:ms-0">
				<Button
					variant="outline"
					class="hidden h-8 w-8 p-0 lg:flex"
					onclick={() => table.setPageIndex(0)}
					disabled={!table.getCanPreviousPage()}
				>
					<span class="sr-only">Go to first page</span>
					<ChevronsLeftIcon />
				</Button>
				<Button
					variant="outline"
					class="size-8"
					size="icon"
					onclick={() => table.previousPage()}
					disabled={!table.getCanPreviousPage()}
				>
					<span class="sr-only">Go to previous page</span>
					<ChevronLeftIcon />
				</Button>
				<Button
					variant="outline"
					class="size-8"
					size="icon"
					onclick={() => table.nextPage()}
					disabled={!table.getCanNextPage()}
				>
					<span class="sr-only">Go to next page</span>
					<ChevronRightIcon />
				</Button>
				<Button
					variant="outline"
					class="hidden size-8 lg:flex"
					size="icon"
					onclick={() => table.setPageIndex(table.getPageCount() - 1)}
					disabled={!table.getCanNextPage()}
				>
					<span class="sr-only">Go to last page</span>
					<ChevronsRightIcon />
				</Button>
			</div>
		</div>
	</div>
</div>
