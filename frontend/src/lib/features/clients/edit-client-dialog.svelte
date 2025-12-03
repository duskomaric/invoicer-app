<script lang="ts">
    /**
     * EditClientDialog Component
     */
    import { api } from "$lib/utils/api";
    import type { Client, ClientUpdate } from "$lib/utils/types";
    import { toast } from "svelte-sonner";

    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";

    import EditIcon from "@tabler/icons-svelte/icons/edit";
    import MailIcon from "@tabler/icons-svelte/icons/mail";
    import UserIcon from "@tabler/icons-svelte/icons/user";
    import MapPinIcon from "@tabler/icons-svelte/icons/map-pin";
    import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";

    let {
        client,
        onClientUpdated,
    }: {
        client: Client;
        onClientUpdated: () => void;
    } = $props();

    let open = $state(false);
    let name = $state(client.name);
    let email = $state(client.email);
    let address = $state(client.address || "");
    let error = $state("");
    let loading = $state(false);

    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = "";

        try {
            const clientUpdate: ClientUpdate = {
                name,
                email,
                address: address.trim() || null,
            };

            await api.put(`/api/v1/clients/${client.id}`, clientUpdate);
            toast.info(`Client "${name}" updated successfully!`);

            open = false;
            onClientUpdated();
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
        <Button variant="ghost" size="sm">
            <EditIcon class="h-4 w-4" />
        </Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <EditIcon class="h-5 w-5 text-primary" />
                Edit Client
            </Dialog.Title>
            <Dialog.Description>
                Update client information. Make changes and save.
            </Dialog.Description>
        </Dialog.Header>
        <form onsubmit={handleSubmit}>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="edit-name">Name</Label>
                    <div class="relative">
                        <UserIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Input
                            id="edit-name"
                            type="text"
                            placeholder="Acme Corp"
                            required
                            bind:value={name}
                            class="pl-9"
                        />
                    </div>
                </div>
                <div class="grid gap-2">
                    <Label for="edit-email">Email</Label>
                    <div class="relative">
                        <MailIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Input
                            id="edit-email"
                            type="email"
                            placeholder="contact@acme.com"
                            required
                            bind:value={email}
                            class="pl-9"
                        />
                    </div>
                </div>
                <div class="grid gap-2">
                    <Label for="edit-address">Address</Label>
                    <div class="relative">
                        <MapPinIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Textarea
                            id="edit-address"
                            placeholder="123 Main St, City, Country"
                            bind:value={address}
                            class="pl-9 min-h-[80px]"
                        />
                    </div>
                </div>
                {#if error}
                    <div class="text-red-500 text-sm flex items-center gap-2">
                        <div class="h-1 w-1 rounded-full bg-red-500"></div>
                        {error}
                    </div>
                {/if}
            </div>
            <Dialog.Footer>
                <Button type="submit" disabled={loading}>
                    {#if loading}
                        <Loader2Icon class="mr-2 h-4 w-4 animate-spin" />
                        Updating...
                    {:else}
                        Update Client
                    {/if}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
