<script lang="ts">
	import type { User } from "$lib/utils/types";
	import * as Dialog from "$lib/components/ui/dialog";
	import { Button } from "$lib/components/ui/button";
	import { Badge } from "$lib/components/ui/badge";
	import { Separator } from "$lib/components/ui/separator";
	import UserIcon from "@tabler/icons-svelte/icons/user";
	import MailIcon from "@tabler/icons-svelte/icons/mail";
	import IdBadgeIcon from "@tabler/icons-svelte/icons/id-badge";
	import CheckIcon from "@tabler/icons-svelte/icons/check";
	import XIcon from "@tabler/icons-svelte/icons/x";
	import EyeFilledIcon from "@tabler/icons-svelte/icons/eye-filled";

	let { user }: { user: User } = $props();
</script>

<Dialog.Root>
	<Dialog.Trigger>
		<Button variant="ghost" size="sm" class="h-8 w-8 p-0">
			<span class="sr-only">View user</span>
			<EyeFilledIcon class="h-4 w-4" />
		</Button>
	</Dialog.Trigger>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header
			class="flex flex-row items-center gap-4 space-y-0 pb-4 border-b"
		>
			<div
				class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10"
			>
				<UserIcon class="h-6 w-6 text-primary" />
			</div>
			<div class="flex-1">
				<Dialog.Title class="text-lg font-semibold"
					>{user.full_name}</Dialog.Title
				>
				<Dialog.Description class="text-sm text-muted-foreground">
					User Profile
				</Dialog.Description>
			</div>
			<Badge
				variant={user.is_active ? "default" : "secondary"}
				class="ml-auto"
			>
				{user.is_active ? "Active" : "Inactive"}
			</Badge>
		</Dialog.Header>

		<div class="grid gap-6 py-6">
			<div class="grid grid-cols-[24px_1fr] items-start gap-4">
				<IdBadgeIcon class="h-5 w-5 text-muted-foreground mt-0.5" />
				<div class="space-y-1">
					<p class="text-sm font-medium leading-none">User ID</p>
					<p class="text-sm text-muted-foreground font-mono">
						{user.id}
					</p>
				</div>
			</div>

			<div class="grid grid-cols-[24px_1fr] items-start gap-4">
				<MailIcon class="h-5 w-5 text-muted-foreground mt-0.5" />
				<div class="space-y-1">
					<p class="text-sm font-medium leading-none">
						Email Address
					</p>
					<p class="text-sm text-muted-foreground">{user.email}</p>
				</div>
			</div>

			<div class="grid grid-cols-[24px_1fr] items-start gap-4">
				{#if user.is_active}
					<CheckIcon class="h-5 w-5 text-green-600 mt-0.5" />
				{:else}
					<XIcon class="h-5 w-5 text-red-600 mt-0.5" />
				{/if}
				<div class="space-y-1">
					<p class="text-sm font-medium leading-none">
						Account Status
					</p>
					<p class="text-sm text-muted-foreground">
						{user.is_active
							? "This account is active and has full access."
							: "This account is currently inactive."}
					</p>
				</div>
			</div>
		</div>

		<Dialog.Footer>
			<Dialog.Close>
				<Button variant="outline" class="w-full sm:w-auto">Close</Button
				>
			</Dialog.Close>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>
