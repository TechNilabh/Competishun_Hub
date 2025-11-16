<script lang="ts">
	import { onMount } from "svelte";

	const sections = [
		{
			id: "description",
			title: "Description",
			content: `
				<h3 class="font-semibold text-xl mb-2">Start here if…</h3>
				<p class="mb-4">
					This competition challenges you to predict the sale price of houses based on multiple
					features such as size, location, condition, and overall quality. If you know some basic
					Python/R and machine learning concepts, this is a perfect challenge to improve your
					skills.
				</p>

				<p class="mb-4">
					You'll perform exploratory data analysis, feature engineering, regression modeling, and 
					hyperparameter tuning to achieve the best score.
				</p>

				<h3 class="font-semibold text-xl mb-2">Competition Description</h3>
				<p class="mb-4">
					Housing prices depend on many factors—not just the number of bedrooms or the size of the house.
					This dataset contains dozens of explanatory variables describing almost every aspect of a home.
					Your goal is to use these features to predict the final sale price.
				</p>

				<ul class="list-disc pl-6 space-y-1 mb-4">
					<li>79 explanatory variables describing residential homes</li>
					<li>Perfect for testing regression skills</li>
					<li>Real-world messy data (missing values, skew, categorical variables)</li>
				</ul>
			`
		},

		{
			id: "evaluation",
			title: "Evaluation",
			content: `
				<h3 class="text-xl font-semibold mb-2">Goal</h3>
				<p class="mb-4">
					Your task is to predict the final sale price for each house in the test set.
					Your output must be a <code>submission.csv</code> file.
				</p>

				<h3 class="text-xl font-semibold mb-2">Metric</h3>
				<p class="mb-4">
					Submissions are evaluated using <strong>Root Mean Squared Error (RMSE)</strong> between the
					log-transformed predicted and actual sale prices.
				</p>
			`
		},

		{
			id: "tutorials",
			title: "Tutorials",
			content: `
				<h3 class="font-semibold text-lg mb-2">Recommended Learning</h3>

				<ul class="list-disc pl-6 space-y-1">
					<li>Feature engineering techniques</li>
					<li>Handling missing values</li>
					<li>Gradient boosting (XGBoost, LightGBM)</li>
					<li>Regularization: Ridge, Lasso, ElasticNet</li>
					<li>Model stacking and blending</li>
				</ul>
			`
		}
	];

	let activeSection = "description";
	let mobileTOCOpen = false;

	onMount(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) activeSection = entry.target.id;
				});
			},
			{ threshold: 0.4 }
		);

		sections.forEach((s) => {
			const el = document.getElementById(s.id);
			if (el) observer.observe(el);
		});
	});
</script>

<!-- Layout -->
<div class="relative flex gap-10 items-start">
	
	<!-- Sticky Sidebar -->
	<!-- <aside
		use:stickySidebar={{ topSpacing: 100, bottomSpacing: 440 }}
		class="w-64 hidden md:block bg-[#1c1c1c] rounded-xl p-5 shadow-lg border border-gray-700"
	>
		<h2 class="text-lg font-bold mb-4">Table of Contents</h2>

		<ul class="relative space-y-1">
			{#each sections as s}
				<li class="relative">
					<a
						href={"#" + s.id}
						class="block px-3 py-2 rounded-md transition-all duration-200
							{activeSection === s.id
								? 'bg-gray-700/40 text-white font-semibold shadow-inner'
								: 'text-gray-400 hover:bg-gray-700/20 hover:text-white'}"
					>
						{s.title}
					</a>
				</li>
			{/each}
		</ul>
	</aside> -->

	<!-- Mobile TOC Toggle -->
	<!-- <div class="md:hidden mb-4">
		<button
			class="px-4 py-2 bg-gray-800 rounded-md border border-gray-700 text-gray-200"
			on:click={() => (mobileTOCOpen = !mobileTOCOpen)}
		>
			{mobileTOCOpen ? "Close Menu" : "Open Table of Contents"}
		</button>

		{#if mobileTOCOpen}
			<ul
				class="mt-4 bg-[#1c1c1c] rounded-lg border border-gray-700 shadow-xl p-4 space-y-2 animate-fadeIn"
			>
				{#each sections as s}
					<li>
						<a
							href={"#" + s.id}
							class="block px-3 py-2 rounded-md transition-all duration-200
								{activeSection === s.id
									? 'bg-gray-700/40 text-white font-semibold'
									: 'text-gray-400 hover:bg-gray-700/20 hover:text-white'}"
							on:click={() => (mobileTOCOpen = false)}
						>
							{s.title}
						</a>
					</li>
				{/each}
			</ul>
		{/if}
	</div> -->

	<!-- Main Content -->
	<main class="flex-1 space-y-24 text-black dark:text-white">
		{#each sections as section}
			<section
				id={section.id}
				class="relative scroll-mt-32 p-8  border  rounded-2xl shadow-[0_0_20px_rgba(0,0,0,0.25)]
					hover:shadow-[0_0_30px_rgba(0,0,0,0.45)] transition-all duration-300 animate-fadeIn"
			>
				<div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-t-2xl opacity-70"></div>

				<h2 class="text-4xl font-bold mb-6  tracking-tight">
					{section.title}
				</h2>

				<div class="h-[1px] w-full bg-gray-700/50 mb-6"></div>

				<div class="prose prose-invert max-w-none leading-relaxed ">
					{@html section.content}
				</div>
			</section>
		{/each}
	</main>
</div>

<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(-5px); }
		to { opacity: 1; transform: translateY(0); }
	}
	.animate-fadeIn {
		animation: fadeIn 0.25s ease-out;
	}
</style>