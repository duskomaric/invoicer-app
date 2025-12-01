<script lang="ts">
    import { API_BASE_URL } from "$lib/config";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Field, FieldLabel } from "$lib/components/ui/field/index.js";
    import type { Client } from "$lib/components/clients-table.svelte";
    import { toast } from "svelte-sonner";

    let {
        client,
        onClientUpdated,
    }: { client: Client; onClientUpdated: () => void } = $props();

    let open = $state(false);
    let name = $state(client.name);
    let email = $state(client.email);
    let address = $state(client.address || "");
    let error = $state("");
    let loading = $state(false);

    // Update form when client prop changes
    $effect(() => {
        name = client.name;
        email = client.email;
        address = client.address || "";
    });

    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = "";

        try {
            const token = localStorage.getItem("token");
            if (!token) {
                throw new Error("Not authenticated");
            }

            const updateData = {
                name,
                email,
                address: address || null,
            };

            const res = await fetch(
                `${API_BASE_URL}/api/v1/clients/${client.id}`,
                {
                    method: "PUT",
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(updateData),
                },
            );

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Failed to update client");
            }

            open = false;
            toast.success(`Client "${name}" updated successfully!`);
            onClientUpdated();
        } catch (err: any) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger>
        <Button variant="ghost" size="sm">Edit</Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title>Edit Client</Dialog.Title>
            <Dialog.Description>Update client information.</Dialog.Description>
        </Dialog.Header>
        <form onsubmit={handleSubmit}>
            <div class="grid gap-4 py-4">
                <Field>
                    <FieldLabel for="edit-name">Name</FieldLabel>
                    <Input
                        id="edit-name"
                        type="text"
                        required
                        bind:value={name}
                    />
                </Field>
                <Field>
                    <FieldLabel for="edit-email">Email</FieldLabel>
                    <Input
                        id="edit-email"
                        type="email"
                        required
                        bind:value={email}
                    />
                </Field>
                <Field>
                    <FieldLabel for="edit-address"
                        >Address (Optional)</FieldLabel
                    >
                    <Input id="edit-address" type="text" bind:value={address} />
                </Field>
                {#if error}
                    <div class="text-red-500 text-sm">{error}</div>
                {/if}
            </div>
            <Dialog.Footer>
                <Button type="submit" disabled={loading}>
                    {loading ? "Updating..." : "Update Client"}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
