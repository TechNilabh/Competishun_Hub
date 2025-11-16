<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
    import { codeFlow } from "../store";

    async function enterFullscreen() {
		if (!document.fullscreenElement) {
        	await document.documentElement.requestFullscreen();
		}

        codeFlow.update((s) => ({ ...s, step: 3 }));

        goto("/round/2/code/editor");
    }

    function handleFullscreenExit() {
        if (!document.fullscreenElement) {
            codeFlow.update((s) => ({
                ...s,
                fullScreenExited: true,
                step: 4
            }));
            goto("/round/2/code/completed");
        }
    }

    onMount(() => {
        document.addEventListener("fullscreenchange", handleFullscreenExit);
    });
</script>

<section class="max-w-3xl mx-auto mt-20 px-4 animate-fadeIn">

	<!-- Header -->
	<h1 class="text-4xl font-bold text-[var(--text-primary)] mb-4 relative inline-block">
		Enable Fullscreen Mode
		<span class="absolute -bottom-1 left-0 w-24 h-[3px] bg-indigo-500 rounded-full"></span>
	</h1>

	<p class="text-[var(--text-secondary)] text-lg leading-relaxed max-w-2xl mb-8">
		The coding environment is designed to run in fullscreen for a distraction-free
		experience. Once you enter fullscreen, the round will begin immediately.
	</p>

	<!-- Instructions card -->
	<div
		class="p-6 rounded-2xl border border-[var(--border)] bg-[var(--card-bg)]
		       shadow-lg shadow-black/30"
	>
		<h2 class="text-2xl font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
			<span class="w-3 h-3 rounded-full bg-indigo-500"></span>
			Before You Begin
		</h2>

		<ul class="space-y-4">
			<li class="flex items-start gap-3">
				<div class="mt-1 text-indigo-500">
					<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M5 12l5 5L20 7"/>
					</svg>
				</div>
				<p class="text-[var(--text-secondary)]">Your timer starts as soon as fullscreen is enabled.</p>
			</li>

			<li class="flex items-start gap-3">
				<div class="mt-1 text-indigo-500">
					<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M5 12l5 5L20 7"/>
					</svg>
				</div>
				<p class="text-[var(--text-secondary)]">Exiting fullscreen early will automatically end the test.</p>
			</li>

			<li class="flex items-start gap-3">
				<div class="mt-1 text-indigo-500">
					<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M5 12l5 5L20 7"/>
					</svg>
				</div>
				<p class="text-[var(--text-secondary)]">Fullscreen will stay active when you enter the editor.</p>
			</li>

			<li class="flex items-start gap-3">
				<div class="mt-1 text-indigo-500">
					<svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
						<path d="M5 12l5 5L20 7"/>
					</svg>
				</div>
				<p class="text-[var(--text-secondary)]">Use a stable browser window; switching tabs may pause execution.</p>
			</li>
		</ul>
	</div>

	<!-- Warning -->
	<div class="mt-6 p-4 rounded-xl border border-yellow-600/50 bg-yellow-600/10 text-yellow-300">
		<p class="font-semibold">⚠ Important</p>
		<p class="text-sm mt-1">
			Do not exit fullscreen while coding. Doing so will immediately submit and lock your test.
		</p>
	</div>

	<!-- CTA Button -->
	<button
		on:click={enterFullscreen}
		class="mt-10 px-7 py-3 rounded-xl font-semibold bg-indigo-500 hover:bg-indigo-600
		       transition-all duration-200 text-white shadow-lg shadow-indigo-900/30 flex items-center gap-2"
	>
		Go Fullscreen & Start
		<span class="transition-transform group-hover:translate-x-1">→</span>
	</button>
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
