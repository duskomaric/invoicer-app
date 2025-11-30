<script lang="ts">
	import { API_BASE_URL } from "$lib/config";
	import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import type { User } from "$lib/components/users-table.svelte";
	import { toast } from "svelte-sonner";

	let {
		users,
		onUsersDeleted,
		variant = "single",
	}: {
		users: User | User[];
		onUsersDeleted: () => void;
		variant?: "single" | "bulk";
	} = $props();

	let open = $state(false);
	let error = $state("");
	let loading = $state(false);

	const userArray = $derived(Array.isArray(users) ? users : [users]);
	const userCount = $derived(userArray.length);
	const displayText = $derived(
		userCount === 1
			? `user "${userArray[0].full_name}"`
			: `${userCount} users`,
	);

	async function handleDelete() {
		loading = true;
		error = "";

		try {
			const token = localStorage.getItem("token");
			if (!token) {
				throw new Error("Not authenticated");
			}

			// Delete all users
			const deletePromises = userArray.map((user) =>
				fetch(`${API_BASE_URL}/api/v1/users/${user.id}`, {
					method: "DELETE",
					headers: {
						Authorization: `Bearer ${token}`,
					},
				}),
			);

			const results = await Promise.all(deletePromises);

			// Check if any failed
			const failedResults = results.filter((res) => !res.ok);
			if (failedResults.length > 0) {
				throw new Error(
					`Failed to delete ${failedResults.length} user(s)`,
				);
			}

			open = false;
			const message =
				userCount === 1
					? `User "${userArray[0].full_name}" deleted successfully!`
					: `${userCount} users deleted successfully!`;
			toast.warning(message);
			onUsersDeleted();
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<AlertDialog.Root bind:open>
	<AlertDialog.Trigger>
		{#if variant === "bulk"}
			<Button variant="destructive" size="sm">Delete Selected</Button>
		{:else}
			<Button variant="ghost" size="sm">Delete</Button>
		{/if}
	</AlertDialog.Trigger>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete {displayText}.
			</AlertDialog.Description>
		</AlertDialog.Header>
		{#if error}
			<div class="text-red-500 text-sm">{error}</div>
		{/if}
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action onclick={handleDelete} disabled={loading}>
				{loading ? "Deleting..." : "Delete"}
			</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
