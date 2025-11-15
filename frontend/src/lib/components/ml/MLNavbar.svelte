<script lang="ts">
	import { page } from '$app/stores';
</script>

<nav class="flex gap-6 border-b border-gray-700 pb-3 text-lg">
	<a class="{ $page.url.pathname.endsWith('/ml') ? 'text-blue-400' : 'text-gray-300' }"
	   href="/round/2/ml">Instructions</a>

	<a class="{ $page.url.pathname.includes('/dataset') ? 'text-blue-400' : 'text-gray-300' }"
	   href="/round/2/ml/dataset">Dataset</a>

	<a class="{ $page.url.pathname.includes('/submission') ? 'text-blue-400' : 'text-gray-300' }"
	   href="/round/2/ml/submission">Submission</a>

	<a class="{ $page.url.pathname.includes('/leaderboard') ? 'text-blue-400' : 'text-gray-300' }"
	   href="/round/2/ml/leaderboard">Leaderboard</a>
</nav>
