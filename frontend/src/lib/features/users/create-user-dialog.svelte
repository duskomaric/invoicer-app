<script lang="ts">
	/**
	 * CreateUserDialog Component
	 *
	 * A modal dialog for creating new users.
	 * Uses the centralized API utility for data submission.
	 */
	import { api } from "$lib/utils/api";
	import type { UserCreate } from "$lib/utils/types";
	import { toast } from "svelte-sonner";

	// UI Components
	import * as Dialog from "$lib/components/ui/dialog";
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";

	// Icons
	import UserPlusIcon from "@tabler/icons-svelte/icons/user-plus";
	import MailIcon from "@tabler/icons-svelte/icons/mail";
	import UserIcon from "@tabler/icons-svelte/icons/user";
	import LockIcon from "@tabler/icons-svelte/icons/lock";
	import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";
    import PlusIcon from "@tabler/icons-svelte/icons/plus";

	// Props
	let { onUserCreated }: { onUserCreated: () => void } = $props();

	// State
	let open = $state(false);
	let email = $state("");
	let fullName = $state("");
	let password = $state("");
	let error = $state("");
	let loading = $state(false);

	/**
	 * Handles form submission to create a new user.
	 */
	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		error = "";

		try {
			const userData: UserCreate = {
				email,
				full_name: fullName,
				password,
			};

			await api.post("/api/v1/users/", userData);

			toast.info(`User "${fullName}" created successfully!`);

			// Reset form
			email = "";
			fullName = "";
			password = "";
			open = false;
			onUserCreated();
			onUserCreated();
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
			Create User
		</Button>
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title class="flex items-center gap-2">
				<UserPlusIcon class="h-5 w-5 text-primary" />
				Create New User
			</Dialog.Title>
			<Dialog.Description>
				Add a new user to the system. Fill in all the required fields.
			</Dialog.Description>
		</Dialog.Header>
		<form onsubmit={handleSubmit}>
			<div class="grid gap-4 py-4">
				<div class="grid gap-2">
					<Label for="email">Email</Label>
					<div class="relative">
						<MailIcon
							class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
						/>
						<Input
							id="email"
							type="email"
							placeholder="name@example.com"
							required
							bind:value={email}
							class="pl-9"
						/>
					</div>
				</div>
				<div class="grid gap-2">
					<Label for="full_name">Full Name</Label>
					<div class="relative">
						<UserIcon
							class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
						/>
						<Input
							id="full_name"
							type="text"
							placeholder="John Doe"
							required
							bind:value={fullName}
							class="pl-9"
						/>
					</div>
				</div>
				<div class="grid gap-2">
					<Label for="password">Password</Label>
					<div class="relative">
						<LockIcon
							class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
						/>
						<Input
							id="password"
							type="password"
							placeholder="••••••••"
							required
							bind:value={password}
							class="pl-9"
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
						Create User
					{/if}
				</Button>
			</Dialog.Footer>
		</form>
	</Dialog.Content>
</Dialog.Root>
