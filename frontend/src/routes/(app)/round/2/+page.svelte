<script lang="ts">
	import { goto } from '$app/navigation';
	import { fade, slide } from 'svelte/transition';
	import { Code, FileSpreadsheet } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';

	const parts = [
		{
			id: 1,
			title: "Part 1 — Code Execution Task",
			desc: "Write and execute your solution for the given coding problem. Your code will run against public and hidden test cases to evaluate correctness.",
			icon: Code,
			path: "/round/2/code"
		},
		{
			id: 2,
			title: "Part 2 — ML Submission",
			desc: "Download the dataset, train a model, generate submission.csv, and upload it along with your notebook. You will receive an automated accuracy and mismatch score.",
			icon: FileSpreadsheet,
			path: "/round/2/ml"
		}
	];
</script>

<section class="relative flex flex-col justify-center items-center mx-auto max-w-6xl px-6 md:px-10 mt-16 pb-40 animate-fadeIn">

	<h1
		in:fade={{ duration: 300 }}
		class="text-4xl sm:text-5xl font-extrabold text-center mb-6 tracking-tight 
		       text-[var(--text-primary)] relative inline-block"
	>
		Round 2 — Coding Challenge
		<span class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-28 h-[3px] bg-indigo-500 rounded-full"></span>
	</h1>

	<p
		in:fade={{ duration: 400 }}
		class="text-center max-w-3xl mx-auto text-lg text-[var(--text-secondary)] leading-relaxed mb-14"
	>
		This stage assesses your coding skills and your ability to apply machine learning.  
		Complete both parts to finish Round 2 successfully.
	</p>

	<div class="relative max-w-3xl mx-auto space-y-12">

		{#each parts as part, i}
			<div in:slide={{ duration: 250 + i * 100 }} class="relative group">
				<div
					class="p-6 rounded-xl bg-[var(--card-bg)] border border-[var(--border)]
					       shadow-lg transition-all group-hover:shadow-indigo-500/20"
				>
					<div class="flex items-center gap-3 mb-3">
						<svelte:component this={part.icon} size="22" class="text-indigo-400" />
						<h2 class="text-xl font-bold text-[var(--text-primary)]">{part.title}</h2>
					</div>

					<p class="text-[var(--text-secondary)] text-sm leading-relaxed mb-5">
						{part.desc}
					</p>

					<Button
						class="bg-indigo-500 hover:bg-indigo-600 text-white font-semibold"
						on:click={() => goto(part.path)}
					>
						{part.id === 1 ? "Start Coding" : "Go to Submission Portal"}
					</Button>
				</div>
			</div>
		{/each}

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
