<script lang="ts">
	import { codeFlow } from "../store";

	const instructions = [
		"Your code must run within the time limit.",
		"Internet access is disabled inside the coding environment.",
		"Your code will run against multiple hidden test cases.",
		"You cannot go back once you enter fullscreen mode.",
		"Make sure you understand the input/output format.",
		"You can use the sample tests for initial debugging."
	];

	function start() {
		codeFlow.update((s) => ({ ...s, step: 2 }));
		window.location.href = "/round/2/code/fullscreen";
	}
</script>

<section class="max-w-3xl mx-auto mt-20 px-4 animate-fadeIn">

	<!-- Header -->
	<div class="mb-8">
		<h1 class="text-4xl font-bold tracking-tight mb-3 text-[var(--text-primary)] relative inline-block">
			Coding Round Instructions

			<!-- Indigo underline -->
			<span class="absolute -bottom-1 left-0 w-20 h-[3px] bg-indigo-500 rounded-full"></span>
		</h1>

		<p class="text-[var(--text-secondary)] text-lg max-w-2xl">
			Please read all the points below carefully. Once you begin the coding round,
			your timer starts immediately.
		</p>
	</div>

	<!-- Instructions Card -->
	<div
		class="p-6 rounded-2xl border bg-[var(--card-bg)] border-[var(--border)]
		       shadow-lg shadow-black/30 transition-all duration-300 hover:shadow-xl"
	>
		<h2 class="text-2xl font-semibold text-[var(--text-primary)] mb-5 flex items-center gap-2">
			<!-- Indigo indicator dot -->
			<span class="w-3 h-3 bg-indigo-500 rounded-full"></span>
			Before You Start
		</h2>

		<ul class="space-y-5">
			{#each instructions as text}
				<li class="flex items-start gap-3">
					<!-- icon -->
					<div class="mt-1 text-indigo-500 w-5 h-5 flex items-center justify-center">
						<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
							<path d="M5 12l5 5L20 7"/>
						</svg>
					</div>

					<p class="text-[var(--text-secondary)] leading-relaxed">
						{text}
					</p>
				</li>
			{/each}
		</ul>
	</div>

	<!-- Warning Box -->
	<div
		class="mt-6 p-4 rounded-xl border border-yellow-600/50 bg-yellow-600/10 text-yellow-500"
	>
		<p class="font-semibold">⚠ Important</p>
		<p class="text-sm mt-1">
			Once you press <strong>Start Coding</strong>, fullscreen mode begins and your timer starts.
		</p>
	</div>

	<!-- Start Button -->
	<div class="mt-10">
		<button
			on:click={start}
			class="px-7 py-3 rounded-xl font-semibold text-white bg-indigo-500
			       hover:bg-indigo-600 transition-all duration-200 shadow-lg shadow-indigo-900/30
			       flex items-center gap-2"
		>
			Start Coding
			<span class="transition-transform group-hover:translate-x-1">→</span>
		</button>
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
