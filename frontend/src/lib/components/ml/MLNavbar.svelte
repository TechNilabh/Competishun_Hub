<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	onMount(() => {
		const items = document.querySelectorAll('.nav-item');
		const underline = document.getElementById('nav-underline');

		function updateUnderline() {
			const active = document.querySelector('.active-link') as HTMLElement | null;
			if (!active || !underline) return;

			const rect = active.getBoundingClientRect();
			const parentRect = active.parentElement?.getBoundingClientRect();

			const offsetX = parentRect ? rect.left - parentRect.left : rect.left;

			underline.style.width = rect.width + 'px';
			underline.style.transform = `translateX(${offsetX}px)`;
		}

		updateUnderline();
		window.addEventListener('resize', updateUnderline);
		items.forEach(i => i.addEventListener('click', () => setTimeout(updateUnderline, 120)));
	});
</script>

<nav class="relative flex flex-wrap gap-6 border-b border-gray-800 pb-4 text-sm md:text-md lg:text-lg font-medium overflow-x-auto scrollbar-hide">

	<!-- Animated underline -->
	<div class="absolute bottom-0 left-0 h-[2px] bg-indigo-500 transition-all duration-300 ease-out" id="nav-underline"></div>

	<a
		href="/round/2/ml"
		class="nav-item px-2 py-1 transition-all duration-200 hover:text-indigo-500"
		class:active-link={$page.url.pathname.endsWith('/ml')}
	>Instructions</a>

	<a
		href="/round/2/ml/dataset"
		class="nav-item px-2 py-1 transition-all duration-200 hover:text-indigo-500"
		class:active-link={$page.url.pathname.includes('/dataset')}
	>Dataset</a>

	<a
		href="/round/2/ml/submission"
		class="nav-item px-2 py-1 transition-all duration-200 hover:text-indigo-500"
		class:active-link={$page.url.pathname.includes('/submission')}
	>Submission</a>

	<a
		href="/round/2/ml/leaderboard"
		class="nav-item px-2 py-1 transition-all duration-200 hover:text-indigo-500"
		class:active-link={$page.url.pathname.includes('/leaderboard')}
	>Leaderboard</a>
</nav>

<style>
	.scrollbar-hide::-webkit-scrollbar { display: none; }
	.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

	.nav-item {
		position: relative;
		color: #c9c9c9;
		cursor: pointer;
		white-space: nowrap;
		font-weight: 500;
	}

	.active-link {
		color: #966dff;
	}
</style>


