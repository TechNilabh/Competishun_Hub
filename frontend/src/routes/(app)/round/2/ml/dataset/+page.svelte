<script lang="ts">
	function downloadDataset() {
		window.open("https://drive.google.com/drive/folders/10PmK1Rhrp5cKDJw5PyAf90Lls3FzF-AN?usp=sharing", "_blank");
	}
	const datasetFiles = [
		{ name: "train.csv", desc: "Inputs + labels" },
		{ name: "test.csv", desc: "Inputs only" },
		{ name: "sample_submission.csv", desc: "Sample output format" }
	];
</script>


<section class="mt-20 space-y-6 animate-fadeIn text-black dark:text-white ">

	<div class="inline-block">
		<h1 class="text-3xl font-bold tracking-tight mb-2 relative">
			Dataset
			<span class="absolute -bottom-1 left-0 w-16 h-[3px] bg-indigo-500 rounded-full"></span>
		</h1>
	</div>

	<p class=")] max-w-3xl leading-relaxed">
		This dataset includes all the features required to train and evaluate your model.
		Your <span class="font-semibold"> Submission.csv</span>
		will be scored against hidden labels.
	</p>

	<!-- Dataset File Card -->
	<div
		class="p-6 rounded-2xl border shadow-lg bg-[var(--card-bg)] border-[var(--border)]
		       transition-all duration-300 hover:shadow-[0_0_25px_rgba(0,0,0,0.25)]"
	>
		<h2 class="text-xl font-semibold mb-4  flex items-center gap-2">
			<span class="w-2 h-2 bg-indigo-500 rounded-full"></span>
			Files Included
		</h2>

		<ul class="space-y-3">
			{#each datasetFiles as file}
				<li
					class="flex items-center gap-3 p-3 rounded-lg bg-[var(--item-bg)]
						border border-[var(--border)] hover:bg-[var(--item-hover-bg)]
						transition-colors duration-200"
				>
					<!-- File Icon -->
					<div class="w-9 h-9 rounded-lg flex items-center justify-center bg-blue-600/20">
						<svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" stroke-width="2"
							viewBox="0 0 24 24">
							<path d="M4 4h10l6 6v10a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2z"/>
						</svg>
					</div>

					<!-- File Text -->
					<div>
						<p class="font-semibold ">{file.name}</p>
						<p class="text-sm ">{file.desc}</p>
					</div>
				</li>
			{/each}
		</ul>
	</div>

	<button
		on:click={downloadDataset}
		class="px-6 py-3 rounded-xl font-semibold
		       bg-indigo-500 hover:opacity-75 transition-all
		       shadow-lg shadow-blue-900/20 text-white"
	>
		Download Dataset
	</button>

</section>

<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(12px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.animate-fadeIn {
		animation: fadeIn 0.5s ease-out;
	}
</style>