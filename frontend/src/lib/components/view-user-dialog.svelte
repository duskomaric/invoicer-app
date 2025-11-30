<script lang="ts">
	import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Field, FieldLabel } from "$lib/components/ui/field/index.js";
	import type { User } from "$lib/components/users-table.svelte";

	let { user }: { user: User } = $props();
</script>

<Dialog.Root>
	<Dialog.Trigger>
		<Button variant="ghost" size="sm">View</Button>
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title>User Details</Dialog.Title>
			<Dialog.Description>
				View user information.
			</Dialog.Description>
		</Dialog.Header>
		<div class="grid gap-4 py-4">
			<div class="grid gap-1">
				<span class="text-sm font-medium text-muted-foreground">ID</span>
				<p class="text-sm font-medium">{user.id}</p>
			</div>
			<div class="grid gap-1">
				<span class="text-sm font-medium text-muted-foreground">Email</span>
				<p class="text-sm font-medium">{user.email}</p>
			</div>
			<div class="grid gap-1">
				<span class="text-sm font-medium text-muted-foreground">Full Name</span>
				<p class="text-sm font-medium">{user.full_name}</p>
			</div>
			<div class="grid gap-1">
				<span class="text-sm font-medium text-muted-foreground">Status</span>
				<p class="text-sm font-medium {user.is_active ? 'text-green-600' : 'text-red-600'}">
					{user.is_active ? 'Active' : 'Inactive'}
				</p>
			</div>
		</div>
		<Dialog.Footer>
			<Dialog.Close>
				<Button variant="outline">Close</Button>
			</Dialog.Close>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
