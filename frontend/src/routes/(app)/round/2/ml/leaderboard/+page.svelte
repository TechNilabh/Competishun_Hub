<script lang="ts">
	import { onMount } from "svelte";

	let leaderboard: any[] = [];
	let loading = true;

	let HIT_URL = "/round/2/ml/api/leaderboard";

	onMount(async () => {
		try {
			const res = await fetch(HIT_URL);
			leaderboard = await res.json();
		} finally {
			loading = false;
		}
	});
</script>

<section class="text-black dark:text-white mt-20">

	<h1 class="text-3xl font-bold mb-6 text-center">Leaderboard</h1>

	<div class="w-full max-w-3xl mx-auto">

		<!-- Loading Spinner -->
		{#if loading}
			<div class="flex justify-center py-10">
				<div class="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
			</div>
		{:else}

			<!-- Table Wrapper -->
			<div class="overflow-x-auto rounded-xl shadow-md border border-indigo-500/40">

				<table class="w-full border-collapse">
					
					<!-- Sticky Header -->
					<thead class="bg-indigo-500 text-white sticky top-0">
						<tr>
							<th class="px-4 py-3 text-left">Rank</th>
							<th class="px-4 py-3 text-left">User</th>
							<th class="px-4 py-3 text-left">Score</th>
						</tr>
					</thead>

					<tbody>
						{#each leaderboard as entry, i}
							<tr
								class="
									border-b border-indigo-500/20 
									odd:bg-indigo-500/5 
									even:bg-white dark:even:bg-gray-900 
									hover:bg-indigo-500 hover:text-white transition
								"
							>
								<td class="px-4 py-3 font-semibold">{i + 1}</td>
								<td class="px-4 py-3">{entry.user}</td>
								<td class="px-4 py-3">{entry.score}</td>
							</tr>
						{/each}
					</tbody>

				</table>
			</div>
		{/if}

	</div>

</section>
