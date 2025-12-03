<script lang="ts">
    /**
     * ViewInvoiceDialog Component
     */
    import type { Invoice } from "$lib/utils/types";
    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import EyeIcon from "@tabler/icons-svelte/icons/eye";
    import FileInvoiceIcon from "@tabler/icons-svelte/icons/file-invoice";
    import CalendarIcon from "@tabler/icons-svelte/icons/calendar";
    import CurrencyDollarIcon from "@tabler/icons-svelte/icons/currency-dollar";

    let { invoice }: { invoice: Invoice } = $props();
    let open = $state(false);

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleDateString();
    }

    function formatPrice(price: number, currency: string) {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: currency,
        }).format(price);
    }

    function getStatusVariant(status: string) {
        switch (status) {
            case "paid":
                return "default";
            case "sent":
                return "secondary";
            case "draft":
                return "outline";
            case "cancelled":
                return "destructive";
            default:
                return "secondary";
        }
    }
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger>
        <Button variant="ghost" size="sm">
            <EyeIcon class="h-4 w-4" />
        </Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <EyeIcon class="h-5 w-5 text-primary" />
                Invoice Details #{invoice.id}
            </Dialog.Title>
            <Dialog.Description>
                View detailed information about this invoice
            </Dialog.Description>
        </Dialog.Header>
        <div class="grid gap-4 py-4">
            <div class="flex items-center justify-between">
                <span class="text-sm text-muted-foreground">Status:</span>
                <Badge variant={getStatusVariant(invoice.status)}>
                    {invoice.status.toUpperCase()}
                </Badge>
            </div>

            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <CalendarIcon class="h-4 w-4" />
                    <span class="font-medium">Due Date</span>
                </div>
                <p class="text-base pl-6">{formatDate(invoice.due_date)}</p>
            </div>

            <div class="grid gap-2">
                <div
                    class="flex items-center gap-2 text-sm text-muted-foreground"
                >
                    <CurrencyDollarIcon class="h-4 w-4" />
                    <span class="font-medium">Total Amount</span>
                </div>
                <p class="text-lg font-bold pl-6">
                    {formatPrice(invoice.total_amount, invoice.currency)}
                </p>
            </div>

            {#if invoice.is_recurring}
                <div class="grid gap-2">
                    <div
                        class="flex items-center gap-2 text-sm text-muted-foreground"
                    >
                        <FileInvoiceIcon class="h-4 w-4" />
                        <span class="font-medium">Recurring</span>
                    </div>
                    <p class="text-base pl-6 capitalize">
                        {invoice.recurring_interval || "Not set"}
                    </p>
                </div>
            {/if}

            <div class="border-t pt-4">
                <h4 class="text-sm font-medium mb-3">Invoice Items</h4>
                <div class="space-y-2">
                    {#each invoice.items as item}
                        <div
                            class="flex justify-between items-center p-2 bg-muted/50 rounded"
                        >
                            <div>
                                <p class="font-medium">
                                    Product ID: {item.product_id}
                                </p>
                                <p class="text-sm text-muted-foreground">
                                    Quantity: {item.quantity}
                                </p>
                            </div>
                            <p class="font-semibold">
                                {formatPrice(
                                    item.unit_price * item.quantity,
                                    invoice.currency,
                                )}
                            </p>
                        </div>
                    {/each}
                </div>
            </div>

            <div class="text-sm text-muted-foreground pt-2 border-t">
                <p>Created: {formatDate(invoice.created_at || "")}</p>
            </div>
        </div>
    </Dialog.Content>
</Dialog.Root>
