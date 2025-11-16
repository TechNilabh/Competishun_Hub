<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '$lib/components/ui/button';
	import { slide, fade } from 'svelte/transition';

	let track = 'student';
	let openId: number | null = null;

	const rounds = [
		{
			id: 1,
			title: 'Round 1 — Quiz',
			description: 'A timed multiple-choice quiz that evaluates foundational CS knowledge, reasoning, and problem-solving speed.',
			path: '/round/1'
		},
		{
			id: 2,
			title: 'Round 2 — Coding',
			description: 'A two-stage coding assessment featuring a structured coding problem and an ML submission challenge.',
			path: '/round/2'
		}
	];
</script>

<section id="round" class="relative mx-auto max-w-7xl px-6 md:px-8 py-20 animate-fadeIn">

	<!-- Heading -->
	<div class="text-center mb-16">
		<h1 class="text-4xl md:text-5xl font-extrabold text-[var(--text-primary)] tracking-tight mb-3 relative inline-block">
			Problem Statement
			<span class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-32 h-[3px] bg-indigo-500 rounded-full"></span>
		</h1>

		<p class="text-lg text-[var(--text-secondary)] max-w-2xl mx-auto leading-relaxed">
			The competition consists of two stages designed to evaluate your concepts, logic, coding ability, and ML intuition.
		</p>
	</div>

	<!-- Timeline / Rounds List -->
	<div class="max-w-3xl mx-auto">

		<h2 class="text-2xl font-semibold mb-8 text-[var(--text-primary)]">
			Competition Rounds
		</h2>

		<div class="relative space-y-10">
			
			{#each rounds as r, i}
				<div class="relative group">

					
					<!-- Card -->
					<div
						in:slide={{ duration: 300 }}
						class="p-6 rounded-xl border border-[var(--border)] bg-[var(--card-bg)]
							   shadow-lg group-hover:shadow-indigo-500/20 transition-all duration-200"
					>
						<h3 class="text-xl font-bold text-[var(--text-primary)] mb-2">
							{r.title}
						</h3>

						<p class="text-[var(--text-secondary)] text-sm leading-relaxed mb-4">
							{r.description}
						</p>

						<Button
							class="bg-indigo-500 hover:bg-indigo-600 text-white font-semibold"
							on:click={() => goto(r.path)}
						>
							Go to Round {r.id}
						</Button>
					</div>
				</div>
			{/each}
		</div>
	</div>
</section>

<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(12px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.animate-fadeIn {
		animation: fadeIn 0.4s ease-out;
	}
</style>
