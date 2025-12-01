<script lang="ts">
    import { API_BASE_URL } from "$lib/config";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import { Button } from "$lib/components/ui/button/index.js";
    import { Input } from "$lib/components/ui/input/index.js";
    import { Field, FieldLabel } from "$lib/components/ui/field/index.js";
    import { toast } from "svelte-sonner";

    let { onClientCreated }: { onClientCreated: () => void } = $props();

    let open = $state(false);
    let name = $state("");
    let email = $state("");
    let address = $state("");
    let error = $state("");
    let loading = $state(false);

    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = "";

        try {
            const token = localStorage.getItem("token");
            if (!token) {
                throw new Error("Not authenticated");
            }

            const res = await fetch(`${API_BASE_URL}/api/v1/clients/`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    email,
                    address: address || null,
                }),
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "Failed to create client");
            }

            // Show success toast before resetting
            toast.info(`Client "${name}" created successfully!`);

            // Reset form
            name = "";
            email = "";
            address = "";
            open = false;
            onClientCreated();
        } catch (err: any) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger>
        <Button>Create Client</Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title>Create New Client</Dialog.Title>
            <Dialog.Description>
                Add a new client to the system. Fill in all the required fields.
            </Dialog.Description>
        </Dialog.Header>
        <form onsubmit={handleSubmit}>
            <div class="grid gap-4 py-4">
                <Field>
                    <FieldLabel for="name">Name</FieldLabel>
                    <Input id="name" type="text" required bind:value={name} />
                </Field>
                <Field>
                    <FieldLabel for="email">Email</FieldLabel>
                    <Input
                        id="email"
                        type="email"
                        required
                        bind:value={email}
                    />
                </Field>
                <Field>
                    <FieldLabel for="address">Address (Optional)</FieldLabel>
                    <Input id="address" type="text" bind:value={address} />
                </Field>
                {#if error}
                    <div class="text-red-500 text-sm">{error}</div>
                {/if}
            </div>
            <Dialog.Footer>
                <Button type="submit" disabled={loading}>
                    {loading ? "Creating..." : "Create Client"}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
