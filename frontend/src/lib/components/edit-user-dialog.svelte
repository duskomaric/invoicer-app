<script lang="ts">
	import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Field, FieldLabel } from "$lib/components/ui/field/index.js";
	import type { User } from "$lib/components/users-table.svelte";
	import { toast } from "svelte-sonner";

	let { user, onUserUpdated }: { user: User; onUserUpdated: () => void } = $props();

	let open = $state(false);
	let email = $state(user.email);
	let username = $state(user.username);
	let fullName = $state(user.full_name);
	let password = $state("");
	let error = $state("");
	let loading = $state(false);

	// Update form when user prop changes
	$effect(() => {
		email = user.email;
		username = user.username;
		fullName = user.full_name;
		password = "";
	});

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		error = "";

		try {
			const token = localStorage.getItem('token');
			if (!token) {
				throw new Error('Not authenticated');
			}

			const updateData: any = {
				email,
				username,
				full_name: fullName
			};

			// Only include password if it's been set
			if (password.trim()) {
				updateData.password = password;
			}

			const res = await fetch(`http://localhost:8000/api/v1/users/${user.id}`, {
				method: 'PUT',
				headers: {
					'Authorization': `Bearer ${token}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(updateData)
			});

			if (!res.ok) {
				const data = await res.json();
				throw new Error(data.detail || 'Failed to update user');
			}

			open = false;
			toast.success(`User "${username}" updated successfully!`);
			onUserUpdated();
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Trigger>
		<Button variant="ghost" size="sm">Edit</Button>
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title>Edit User</Dialog.Title>
			<Dialog.Description>
				Update user information. Leave password blank to keep current password.
			</Dialog.Description>
		</Dialog.Header>
		<form onsubmit={handleSubmit}>
			<div class="grid gap-4 py-4">
				<Field>
					<FieldLabel for="edit-email">Email</FieldLabel>
					<Input id="edit-email" type="email" required bind:value={email} />
				</Field>
				<Field>
					<FieldLabel for="edit-username">Username</FieldLabel>
					<Input id="edit-username" type="text" required bind:value={username} />
				</Field>
				<Field>
					<FieldLabel for="edit-full_name">Full Name</FieldLabel>
					<Input id="edit-full_name" type="text" required bind:value={fullName} />
				</Field>
				<Field>
					<FieldLabel for="edit-password">Password (optional)</FieldLabel>
					<Input id="edit-password" type="password" bind:value={password} placeholder="Leave blank to keep current" />
				</Field>
				{#if error}
					<div class="text-red-500 text-sm">{error}</div>
				{/if}
			</div>
			<Dialog.Footer>
				<Button type="submit" disabled={loading}>
					{loading ? 'Updating...' : 'Update User'}
				</Button>
			</Dialog.Footer>
		</form>
	</Dialog.Content>
</Dialog.Root>
