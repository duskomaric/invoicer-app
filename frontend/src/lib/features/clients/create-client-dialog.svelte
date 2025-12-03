<script lang="ts">
    /**
     * CreateClientDialog Component
     *
     * A modal dialog for creating new clients.
     */
    import { api } from "$lib/utils/api";
    import type { ClientCreate } from "$lib/utils/types";
    import { toast } from "svelte-sonner";

    // UI Components
    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";

    // Icons
    import UserPlusIcon from "@tabler/icons-svelte/icons/user-plus";
    import MailIcon from "@tabler/icons-svelte/icons/mail";
    import UserIcon from "@tabler/icons-svelte/icons/user";
    import MapPinIcon from "@tabler/icons-svelte/icons/map-pin";
    import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";
    import PlusIcon from "@tabler/icons-svelte/icons/plus";

    // Props
    let { onClientCreated }: { onClientCreated: () => void } = $props();

    // State
    let open = $state(false);
    let name = $state("");
    let email = $state("");
    let address = $state("");
    let error = $state("");
    let loading = $state(false);

    /**
     * Handles form submission to create a new client.
     */
    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = "";

        try {
            const clientData: ClientCreate = {
                name,
                email,
                address: address.trim() || null,
            };

            await api.post("/api/v1/clients/", clientData);

            toast.info(`Client "${name}" created successfully!`);

            // Reset form
            name = "";
            email = "";
            address = "";
            open = false;
            onClientCreated();
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
        <Button>
            <PlusIcon class="mr-2 h-4 w-4" />
            Create Client
        </Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <UserPlusIcon class="h-5 w-5 text-primary" />
                Create New Client
            </Dialog.Title>
            <Dialog.Description>
                Add a new client to your account. Fill in all the required
                fields.
            </Dialog.Description>
        </Dialog.Header>
        <form onsubmit={handleSubmit}>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="name">Name</Label>
                    <div class="relative">
                        <UserIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Input
                            id="name"
                            type="text"
                            placeholder="Acme Corp"
                            required
                            bind:value={name}
                            class="pl-9"
                        />
                    </div>
                </div>
                <div class="grid gap-2">
                    <Label for="email">Email</Label>
                    <div class="relative">
                        <MailIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Input
                            id="email"
                            type="email"
                            placeholder="contact@acme.com"
                            required
                            bind:value={email}
                            class="pl-9"
                        />
                    </div>
                </div>
                <div class="grid gap-2">
                    <Label for="address">Address (Optional)</Label>
                    <div class="relative">
                        <MapPinIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Textarea
                            id="address"
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
                        Creating...
                    {:else}
                        Create Client
                    {/if}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
