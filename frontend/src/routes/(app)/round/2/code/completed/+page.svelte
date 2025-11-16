<script lang="ts">
	import { codeFlow } from "../store";
</script>

<section class="max-w-3xl mx-auto mt-24 px-4 animate-fadeIn">

	<h1 class="text-4xl font-bold mb-6 text-[var(--text-primary)] relative inline-block">
		Test Completed
		<span class="absolute -bottom-1 left-0 w-24 h-[3px] bg-indigo-500 rounded-full"></span>
	</h1>

	{#if $codeFlow.fullScreenExited}
		
		<!-- Forced exit (warning) -->
		<div 
			class="p-6 rounded-2xl border border-amber-600/40 bg-amber-600/10 
			       text-amber-500 shadow-lg mb-8"
		>
			<h2 class="text-2xl font-semibold mb-2 flex items-center gap-2">
				<svg width="24" height="24" stroke="currentColor" stroke-width="2" fill="none">
					<path d="M12 9v4m0 4h.01M10.29 3.86l-8.19 14.2A2 2 0 0 0 4 21h16a2 2 0 0 0 1.9-2.65l-8.2-14.2a2 2 0 0 0-3.42 0z"/>
				</svg>
				Fullscreen Exited — Test Ended
			</h2>

			<p class="text-[var(--text-secondary)] leading-relaxed">
				You exited fullscreen mode during the test, which automatically ends the session.
				Your last written code was saved and your submission has been recorded.
			</p>
		</div>

	{:else}
		
		<!-- Success result -->
		<div 
			class="p-6 rounded-2xl border border-green-600/40 bg-green-600/10 
			       text-green-300 shadow-lg mb-8"
		>
			<h2 class="text-2xl font-semibold mb-2 flex items-center gap-2">
				<svg width="24" height="24" stroke="currentColor" stroke-width="2" fill="none">
					<path d="M5 13l4 4L19 7"/>
				</svg>
				Submission Recorded
			</h2>

			<p class="text-[var(--text-secondary)] leading-relaxed">
				Congratulations! You successfully completed the coding round.
				Your submission has been uploaded and will be evaluated shortly.
			</p>
		</div>

	{/if}

	<!-- Action Buttons -->
	<div class="flex gap-4 mt-10">
		<a
			href="/round/2"
			class="px-6 py-3 rounded-xl bg-indigo-500 hover:bg-indigo-600 
			       text-white font-semibold transition-all shadow"
		>
			Back to Rounds
		</a>

		<a
			href="/round/2/code/review"
			class="px-6 py-3 rounded-xl bg-[var(--item-bg)] border border-[var(--border)]
			       hover:bg-[var(--item-hover-bg)] text-[var(--text-primary)] font-semibold
			       transition-all shadow"
		>
			Review Your Code
		</a>
	</div>

</section>

<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(10px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.animate-fadeIn {
		animation: fadeIn 0.4s ease-out;
	}
</style>
