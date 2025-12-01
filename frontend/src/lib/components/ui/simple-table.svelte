<script lang="ts" generics="T">
    import { Button } from "$lib/components/ui/button";
    import * as Table from "$lib/components/ui/table";
    import ChevronLeftIcon from "@tabler/icons-svelte/icons/chevron-left";
    import ChevronRightIcon from "@tabler/icons-svelte/icons/chevron-right";

    type Column<T> = {
        key: keyof T | "actions";
        header: string;
        cell?: (item: T) => any;
    };

    let {
        data,
        columns,
        pageSize = 10,
    }: {
        data: T[];
        columns: Column<T>[];
        pageSize?: number;
    } = $props();

    let currentPage = $state(0);

    const totalPages = $derived(Math.ceil(data.length / pageSize));
    const paginatedData = $derived(
        data.slice(currentPage * pageSize, (currentPage + 1) * pageSize),
    );

    function nextPage() {
        if (currentPage < totalPages - 1) currentPage++;
    }

    function prevPage() {
        if (currentPage > 0) currentPage--;
    }
</script>

<div class="space-y-4">
    <div class="overflow-hidden rounded-lg border">
        <Table.Root>
            <Table.Header>
                <Table.Row>
                    {#each columns as column}
                        <Table.Head>{column.header}</Table.Head>
                    {/each}
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {#if paginatedData.length === 0}
                    <Table.Row>
                        <Table.Cell
                            colspan={columns.length}
                            class="h-24 text-center"
                        >
                            No results.
                        </Table.Cell>
                    </Table.Row>
                {:else}
                    {#each paginatedData as item}
                        <Table.Row>
                            {#each columns as column}
                                <Table.Cell>
                                    {#if column.cell}
                                        {@render column.cell(item)}
                                    {:else if column.key !== "actions"}
                                        {item[column.key as keyof T]}
                                    {/if}
                                </Table.Cell>
                            {/each}
                        </Table.Row>
                    {/each}
                {/if}
            </Table.Body>
        </Table.Root>
    </div>

    {#if totalPages > 1}
        <div class="flex items-center justify-between">
            <div class="text-sm text-muted-foreground">
                Page {currentPage + 1} of {totalPages}
            </div>
            <div class="flex gap-2">
                <Button
                    variant="outline"
                    size="sm"
                    onclick={prevPage}
                    disabled={currentPage === 0}
                >
                    <ChevronLeftIcon class="h-4 w-4" />
                    Previous
                </Button>
                <Button
                    variant="outline"
                    size="sm"
                    onclick={nextPage}
                    disabled={currentPage >= totalPages - 1}
                >
                    Next
                    <ChevronRightIcon class="h-4 w-4" />
                </Button>
            </div>
        </div>
    {/if}
</div>
