<script lang="ts">
	let file: File | null = null;
	let score: number | null = null;
	let rank: number | null = null;
	let status = "";

	let HIT_URL = '/round/2/ml/api/submit'

	function handleFileChange(e: Event) {
		const target = e.target as HTMLInputElement;
		file = target.files?.[0] || null;
	}

	async function handleSubmit() {
		if (!file) {
			status = "Please upload submission.csv";
			return;
		}

		const form = new FormData();
		form.append("file", file);

		status = "Submitting...";

		const res = await fetch(HIT_URL, {
			method: "POST",
			body: form
		});

		const data = await res.json();
		score = data.score;
		rank = data.rank;

		status = "Done!";
	}
</script>

<section class="mt-20">

<input
	type="file"
	accept=".csv"
	on:change={handleFileChange}
	class="mb-4"
/>


<button
	on:click={handleSubmit}
	class="px-5 py-3 bg-green-600 rounded-lg hover:bg-green-500"
>
	Submit
</button>

{#if status}
<p class="mt-4 text-yellow-300">{status}</p>
{/if}

{#if score !== null}
<div class="mt-6 p-4 bg-gray-800 rounded-lg">
	<h2 class="text-xl text-green-400">Your Score: {score.toFixed(4)}</h2>
	<p class="text-gray-300">Your score is also added to the leaderboard.</p>
</div>
{/if}

</section>
