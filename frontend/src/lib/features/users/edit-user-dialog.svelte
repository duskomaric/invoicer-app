<script lang="ts">
	/**
	 * EditUserDialog Component
	 *
	 * A modal dialog for editing existing users.
	 * Pre-fills the form with current user data and handles updates via API.
	 */
	import { api } from "$lib/utils/api";
	import type { User, UserUpdate } from "$lib/utils/types";
	import { toast } from "svelte-sonner";

	// UI Components
	import * as Dialog from "$lib/components/ui/dialog";
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";
	import { Label } from "$lib/components/ui/label";

	// Icons
	import PencilIcon from "@tabler/icons-svelte/icons/pencil";
	import MailIcon from "@tabler/icons-svelte/icons/mail";
	import UserIcon from "@tabler/icons-svelte/icons/user";
	import LockIcon from "@tabler/icons-svelte/icons/lock";
	import Loader2Icon from "@tabler/icons-svelte/icons/loader-2";

	// Props
	let { user, onUserUpdated }: { user: User; onUserUpdated: () => void } =
		$props();

	// State
	let open = $state(false);
	let email = $state(user.email);
	let fullName = $state(user.full_name);
	let password = $state("");
	let error = $state("");
	let loading = $state(false);

	/**
	 * Sync local state with user prop when it changes.
	 * This ensures the form always shows the correct data if the parent updates.
	 */
	$effect(() => {
		email = user.email;
		fullName = user.full_name;
		password = "";
	});

	/**
	 * Handles form submission to update the user.
	 * Only sends password if it has been changed.
	 */
	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		error = "";

		try {
			const updateData: UserUpdate & { password?: string } = {
				email,
				full_name: fullName,
			};

			// Only include password if it's been set
			if (password.trim()) {
				updateData.password = password;
			}

			await api.put(`/api/v1/users/${user.id}`, updateData);

			open = false;
			toast.success(`User "${fullName}" updated successfully!`);
			onUserUpdated();
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
		<Button variant="ghost" size="sm" class="h-8 w-8 p-0">
			<span class="sr-only">Edit user</span>
			<PencilIcon class="h-4 w-4" />
		</Button>
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title class="flex items-center gap-2">
				<PencilIcon class="h-5 w-5 text-primary" />
				Edit User
			</Dialog.Title>
			<Dialog.Description>
				Update user information. Leave password blank to keep current
				password.
			</Dialog.Description>
		</Dialog.Header>
		<form onsubmit={handleSubmit}>
			<div class="grid gap-4 py-4">
				<div class="grid gap-2">
					<Label for="edit-email">Email</Label>
					<div class="relative">
						<MailIcon
							class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
						/>
						<Input
							id="edit-email"
							type="email"
							required
							bind:value={email}
							class="pl-9"
						/>
					</div>
				</div>
				<div class="grid gap-2">
					<Label for="edit-full_name">Full Name</Label>
					<div class="relative">
						<UserIcon
							class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
						/>
						<Input
							id="edit-full_name"
							type="text"
							required
							bind:value={fullName}
							class="pl-9"
						/>
					</div>
				</div>
				<div class="grid gap-2">
					<Label for="edit-password">Password (optional)</Label>
					<div class="relative">
						<LockIcon
							class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground"
						/>
						<Input
							id="edit-password"
							type="password"
							bind:value={password}
							placeholder="Leave blank to keep current"
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
						Updating...
					{:else}
						Update User
					{/if}
				</Button>
			</Dialog.Footer>
		</form>
	</Dialog.Content>
</Dialog.Root>
