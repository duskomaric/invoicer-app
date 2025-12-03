<script lang="ts">
	import { onMount } from "svelte";
	import { API_BASE_URL } from "$lib/config";
	import CameraIcon from "@tabler/icons-svelte/icons/camera";
	import ChartBarIcon from "@tabler/icons-svelte/icons/chart-bar";
	import DashboardIcon from "@tabler/icons-svelte/icons/dashboard";
	import DatabaseIcon from "@tabler/icons-svelte/icons/database";
	import FileAiIcon from "@tabler/icons-svelte/icons/file-ai";
	import FileDescriptionIcon from "@tabler/icons-svelte/icons/file-description";
	import FileWordIcon from "@tabler/icons-svelte/icons/file-word";
	import FolderIcon from "@tabler/icons-svelte/icons/folder";
	import HelpIcon from "@tabler/icons-svelte/icons/help";
	import InnerShadowTopIcon from "@tabler/icons-svelte/icons/inner-shadow-top";
	import ListDetailsIcon from "@tabler/icons-svelte/icons/list-details";
	import ReportIcon from "@tabler/icons-svelte/icons/report";
	import SearchIcon from "@tabler/icons-svelte/icons/search";
	import SettingsIcon from "@tabler/icons-svelte/icons/settings";
	import UsersIcon from "@tabler/icons-svelte/icons/users";
	import BuildingsIcon from "@tabler/icons-svelte/icons/buildings";
	import PackageIcon from "@tabler/icons-svelte/icons/package";
	import FileInvoiceIcon from "@tabler/icons-svelte/icons/file-invoice";
	import NavDocuments from "./nav-documents.svelte";
	import NavMain from "./nav-main.svelte";
	import NavSecondary from "./nav-secondary.svelte";
	import NavUser from "./nav-user.svelte";
	import * as Sidebar from "$lib/components/ui/sidebar/index.js";
	import type { ComponentProps } from "svelte";

	let user = $state({
		name: "Loading...",
		email: "",
		avatar: "/avatars/shadcn.jpg",
	});

	onMount(async () => {
		const token = localStorage.getItem("token");
		if (token) {
			try {
				const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
					headers: {
						Authorization: `Bearer ${token}`,
					},
				});

				if (res.ok) {
					const userData = await res.json();
					user = {
						name: userData.full_name,
						email: userData.email,
						avatar: "/avatars/shadcn.jpg",
					};
				}
			} catch (error) {
				console.error("Failed to fetch user data:", error);
			}
		}
	});

	const data = $derived({
		user,
		navMain: [
			{
				title: "Dashboard",
				url: "/dashboard",
				icon: DashboardIcon,
			},
			{
				title: "Users",
				url: "/users",
				icon: UsersIcon,
			},
			{
				title: "Clients",
				url: "/clients",
				icon: BuildingsIcon,
			},
			{
				title: "Products",
				url: "/products",
				icon: PackageIcon,
			},
			{
				title: "Invoices",
				url: "/invoices",
				icon: FileInvoiceIcon,
			},
		],
		navClouds: [
			{
				title: "Capture",
				icon: CameraIcon,
				isActive: true,
				url: "#",
				items: [
					{
						title: "Active Proposals",
						url: "#",
					},
					{
						title: "Archived",
						url: "#",
					},
				],
			},
			{
				title: "Proposal",
				icon: FileDescriptionIcon,
				url: "#",
				items: [
					{
						title: "Active Proposals",
						url: "#",
					},
					{
						title: "Archived",
						url: "#",
					},
				],
			},
			{
				title: "Prompts",
				icon: FileAiIcon,
				url: "#",
				items: [
					{
						title: "Active Proposals",
						url: "#",
					},
					{
						title: "Archived",
						url: "#",
					},
				],
			},
		],
		navSecondary: [
			{
				title: "Settings",
				url: "#",
				icon: SettingsIcon,
			},
			{
				title: "Search",
				url: "#",
				icon: SearchIcon,
			},
		],
		documents: [
			{
				name: "Reports",
				url: "#",
				icon: ReportIcon,
			},
		],
	});

	let { ...restProps }: ComponentProps<typeof Sidebar.Root> = $props();
</script>

<Sidebar.Root collapsible="offcanvas" {...restProps}>
	<Sidebar.Header>
		<Sidebar.Menu>
			<Sidebar.MenuItem>
				<Sidebar.MenuButton
					class="data-[slot=sidebar-menu-button]:!p-1.5"
				>
					{#snippet child({ props })}
						<a href="/" {...props}>
							<InnerShadowTopIcon class="!size-5" />
							<h1 class="text-base font-semibold">Invoicer</h1
							>
						</a>
					{/snippet}
				</Sidebar.MenuButton>
			</Sidebar.MenuItem>
		</Sidebar.Menu>
	</Sidebar.Header>
	<Sidebar.Content>
		<NavMain items={data.navMain} />
		<NavDocuments items={data.documents} />
		<NavSecondary items={data.navSecondary} class="mt-auto" />
	</Sidebar.Content>
	<Sidebar.Footer>
		<NavUser user={data.user} />
	</Sidebar.Footer>
</Sidebar.Root>
