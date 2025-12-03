<script lang="ts">
	import "./layout.css";
	import favicon from "$lib/assets/favicon.svg";
	import { Toaster } from "$lib/components/ui/sonner/index.js";
	import { ModeWatcher } from "mode-watcher";

	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";

	let { children } = $props();

	onMount(() => {
		const token = localStorage.getItem("token");
		// Allow access to login page without token
		if (!token && !$page.url.pathname.startsWith("/login")) {
			goto("/login");
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<ModeWatcher />
{@render children()}
<Toaster />
