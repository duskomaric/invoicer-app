<script lang="ts">
    /**
     * EditInvoiceDialog Component
     */
    import { api } from "$lib/utils/api";
    import type {
        Invoice,
        InvoiceUpdate,
        Client,
        Product,
    } from "$lib/utils/types";
    import { toast } from "svelte-sonner";

    import * as Dialog from "$lib/components/ui/dialog";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";

    import EditIcon from "@tabler/icons-svelte/icons/edit";
    import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";
    import PlusIcon from "@tabler/icons-svelte/icons/plus";
    import TrashIcon from "@tabler/icons-svelte/icons/trash";

    let {
        invoice,
        onInvoiceUpdated,
    }: {
        invoice: Invoice;
        onInvoiceUpdated: () => void;
    } = $props();

    let open = $state(false);
    let clientId = $state(String(invoice.client_id));
    let dueDate = $state(invoice.due_date.split("T")[0]);
    let status = $state(invoice.status);
    let isRecurring = $state(invoice.is_recurring);
    let recurringInterval = $state(invoice.recurring_interval || "");

    // Invoice items
    type InvoiceItemRow = {
        productId: string;
        quantity: string;
        unitPrice: string;
        currency: string;
    };

    // Initialize items from invoice
    let items = $state<InvoiceItemRow[]>(
        invoice.items && invoice.items.length > 0
            ? invoice.items.map((item) => ({
                  productId: String(item.product_id),
                  quantity: String(item.quantity),
                  unitPrice: String(item.unit_price),
                  currency: invoice.currency, // Assuming items share invoice currency for now
              }))
            : [
                  {
                      productId: "",
                      quantity: "1",
                      unitPrice: "",
                      currency: "USD",
                  },
              ],
    );

    let error = $state("");
    let loading = $state(false);

    // Data for dropdowns
    let clients = $state<Client[]>([]);
    let products = $state<Product[]>([]);

    async function loadClients() {
        try {
            const query = new URLSearchParams({ limit: "100" });
            const res = await api.get<{ data: Client[] }>(
                `/api/v1/clients/?${query.toString()}`,
            );
            clients = res.data;

            // Ensure current client is in the list
            if (
                invoice.client &&
                !clients.find((c) => c.id === invoice.client_id)
            ) {
                clients = [invoice.client, ...clients];
            }
        } catch (err) {
            console.error("Failed to load clients", err);
        }
    }

    async function loadProducts() {
        try {
            const query = new URLSearchParams({ limit: "100" });
            const res = await api.get<{ data: Product[] }>(
                `/api/v1/products/?${query.toString()}`,
            );
            products = res.data;
        } catch (err) {
            console.error("Failed to load products", err);
        }
    }

    function handleProductChange(index: number) {
        const productId = items[index].productId;
        if (productId) {
            const product = products.find((p) => String(p.id) === productId);
            if (product) {
                items[index].unitPrice = String(product.price);
                items[index].currency = product.currency;
            }
        }
    }

    // Load data when dialog opens
    $effect(() => {
        if (open) {
            loadClients();
            loadProducts();
            // Reset form state to invoice values
            clientId = String(invoice.client_id);
            dueDate = invoice.due_date.split("T")[0];
            status = invoice.status;
            isRecurring = invoice.is_recurring;
            recurringInterval = invoice.recurring_interval || "";
            items =
                invoice.items && invoice.items.length > 0
                    ? invoice.items.map((item) => ({
                          productId: String(item.product_id),
                          quantity: String(item.quantity),
                          unitPrice: String(item.unit_price),
                          currency: invoice.currency,
                      }))
                    : [
                          {
                              productId: "",
                              quantity: "1",
                              unitPrice: "",
                              currency: "USD",
                          },
                      ];
        }
    });

    function addItem() {
        items = [
            ...items,
            { productId: "", quantity: "1", unitPrice: "", currency: "USD" },
        ];
    }

    function removeItem(index: number) {
        items = items.filter((_, i) => i !== index);
    }

    async function handleSubmit(e: Event) {
        e.preventDefault();
        loading = true;
        error = "";

        try {
            if (!clientId) {
                error = "Please select a client";
                loading = false;
                return;
            }

            if (items.length === 0) {
                error = "Please add at least one item";
                loading = false;
                return;
            }

            for (const item of items) {
                if (!item.productId || !item.unitPrice) {
                    error =
                        "Please select a product and enter a price for all items";
                    loading = false;
                    return;
                }
            }

            const invoiceUpdate: any = {
                client_id: parseInt(clientId),
                status,
                due_date: new Date(dueDate).toISOString(),
                is_recurring: isRecurring,
                recurring_interval:
                    isRecurring && recurringInterval ? recurringInterval : null,
                items: items.map((item) => ({
                    product_id: parseInt(item.productId),
                    quantity: parseInt(item.quantity),
                    unit_price: parseFloat(item.unitPrice),
                })),
            };

            await api.put(`/api/v1/invoices/${invoice.id}`, invoiceUpdate);
            toast.info(`Invoice #${invoice.id} updated successfully!`);

            open = false;
            onInvoiceUpdated();
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

    let loaded = $state(false);

    $effect(() => {
        if (open) {
            // Set loaded to true after a tick?
            setTimeout(() => (loaded = true), 500);
        } else {
            loaded = false;
        }
    });
</script>

<Dialog.Root bind:open>
    <Dialog.Trigger>
        <Button variant="ghost" size="sm">
            <EditIcon class="h-4 w-4" />
        </Button>
    </Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <Dialog.Header>
            <Dialog.Title class="flex items-center gap-2">
                <EditIcon class="h-5 w-5 text-primary" />
                Edit Invoice
            </Dialog.Title>
            <Dialog.Description>Update invoice details.</Dialog.Description>
        </Dialog.Header>
        <form onsubmit={handleSubmit}>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="edit-client">Client</Label>
                    <select
                        id="edit-client"
                        bind:value={clientId}
                        required
                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                    >
                        <option value="">Select client...</option>
                        {#each clients as client}
                            <option value={String(client.id)}
                                >{client.name}</option
                            >
                        {/each}
                    </select>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div class="grid gap-2">
                        <Label for="edit-status">Status</Label>
                        <select
                            id="edit-status"
                            bind:value={status}
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                        >
                            <option value="draft">Draft</option>
                            <option value="sent">Sent</option>
                            <option value="paid">Paid</option>
                            <option value="cancelled">Cancelled</option>
                        </select>
                    </div>
                    <div class="grid gap-2">
                        <Label for="edit-due_date">Due Date</Label>
                        <Input
                            id="edit-due_date"
                            type="date"
                            required
                            bind:value={dueDate}
                        />
                    </div>
                </div>

                <div class="border-t pt-4">
                    <div class="flex justify-between items-center mb-3">
                        <h4 class="text-sm font-medium">Invoice Items</h4>
                        <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onclick={addItem}
                        >
                            <PlusIcon class="h-4 w-4 mr-1" />
                            Add Item
                        </Button>
                    </div>

                    <div class="space-y-4">
                        {#each items as item, index}
                            <div
                                class="grid gap-3 p-3 border rounded-md relative bg-muted/20"
                            >
                                {#if items.length > 1}
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="icon"
                                        class="absolute right-2 top-2 h-6 w-6 text-muted-foreground hover:text-destructive"
                                        onclick={() => removeItem(index)}
                                    >
                                        <TrashIcon class="h-4 w-4" />
                                    </Button>
                                {/if}

                                <div class="grid gap-2 pr-8">
                                    <Label>Product/Service</Label>
                                    <select
                                        bind:value={item.productId}
                                        onchange={() =>
                                            handleProductChange(index)}
                                        required
                                        class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                                    >
                                        <option value=""
                                            >Select product...</option
                                        >
                                        {#each products as product}
                                            <option value={String(product.id)}>
                                                {product.name} - {product.currency}
                                                {product.price}
                                            </option>
                                        {/each}
                                    </select>
                                </div>

                                <div class="grid grid-cols-3 gap-2">
                                    <div class="grid gap-2">
                                        <Label>Quantity</Label>
                                        <Input
                                            type="number"
                                            min="1"
                                            required
                                            bind:value={item.quantity}
                                        />
                                    </div>
                                    <div class="grid gap-2">
                                        <Label>Unit Price</Label>
                                        <Input
                                            type="number"
                                            step="0.01"
                                            min="0"
                                            required
                                            bind:value={item.unitPrice}
                                        />
                                    </div>
                                    <div class="grid gap-2">
                                        <Label>Currency</Label>
                                        <select
                                            bind:value={item.currency}
                                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                                        >
                                            <option value="USD">USD</option>
                                            <option value="EUR">EUR</option>
                                            <option value="GBP">GBP</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <div class="flex items-center gap-2 mt-2">
                    <input
                        type="checkbox"
                        id="edit-is_recurring"
                        bind:checked={isRecurring}
                        class="h-4 w-4"
                    />
                    <Label for="edit-is_recurring" class="cursor-pointer"
                        >Recurring Invoice</Label
                    >
                </div>
                {#if isRecurring}
                    <div class="grid gap-2">
                        <Label for="edit-recurring_interval"
                            >Recurring Interval</Label
                        >
                        <select
                            id="edit-recurring_interval"
                            bind:value={recurringInterval}
                            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
                        >
                            <option value="">Select interval...</option>
                            <option value="monthly">Monthly</option>
                            <option value="quarterly">Quarterly</option>
                            <option value="yearly">Yearly</option>
                        </select>
                    </div>
                {/if}
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
                        Update Invoice
                    {/if}
                </Button>
            </Dialog.Footer>
        </form>
    </Dialog.Content>
</Dialog.Root>
