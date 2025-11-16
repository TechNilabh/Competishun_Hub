<script lang="ts">
	import { onMount } from "svelte";

	let history: any[] = [];

	onMount(async () => {
		const res = await fetch("/round/2/ml/api/history");
		history = await res.json();
	});
</script>

<h1 class="text-2xl font-bold mb-4">Submission History</h1>

<table class="w-full text-left border-collapse border border-gray-700">
	<tr class="bg-gray-800">
		<th class="px-4 py-2">Time</th>
		<th class="px-4 py-2">Score</th>
		<th class="px-4 py-2">File</th>
	</tr>

	{#each history as h}
	<tr class="border border-gray-700">
		<td class="px-4 py-2">{h.timestamp}</td>
		<td class="px-4 py-2">{h.score}</td>
		<td class="px-4 py-2">{h.file}</td>
	</tr>
	{/each}
</table>
