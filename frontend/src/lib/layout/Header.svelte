<script lang="ts">
	import { cn } from '$lib/utils';
	import { AlignJustify, XIcon } from 'lucide-svelte';
	import { fly } from 'svelte/transition';
	import { theme } from '$lib/stores/theme';
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { Sun, Moon } from 'lucide-svelte';
	import logo from '$lib/imgs/AgenticAILogo.svg';
	import lock_pic from '$lib/imgs/lock.svg';
  	
	const targetDate = '2025-11-11T00:00:00+05:30';

	let isUnlocked = true;


	const menuItem = [
		{ id: 'hero', label: 'Home', href: '/' },
		{ id: 'about', label: 'About', href: '/about' },
		{ id: 'round', label: 'Problems', href: '/round', locked: !isUnlocked },
	];

	let hamburgerMenuIsOpen = false;

	function scrollToSection(event: Event, id: string, href: string) {
			event.preventDefault();
			if (window.location.pathname === href) {
				const target = document.getElementById(id);
				if (target) {
					const targetPosition = target.getBoundingClientRect().top + window.scrollY - 100;
					window.scrollTo({
						top: targetPosition,
						behavior: 'smooth'
					});
				}
			} else {
				goto(href).then(() => {
					const target = document.getElementById(id);
					if (target) {
						const targetPosition = target.getBoundingClientRect().top + window.scrollY;

						window.scrollTo({
							top: targetPosition,
							behavior: 'smooth'
						});
					}
				});
			}
		}

		function handleLinkClick() {
			hamburgerMenuIsOpen = false;
		}




	onMount(() => {
		const anchors = document.querySelectorAll('a[href^="#"]');

		const scrollHandler = (e: Event) => {
			e.preventDefault();
			const target = e.currentTarget as HTMLAnchorElement;
			const href = target.getAttribute("href");
			if (!href) return;

			const el = document.querySelector(href);
			if (el) {
				el.scrollIntoView({
					behavior: "smooth",
					block: "start"
				});
			}
		};

		anchors.forEach(a => a.addEventListener("click", scrollHandler));

		const interval = setInterval(() => {
			try {
				const todayISO = new Date().toISOString().split("T")[0];
				const targetISO = new Date(targetDate).toISOString().split("T")[0];

				if (todayISO >= targetISO) {
					isUnlocked = true;
					clearInterval(interval);
				}
			} catch {
				console.warn("Invalid targetDate:", targetDate);
			}
		}, 1000);


		return () => {
			anchors.forEach(a => a.removeEventListener("click", scrollHandler));
			clearInterval(interval);
		};
	});



	let innerWidth = 0;
		
	let currentTheme = 'dark';
	theme.subscribe(value => currentTheme = value);
</script>

<svelte:window bind:innerWidth />

<header class={cn(
	"fixed left-0 top-0 z-50 w-full backdrop-blur-md border-b bg-background/70",
)}>
	<div class="container flex items-center justify-between py-4 md:py-0 h-14 md:h-20">
		<!-- Brand -->
		<a class="text-md flex items-center" href="/">
			<img src={logo} alt="Logo" class="h-10 w-10 md:h-12 md:w-12">

		</a>

		<!-- Toggle for small screens -->
		{#if innerWidth < 768}
			<button aria-label="Toggle menu" on:click={() => hamburgerMenuIsOpen = !hamburgerMenuIsOpen}>
				{#if hamburgerMenuIsOpen}
					<XIcon strokeWidth={1.4} class="text-gray-300" />
				{:else}
					<AlignJustify strokeWidth={1.4} class="text-gray-300" />
				{/if}
			</button>
		{/if}

		<!-- Desktop -->
		<nav class={cn(
			"absolute left-0 top-full pt-2 w-full bg-background/95 backdrop-blur-lg border-b border-border/50 shadow-lg transition-all duration-300",
			{"hidden opacity-0 -translate-y-2": innerWidth < 768 && !hamburgerMenuIsOpen},
			"md:static md:bg-transparent md:backdrop-blur-none md:border-none md:shadow-none md:w-auto md:block md:opacity-100 md:translate-y-0"
			)}>
			<ul 
				in:fly={{ y: -10, duration: 200 }} 
				class="flex flex-col uppercase space-y-4 p-6 md:flex-row md:space-y-0 md:space-x-8 md:p-0 md:items-center md:normal-case"
			>
				{#each menuItem as item}
				<li>
					<a 
					href={item.href} 
					on:click={(event) => {
						if (item.locked) {
						event.preventDefault();
						return;
					}
					event.preventDefault();
					handleLinkClick();
					scrollToSection(event, item.id, item.href);
					}}
					class="hover:text-primary flex flex-row bg-transparent justify-center items-center align-middle py-3 text-lg transition-colors duration-200 md:text-base md:py-1 md:font-medium relative
							after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-0 after:h-0.5 after:bg-primary after:transition-all after:duration-300
							hover:after:w-full md:hover:after:w-[calc(100%-0.5rem)]"
					>
					{item.label}
					{#if item.locked}
						<img src={lock_pic} alt="lock" class="w-4 h-4 ml-1 dark:invert">
					{/if}
					</a>
				</li>
				{/each}
				
				<li class="mt-4 md:mt-0 md:ml-4">
				<button
					on:click={() => theme.toggle()}
					class="flex items-center justify-center gap-2 bg-gradient-to-br from-primary/10 to-secondary/20 hover:from-primary/20 hover:to-secondary/30 text-foreground px-5 py-2.5 rounded-full border border-border/50 transition-all duration-300 hover:shadow-md hover:border-primary/30 w-full md:w-auto h-10"
				>
					{#if currentTheme !== 'dark'}
					 <Sun />
					{:else}
					 <Moon />
					{/if}
				</button>
				</li>
			</ul>
		</nav>
	</div>
</header>
