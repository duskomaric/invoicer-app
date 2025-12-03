<script lang="ts">
    /**
     * CreateProductDialog Component
     */
    import { api } from "$lib/utils/api";
    import type { ProductCreate } from "$lib/utils/types";
    import { toast } from "svelte-sonner";

    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Textarea } from "$lib/components/ui/textarea";

    import PlusIcon from "@tabler/icons-svelte/icons/plus";
    import PackageIcon from "@tabler/icons-svelte/icons/package";
    import TextIcon from "@tabler/icons-svelte/icons/file-description";
    import CurrencyDollarIcon from "@tabler/icons-svelte/icons/currency-dollar";
    import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";

    let { onProductCreated }: { onProductCreated: () => void } = $props();

    let open = $state(false);
    let name = $state("");
    let description = $state("");
    let price = $state("");
    let currency = $state("USD");
    let error = $state("");
    let loading = $state(false);

    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = "";

        try {
            const productData: ProductCreate = {
                name,
                description: description.trim() || null,
                price: parseFloat(price),
                currency,
            };

            await api.post("/api/v1/products/", productData);
            toast.info(`Product "${name}" created successfully!`);

            // Reset form
            name = "";
            description = "";
            price = "";
            currency = "USD";
            open = false;
            onProductCreated();
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
            Create Product
        </Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[425px]">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <PlusIcon class="h-5 w-5 text-primary" />
                Create New Product
            </Dialog.Title>
            <Dialog.Description>
                Add a new product or service. Fill in all the required fields.
            </Dialog.Description>
        </Dialog.Header>
        <form onsubmit={handleSubmit}>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="name">Name</Label>
                    <div class="relative">
                        <PackageIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Input
                            id="name"
                            type="text"
                            placeholder="Consulting Service"
                            required
                            bind:value={name}
                            class="pl-9"
                        />
                    </div>
                </div>
                <div class="grid gap-2">
                    <Label for="description">Description (Optional)</Label>
                    <div class="relative">
                        <TextIcon
                            class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                        />
                        <Textarea
                            id="description"
                            placeholder="Hourly consulting rate..."
                            bind:value={description}
                            class="pl-9 min-h-[80px]"
                        />
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="grid gap-2">
                        <Label for="price">Price</Label>
                        <div class="relative">
                            <CurrencyDollarIcon
                                class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
                            />
                            <Input
                                id="price"
                                type="number"
                                step="0.01"
                                min="0"
                                placeholder="150.00"
                                required
                                bind:value={price}
                                class="pl-9"
                            />
                        </div>
                    </div>
                    <div class="grid gap-2">
                        <Label for="currency">Currency</Label>
                        <select
                            id="currency"
                            bind:value={currency}
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                        >
                            <option value="USD">USD</option>
                            <option value="EUR">EUR</option>
                            <option value="GBP">GBP</option>
                        </select>
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
                        Create Product
                    {/if}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
