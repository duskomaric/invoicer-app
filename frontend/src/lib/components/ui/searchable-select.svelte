<script lang="ts">
    import { Combobox } from "bits-ui";
    import CheckIcon from "@tabler/icons-svelte/icons/check";
    import SelectorIcon from "@tabler/icons-svelte/icons/selector";
    import { cn } from "$lib/utils";

    let {
        value = $bindable(""),
        items = [],
        placeholder = "Select item...",
        onSearch = () => {},
        class: className,
        inputValue = $bindable(""),
        onValueChange = (val: string) => {},
    }: {
        value?: string;
        items: { value: string; label: string }[];
        placeholder?: string;
        onSearch?: (term: string) => void;
        class?: string;
        inputValue?: string;
        onValueChange?: (val: string) => void;
    } = $props();

    let touched = $state(false);

    $effect(() => {
        if (inputValue && touched) {
            onSearch(inputValue);
        }
    });

    $effect(() => {
        onValueChange(value);
    });
</script>

<Combobox.Root
    type="single"
    bind:value
    bind:inputValue
    onOpenChange={(open) => {
        if (open) touched = true;
    }}
>
    <div class={cn("relative w-full", className)}>
        <Combobox.Input
            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 pr-8"
            {placeholder}
        />
        <Combobox.Trigger
            class="absolute right-0 top-0 h-full px-2 flex items-center justify-center"
        >
            <SelectorIcon class="h-4 w-4 opacity-50" />
        </Combobox.Trigger>
    </div>
    <Combobox.Portal>
        <Combobox.Content
            class="w-[--bits-combobox-anchor-width] rounded-md border bg-popover p-1 text-popover-foreground shadow-md outline-none z-50 max-h-60 overflow-y-auto"
        >
            {#each items as item (item.value)}
                <Combobox.Item
                    class="relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none data-[disabled]:pointer-events-none data-[highlighted]:bg-accent data-[highlighted]:text-accent-foreground data-[disabled]:opacity-50"
                    value={item.value}
                    label={item.label}
                >
                    {#if value === item.value}
                        <span
                            class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center"
                        >
                            <CheckIcon class="h-4 w-4" />
                        </span>
                    {/if}
                    {item.label}
                </Combobox.Item>
            {/each}
            {#if items.length === 0}
                <div class="py-6 text-center text-sm">No items found.</div>
            {/if}
        </Combobox.Content>
    </Combobox.Portal>
</Combobox.Root>
