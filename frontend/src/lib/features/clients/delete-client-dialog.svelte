<script lang="ts">
    /**
     * DeleteClientDialog Component
     */
    import { api } from "$lib/utils/api";
    import type { Client } from "$lib/utils/types";
    import { toast } from "svelte-sonner";

    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import TrashIcon from "@tabler/icons-svelte/icons/trash";
    import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";
    import AlertTriangleIcon from "@tabler/icons-svelte/icons/alert-triangle";

    let {
        clients,
        onClientsDeleted,
        variant = "single",
    }: {
        clients: Client[];
        onClientsDeleted: () => void;
        variant?: "single" | "bulk";
    } = $props();

    let open = $state(false);
    let loading = $state(false);
    let error = $state("");

    async function handleDelete() {
        loading = true;
        error = "";

        try {
            await Promise.all(
                clients.map((client) =>
                    api.delete(`/api/v1/clients/${client.id}`),
                ),
            );

            const message =
                clients.length === 1
                    ? `Client "${clients[0].name}" deleted successfully!`
                    : `${clients.length} clients deleted successfully!`;

            toast.info(message);
            open = false;
            onClientsDeleted();
        } catch (err) {
            if (err instanceof Error) {
                error = err.message;
            } else {
                error = "An unknown error occurred";
            }
        } finally {
            loading = false;
        }
    }
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger>
        {#if variant === "bulk"}
            <Button variant="destructive" size="sm">
                <TrashIcon class="mr-2 h-4 w-4" />
                Delete Selected
            </Button>
        {:else}
            <Button variant="ghost" size="sm">
                <TrashIcon class="h-4 w-4" />
            </Button>
        {/if}
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <AlertTriangleIcon class="h-5 w-5 text-destructive" />
                {clients.length === 1
                    ? "Delete Client"
                    : `Delete ${clients.length} Clients`}
            </Dialog.Title>
            <Dialog.Description>
                {#if clients.length === 1}
                    Are you sure you want to delete "{clients[0].name}"? This
                    action cannot be undone.
                {:else}
                    Are you sure you want to delete {clients.length} clients? This
                    action cannot be undone.
                {/if}
            </Dialog.Description>
        </Dialog.Header>
        <div class="py-4">
            {#if error}
                <div
                    class="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm"
                >
                    {error}
                </div>
            {/if}
            <div class="flex justify-end gap-2">
                <Button variant="outline" onclick={() => (open = false)}>
                    Cancel
                </Button>
                <Button
                    variant="destructive"
                    onclick={handleDelete}
                    disabled={loading}
                >
                    {#if loading}
                        <Loader2Icon class="mr-2 h-4 w-4 animate-spin" />
                        Deleting...
                    {:else}
                        Delete
                    {/if}
                </Button>
            </div>
        </div>
    </Dialog.Content>
</Dialog.Root>
