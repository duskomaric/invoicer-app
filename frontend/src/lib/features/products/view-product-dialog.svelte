<script lang="ts">
    /**
     * ViewProductDialog Component
     */
    import type { Product } from "$lib/utils/types";
    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import EyeIcon from "@tabler/icons-svelte/icons/eye";
    import PackageIcon from "@tabler/icons-svelte/icons/package";
    import TextIcon from "@tabler/icons-svelte/icons/file-description";
    import CurrencyDollarIcon from "@tabler/icons-svelte/icons/currency-dollar";
    import CalendarIcon from "@tabler/icons-svelte/icons/calendar";

    let { product }: { product: Product } = $props();
    let open = $state(false);

    function formatDate(dateString?: string) {
        if (!dateString) return "N/A";
        return new Date(dateString).toLocaleDateString();
    }

    function formatPrice(price: number, currency: string) {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: currency,
        }).format(price);
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
                Product Details
            </Dialog.Title>
            <Dialog.Description>
                View detailed information about {product.name}
            </Dialog.Description>
        </Dialog.Header>
        <div class="grid gap-4 py-4">
            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <PackageIcon class="h-4 w-4" />
                    <span class="font-medium">Name</span>
                </div>
                <p class="text-base pl-6">{product.name}</p>
            </div>
            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <TextIcon class="h-4 w-4" />
                    <span class="font-medium">Description</span>
                </div>
                <p class="text-base pl-6">
                    {product.description || "No description provided"}
                </p>
            </div>
            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <CurrencyDollarIcon class="h-4 w-4" />
                    <span class="font-medium">Price</span>
                </div>
                <p class="text-base pl-6 font-semibold">
                    {formatPrice(product.price, product.currency)}
                </p>
            </div>
            <div class="grid gap-2 pt-2 border-t">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <CalendarIcon class="h-4 w-4" />
                    <span class="font-medium">Created</span>
                </div>
                <p class="text-sm pl-6">{formatDate(product.created_at)}</p>
            </div>
        </div>
    </Dialog.Content>
</Dialog.Root>
