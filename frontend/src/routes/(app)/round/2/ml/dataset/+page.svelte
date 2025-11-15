<script lang="ts">
	function downloadDataset() {
		window.open("https://drive.google.com/drive/folders/10PmK1Rhrp5cKDJw5PyAf90Lls3FzF-AN?usp=sharing", "_blank");
	}
</script>

<section class="mt-20">
<h1 class="text-2xl font-bold mb-4">Dataset</h1>

<p class="text-gray-300 mb-4">
	This dataset contains input features and ground truth labels for training your model.
	Your submission will be evaluated against hidden test labels.
</p>

<div class="mt-6 p-4 bg-gray-800 rounded-xl">
	<h2 class="text-xl font-semibold mb-2">Files Included</h2>
	<ul class="list-disc pl-8 text-gray-400">
		<li>train.csv — inputs + labels</li>
		<li>test.csv — inputs only</li>
		<li>sample_submission.csv</li>
	</ul>
</div>

<button
	on:click={downloadDataset}
	class="mt-6 px-5 py-3 bg-blue-600 rounded-lg hover:bg-blue-500">
	Download Dataset
</button>
</section>
