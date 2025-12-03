<script lang="ts">
    import { page } from "$app/stores";
    import CirclePlusFilledIcon from "@tabler/icons-svelte/icons/circle-plus-filled";
    import MailIcon from "@tabler/icons-svelte/icons/mail";
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Sidebar from "$lib/components/ui/sidebar/index.js";
    import type { Icon } from "@tabler/icons-svelte";

    let { items }: { items: { title: string; url: string; icon?: Icon }[] } = $props();
</script>

<Sidebar.Group>
    <Sidebar.GroupContent class="flex flex-col gap-2">

        <!-- Quick actions -->
        <Sidebar.Menu>
            <Sidebar.MenuItem class="flex items-center gap-2">
                <Sidebar.MenuButton
                        class="bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground active:bg-primary/90 active:text-primary-foreground min-w-8 duration-200 ease-linear"
                        tooltipContent="Quick create"
                >
                    <CirclePlusFilledIcon />
                    <span>Create Invoice</span>
                </Sidebar.MenuButton>

                <Button size="icon" class="size-8 group-data-[collapsible=icon]:opacity-0" variant="outline">
                    <MailIcon />
                    <span class="sr-only">Inbox</span>
                </Button>
            </Sidebar.MenuItem>
        </Sidebar.Menu>

        <!-- Main nav -->
        <Sidebar.Menu>
            {#each items as item (item.title)}
                <Sidebar.MenuItem>
                    <Sidebar.MenuButton tooltipContent={item.title}>
                        {#snippet child({ props })}
                            <a
                                    href={item.url}
                                    {...props}
                                    class="flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-accent hover:text-accent-foreground"
                                    class:bg-accent={$page.url.pathname === item.url}
                                    class:text-accent-foreground={$page.url.pathname === item.url}
                                    class:font-medium={$page.url.pathname === item.url}
                            >
                                {#if item.icon}
                                    <item.icon />
                                {/if}
                                <span>{item.title}</span>
                            </a>

                        {/snippet}
                    </Sidebar.MenuButton>
                </Sidebar.MenuItem>
            {/each}
        </Sidebar.Menu>

    </Sidebar.GroupContent>
</Sidebar.Group>
