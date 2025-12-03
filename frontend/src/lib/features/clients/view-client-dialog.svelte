<script lang="ts">
    /**
     * ViewClientDialog Component
     */
    import type { Client } from "$lib/utils/types";
    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import EyeIcon from "@tabler/icons-svelte/icons/eye";
    import MailIcon from "@tabler/icons-svelte/icons/mail";
    import UserIcon from "@tabler/icons-svelte/icons/user";
    import MapPinIcon from "@tabler/icons-svelte/icons/map-pin";
    import CalendarIcon from "@tabler/icons-svelte/icons/calendar";

    let { client }: { client: Client } = $props();
    let open = $state(false);

    function formatDate(dateString?: string) {
        if (!dateString) return "N/A";
        return new Date(dateString).toLocaleDateString();
    }
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger>
        <Button variant="ghost" size="sm">
            <EyeIcon class="h-4 w-4" />
        </Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[500px]">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <EyeIcon class="h-5 w-5 text-primary" />
                Client Details
            </Dialog.Title>
            <Dialog.Description>
                View detailed information about {client.name}
            </Dialog.Description>
        </Dialog.Header>
        <div class="grid gap-4 py-4">
            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <UserIcon class="h-4 w-4" />
                    <span class="font-medium">Name</span>
                </div>
                <p class="text-base pl-6">{client.name}</p>
            </div>
            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <MailIcon class="h-4 w-4" />
                    <span class="font-medium">Email</span>
                </div>
                <p class="text-base pl-6">{client.email}</p>
            </div>
            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <MapPinIcon class="h-4 w-4" />
                    <span class="font-medium">Address</span>
                </div>
                <p class="text-base pl-6">
                    {client.address || "No address provided"}
                </p>
            </div>
            <div class="grid gap-2 pt-2 border-t">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <CalendarIcon class="h-4 w-4" />
                    <span class="font-medium">Created</span>
                </div>
                <p class="text-sm pl-6">{formatDate(client.created_at)}</p>
            </div>
        </div>
    </Dialog.Content>
</Dialog.Root>
