<script lang="ts">
	import { goto } from '$app/navigation';
	import { fade, slide } from 'svelte/transition';
    import { Lightbulb, FileWarning } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
</script>

<section class="relative mx-auto max-w-6xl px-6 md:px-10 pt-36 pb-36">
	<!-- Heading -->
	<h1
		in:fade={{ duration: 300 }}
		class="text-3xl sm:text-4xl lg:text-5xl font-bold text-center 
    bg-gradient-to-br from-black to-black/40 dark:from-white dark:to-white/40 
    bg-clip-text text-transparent mb-6"
	>
		Round 2 — Coding Challenge
	</h1>

	<p
		in:fade={{ duration: 400 }}
		class="text-center max-w-2xl mx-auto text-lg opacity-80 mb-12"
	>
		This round evaluates your coding ability and your understanding of logic, algorithms,
		and applied machine learning. You will complete two parts: a coding challenge and a
		model-based submission.
	</p>

	<!-- Timeline / Steps -->
	<div class="flex flex-col gap-10 mt-10 max-w-3xl mx-auto border-l border-neutral-300 dark:border-neutral-700 pl-6">

		<!-- Part 1 -->
		<div in:slide={{ duration: 300 }} class="relative">
			<div class="absolute -left-[13px] top-1 w-4 h-4 rounded-full bg-[--color]"></div>

			<h2 class="text-xl font-semibold mb-1">Part 1 — Code Execution Task</h2>

			<p class="text-sm opacity-80 mb-4">
				Write and run code for the given problem. Your solution will be automatically
				graded against a set of hidden test cases.
			</p>

			<Button on:click={() => goto('/round/2/code')}>Start Coding</Button>
		</div>

		<!-- Part 2 -->
		<div in:slide={{ duration: 350 }} class="relative">
			<div class="absolute -left-[13px] top-1 w-4 h-4 rounded-full bg-[--color]"></div>

			<h2 class="text-xl font-semibold mb-1">Part 2 — ML Submission</h2>

			<p class="text-sm opacity-80 mb-4">
				Download the dataset, build your model, generate <code>submission.csv</code>,
				and upload it along with your <code>.ipynb</code> notebook.  
				Your accuracy & mismatch score will be computed automatically.
			</p>

			<Button on:click={() => goto('/round/2/submission')}>Go to Submission Portal</Button>
		</div>
	</div>
</section>
