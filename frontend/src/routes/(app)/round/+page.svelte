<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import { studentProblems, professionalProblems } from '$lib/data/problems';
	import { slide, fade } from 'svelte/transition';

	let track = 'student';
	let openId: number | null = null;

	const list = () => (track === 'student' ? studentProblems : professionalProblems);

	const toggle = (id: number) => {
		openId = openId === id ? null : id;
	};

	const rounds = [
		{
			id: 1,
			title: 'Round 1 — Quiz',
			description: 'A timed MCQ-based quiz testing core CS + logical thinking.',
			path: '/round/exams'
		},
		{
			id: 2,
			title: 'Round 2 — Coding',
			description: 'Two-part coding round with code execution + ML submission.',
			path: '/round/2'
		}
	];
</script>

<section id="round" class="relative mx-auto mt-32 max-w-7xl px-6 md:px-8">
	<div class="max-w-6xl mx-auto px-4 py-12 flex flex-col justify-center items-center">

		<!-- Heading -->
		<h1
			class="text-2xl sm:text-3xl lg:text-4xl text-center animate-fade-in text-balance lg:text-right 
      bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text font-bold leading-none tracking-tighter 
      text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40 p-10"
		>
			Problem statement
		</h1>

		<div class="w-full max-w-3xl mb-12">
			<h2 class="text-xl font-semibold mb-6">Competition Rounds</h2>

			<div class="flex flex-col gap-6 border-l-2 border-neutral-300 dark:border-neutral-700 pl-6">
				{#each rounds as r}
					<div class="relative">
						<!-- Dot -->
						<div class="absolute -left-[13px] top-1 w-4 h-4 bg-[--color] rounded-full"></div>

						<h3 class="text-lg font-bold">{r.title}</h3>
						<p class="text-sm opacity-80 max-w-xl mb-3">{r.description}</p>

						<Button on:click={() => goto(r.path)}>Go to Round {r.id}</Button>
					</div>
				{/each}
			</div>
		</div>

	</div>
</section>
