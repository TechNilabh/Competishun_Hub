<script lang="ts">
	import { onMount } from "svelte";

	let leaderboard : any = [];

	let HIT_URL = '/round/2/ml/api/leaderboard';


	onMount(async () => {
		const res = await fetch(HIT_URL);
		leaderboard = await res.json();
	});
</script>

<h1 class="text-2xl font-bold mb-4">Leaderboard</h1>

<table class="w-full text-left border-collapse border border-gray-700">
	<tr class="bg-gray-800">
		<th class="px-4 py-2">Rank</th>
		<th class="px-4 py-2">User</th>
		<th class="px-4 py-2">Score</th>
	</tr>

	{#each leaderboard as entry, i}
	<tr class="border border-gray-700">
		<td class="px-4 py-2">{i + 1}</td>
		<td class="px-4 py-2">{entry.user}</td>
		<td class="px-4 py-2">{entry.score}</td>
	</tr>
	{/each}
</table>
