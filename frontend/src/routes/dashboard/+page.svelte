<script lang="ts">
	import { onMount } from "svelte";
	import { api } from "$lib/utils/api";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import AppSidebar from "$lib/components/app-sidebar.svelte";
	import SiteHeader from "$lib/components/site-header.svelte";
	import SectionCards from "$lib/components/section-cards.svelte";

	let stats = $state({
		usersCount: 0,
		clientsCount: 0,
		productsCount: 0,
		invoicesCount: 0,
	});

	onMount(async () => {
		try {
			const res = await api.get<{
				users_count: number;
				clients_count: number;
				products_count: number;
				invoices_count: number;
				invoices_status_counts: {
					all_count: number;
					draft_count: number;
					sent_count: number;
					paid_count: number;
					cancelled_count: number;
				};
			}>("/api/v1/stats/");

			stats = {
				usersCount: res.users_count,
				clientsCount: res.clients_count,
				productsCount: res.products_count,
				invoicesCount: res.invoices_count,
			};
		} catch (error) {
			console.error("Failed to fetch dashboard stats:", error);
		}
	});
</script>

<Sidebar.Provider
	style="--sidebar-width: calc(var(--spacing) * 72); --header-height: calc(var(--spacing) * 12);"
>
	<AppSidebar variant="inset" />
	<Sidebar.Inset>
		<SiteHeader />
		<div class="flex flex-1 flex-col">
			<div class="@container/main flex flex-1 flex-col gap-2">
				<div class="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
					<div class="px-4 lg:px-6">
						<h1 class="text-2xl font-bold mb-4">Dashboard</h1>
					</div>
					<SectionCards {stats} />
				</div>
			</div>
		</div>
	</Sidebar.Inset>
</Sidebar.Provider>
