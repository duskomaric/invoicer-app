<script lang="ts">
	import { api } from "$lib/utils/api";
	import type { User } from "$lib/utils/types";
	import * as AlertDialog from "$lib/components/ui/alert-dialog";
	import { Button } from "$lib/components/ui/button";
	import { toast } from "svelte-sonner";
	import TrashIcon from "@tabler/icons-svelte/icons/trash";

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
			await Promise.all(
				userArray.map((user) => api.delete(`/api/v1/users/${user.id}`)),
			);

			open = false;
			const message =
				userCount === 1
					? `User "${userArray[0].full_name}" deleted successfully!`
					: `${userCount} users deleted successfully!`;
			toast.warning(message);
			onUsersDeleted();
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

<AlertDialog.Root bind:open>
	<AlertDialog.Trigger>
		{#if variant === "bulk"}
			<Button variant="destructive" size="sm">Delete Selected</Button>
		{:else}
			<TrashIcon class="h-4 w-4 text-red-600 cursor-pointer" />
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
