<script lang="ts">
	import TrendingDownIcon from "@tabler/icons-svelte/icons/trending-down";
	import TrendingUpIcon from "@tabler/icons-svelte/icons/trending-up";
	import UsersIcon from "@tabler/icons-svelte/icons/users";
	import BuildingIcon from "@tabler/icons-svelte/icons/building";
	import PackageIcon from "@tabler/icons-svelte/icons/package";
	import FileInvoiceIcon from "@tabler/icons-svelte/icons/file-invoice";
	import { Badge } from "$lib/components/ui/badge/index.js";
	import * as Card from "$lib/components/ui/card/index.js";

	let {
		stats = {
			usersCount: 0,
			clientsCount: 0,
			productsCount: 0,
			invoicesCount: 0,
		},
	}: {
		stats?: {
			usersCount: number;
			clientsCount: number;
			productsCount: number;
			invoicesCount: number;
		};
	} = $props();
</script>

<div
	class="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card *:data-[slot=card]:shadow-xs @xl/main:grid-cols-2 @5xl/main:grid-cols-4 grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t lg:px-6"
>
	<Card.Root class="@container/card">
		<Card.Header>
			<Card.Description>Total Users</Card.Description>
			<Card.Title
				class="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums"
			>
				{stats.usersCount}
			</Card.Title>
			<Card.Action>
				<Badge variant="outline">
					<UsersIcon class="mr-1 size-3" />
					Users
				</Badge>
			</Card.Action>
		</Card.Header>
		<Card.Footer class="flex-col items-start gap-1.5 text-sm">
			<div class="line-clamp-1 flex gap-2 font-medium">
				Active system users
			</div>
		</Card.Footer>
	</Card.Root>
	<Card.Root class="@container/card">
		<Card.Header>
			<Card.Description>Total Clients</Card.Description>
			<Card.Title
				class="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums"
			>
				{stats.clientsCount}
			</Card.Title>
			<Card.Action>
				<Badge variant="outline">
					<BuildingIcon class="mr-1 size-3" />
					Clients
				</Badge>
			</Card.Action>
		</Card.Header>
		<Card.Footer class="flex-col items-start gap-1.5 text-sm">
			<div class="line-clamp-1 flex gap-2 font-medium">
				Registered clients
			</div>
		</Card.Footer>
	</Card.Root>
	<Card.Root class="@container/card">
		<Card.Header>
			<Card.Description>Total Products</Card.Description>
			<Card.Title
				class="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums"
			>
				{stats.productsCount}
			</Card.Title>
			<Card.Action>
				<Badge variant="outline">
					<PackageIcon class="mr-1 size-3" />
					Products
				</Badge>
			</Card.Action>
		</Card.Header>
		<Card.Footer class="flex-col items-start gap-1.5 text-sm">
			<div class="line-clamp-1 flex gap-2 font-medium">
				Available products/services
			</div>
		</Card.Footer>
	</Card.Root>
	<Card.Root class="@container/card">
		<Card.Header>
			<Card.Description>Total Invoices</Card.Description>
			<Card.Title
				class="@[250px]/card:text-3xl text-2xl font-semibold tabular-nums"
			>
				{stats.invoicesCount}
			</Card.Title>
			<Card.Action>
				<Badge variant="outline">
					<FileInvoiceIcon class="mr-1 size-3" />
					Invoices
				</Badge>
			</Card.Action>
		</Card.Header>
		<Card.Footer class="flex-col items-start gap-1.5 text-sm">
			<div class="line-clamp-1 flex gap-2 font-medium">
				Generated invoices
			</div>
		</Card.Footer>
	</Card.Root>
</div>
