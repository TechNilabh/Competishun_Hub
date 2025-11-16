<script lang="ts">
	import { onMount } from "svelte";

	let file: File | null = null;
	let score: number | null = null;
	let rank: number | null = null;
	let status = "";
	let isSubmitting = false;
	let dragging = false;

	let HIT_URL = "/round/2/ml/api/submit";

	function handleFileChange(e: Event) {
		const target = e.target as HTMLInputElement;
		file = target.files?.[0] || null;
		status = file ? `Selected: ${file.name}` : "";
	}

	function handleDrop(e: DragEvent) {
		e.preventDefault();
		dragging = false;

		if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
			file = e.dataTransfer.files[0];
			status = `Selected: ${file.name}`;
		}
	}

	async function handleSubmit() {
		if (!file || isSubmitting) return;

		status = "Submitting...";
		isSubmitting = true;

		const form = new FormData();
		form.append("file", file);

		const res = await fetch(HIT_URL, { method: "POST", body: form });
		const data = await res.json();

		score = data.score;
		rank = data.rank;

		status = "Done!";
		isSubmitting = false;
	}
</script>

<section class="mt-20 text-black dark:text-white">

	<!-- Upload Box -->
	<div 
		class="
			w-full max-w-xl mx-auto p-6 border-2 border-dashed rounded-xl transition 
			hover:border-indigo-500 
			{dragging ? 'border-indigo-500 bg-indigo-500/10' : 'border-gray-400'}
		"
		on:dragover|preventDefault={() => dragging = true}
		on:dragleave={() => dragging = false}
		on:drop={handleDrop}
	>
		<div class="flex flex-col items-center text-center">
			<p class="text-lg font-semibold">Upload your <span class="text-indigo-500">submission.csv</span></p>
			<p class="text-sm opacity-70 mt-1">Drag & drop or select file manually</p>

			<label class="mt-5 cursor-pointer bg-indigo-500 text-white px-4 py-2 rounded-lg hover:bg-indigo-600 transition">
				Choose File
				<input type="file" accept=".csv" on:change={handleFileChange} class="hidden" />
			</label>

			{#if file}
				<p class="mt-3 text-sm text-indigo-500">{file.name}</p>
			{/if}
		</div>
	</div>

	<!-- Submit Button -->
	<div class="w-full max-w-xl mx-auto mt-6 flex justify-center">
		<button
			on:click={handleSubmit}
			disabled={isSubmitting || !file}
			class="
				px-6 py-3 rounded-lg text-white 
				bg-indigo-500 hover:bg-indigo-600 transition 
				disabled:opacity-40 disabled:cursor-not-allowed
			"
		>
			{#if isSubmitting}
				<span class="flex items-center gap-2">
					<div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
					Submitting...
				</span>
			{:else}
				Submit
			{/if}
		</button>
	</div>

	<!-- Status Text -->
	{#if status}
		<p class="text-center mt-4 text-indigo-500 font-medium">{status}</p>
	{/if}

	<!-- Results -->
	{#if score !== null}
		<div class="mt-8 max-w-xl mx-auto p-6 rounded-xl bg-indigo-500 text-white shadow-lg">
			<h2 class="text-2xl font-bold">Your Score: {score.toFixed(4)}</h2>
			<p class="opacity-90 mt-1">Your submission has been added to the leaderboard.</p>

			{#if rank !== null}
				<p class="mt-3 text-lg font-semibold">Leaderboard Rank: #{rank}</p>
			{/if}
		</div>
	{/if}

</section>
