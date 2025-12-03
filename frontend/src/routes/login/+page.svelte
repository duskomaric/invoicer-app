<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    import LoginForm from "$lib/components/login-form.svelte";

    // Check if user is already logged in
    onMount(() => {
        const token = localStorage.getItem("token");
        if (token) {
            // User is logged in, redirect to dashboard/users
            goto("/users");
        }
    });
</script>

<div
    class="flex min-h-svh flex-col items-center justify-center gap-6 bg-muted p-6 md:p-10"
>
    <div class="flex w-full max-w-sm flex-col gap-6">
        <a href="/" class="flex items-center gap-2 self-center font-medium">
            <div
                class="flex h-6 w-6 items-center justify-center rounded-md bg-primary text-primary-foreground"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="size-4"
                >
                    <path d="M3 3v18h18" />
                    <path d="m19 9-5 5-4-4-3 3" />
                </svg>
            </div>
            Acme Inc.
        </a>
        <LoginForm />
    </div>
</div>
