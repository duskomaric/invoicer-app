<script lang="ts">
	import { API_BASE_URL } from "$lib/config";
	import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Input } from "$lib/components/ui/input/index.js";
	import { Field, FieldLabel } from "$lib/components/ui/field/index.js";
	import { toast } from "svelte-sonner";

	let { onUserCreated }: { onUserCreated: () => void } = $props();

	let open = $state(false);
	let email = $state("");
	let fullName = $state("");
	let password = $state("");
	let error = $state("");
	let loading = $state(false);

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		error = "";

		try {
			const token = localStorage.getItem("token");
			if (!token) {
				throw new Error("Not authenticated");
			}

			const res = await fetch(`${API_BASE_URL}/api/v1/users/`, {
				method: "POST",
				headers: {
					Authorization: `Bearer ${token}`,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					email,
					full_name: fullName,
					password,
				}),
			});

			if (!res.ok) {
				const data = await res.json();
				throw new Error(data.detail || "Failed to create user");
			}

			// Show success toast before resetting
			toast.info(`User "${fullName}" created successfully!`);

			// Reset form
			email = "";
			fullName = "";
			password = "";
			open = false;
			onUserCreated();
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<Dialog.Root bind:open>
	<Dialog.Trigger>
		<Button>Create User</Button>
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title>Create New User</Dialog.Title>
			<Dialog.Description>
				Add a new user to the system. Fill in all the required fields.
			</Dialog.Description>
		</Dialog.Header>
		<form onsubmit={handleSubmit}>
			<div class="grid gap-4 py-4">
				<Field>
					<FieldLabel for="email">Email</FieldLabel>
					<Input
						id="email"
						type="email"
						required
						bind:value={email}
					/>
				</Field>
				<Field>
					<FieldLabel for="full_name">Full Name</FieldLabel>
					<Input
						id="full_name"
						type="text"
						required
						bind:value={fullName}
					/>
				</Field>
				<Field>
					<FieldLabel for="password">Password</FieldLabel>
					<Input
						id="password"
						type="password"
						required
						bind:value={password}
					/>
				</Field>
				{#if error}
					<div class="text-red-500 text-sm">{error}</div>
				{/if}
			</div>
			<Dialog.Footer>
				<Button type="submit" disabled={loading}>
					{loading ? "Creating..." : "Create User"}
				</Button>
			</Dialog.Footer>
		</form>
	</Dialog.Content>
</Dialog.Root>
