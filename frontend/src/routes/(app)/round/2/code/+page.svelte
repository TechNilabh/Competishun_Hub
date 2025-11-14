<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import Editor from './editor.svelte';
	import { onMount } from 'svelte';

	let language = 'python';
	export const ssr = false;


	let templates: Record<string, string> = {
		python: `# Write your solution here
def solve():
	n = int(input())
	print(n * 2)

if __name__ == "__main__":
	solve()
`,
		c: `#include <stdio.h>
int main() {
	int n;
	scanf("%d", &n);
	printf("%d", n * 2);
	return 0;
}`,
		cpp: `#include <bits/stdc++.h>
using namespace std;

int main() {
	int n;
	cin >> n;
	cout << n * 2;
	return 0;
}`
	};

	let code = templates[language];
	let customInput = "";
	let output = "";
	let running = false;

	function changeLang(l: string) {
		language = l;
		code = templates[l];
	}

	async function runCode() {
		running = true;
		output = "Running...";

		const res = await fetch('/round/2/code/api/run', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ code, language, input: customInput })
		});
		const data = await res.json();
		output = data.output;
		running = false;
	}

	async function submit() {
		running = true;
		output = "Evaluating on test cases...";

		const res = await fetch('/round/2/code/api/submit', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ code, language })
		});
		const data = await res.json();
		output = data.output;
		running = false;
	}
</script>

<section class="max-w-7xl mx-auto mt-16 px-6 pb-28">
	<h1 class="text-3xl font-bold mb-10">Round 2 — Coding Challenge</h1>

	<div class="grid grid-cols-1 xl:grid-cols-3 gap-8">

		<!-- EDITOR PANEL -->
		<div class="xl:col-span-2 flex flex-col gap-4">
			
			<!-- Language Selector Bar -->
			<div class="flex items-center gap-3 bg-white dark:bg-neutral-900 border rounded-xl p-3 shadow">
				<p class="font-medium">Language:</p>
				{#each ["python", "c", "cpp"] as lang}
					<Button
						variant={lang === language ? "default" : "secondary"}
						on:click={() => changeLang(lang)}
						class="capitalize"
					>
						{lang}
					</Button>
				{/each}
			</div>

			<!-- EDITOR -->
			<div class="rounded-xl border shadow overflow-hidden">
				<Editor bind:code {language} />
			</div>
		</div>

		<!-- RIGHT PANEL -->
		<div class="flex flex-col gap-6">

			<!-- Custom Input -->
			<div class="bg-white dark:bg-neutral-900 border rounded-xl shadow p-4">
				<h2 class="font-semibold mb-2">Custom Input</h2>
				<textarea
					bind:value={customInput}
					class="w-full h-28 p-2 border rounded bg-neutral-950 text-white font-mono"
					placeholder="Enter input..."
				></textarea>
			</div>

			<!-- Action Buttons -->
			<div class="flex gap-3">
				<Button disabled={running} class="flex-1" on:click={runCode}>
					{running ? "Running..." : "Run Code"}
				</Button>

				<Button disabled={running} class="flex-1" on:click={submit}>
					Submit
				</Button>
			</div>

			<!-- Output Panel -->
			<div class="border rounded-xl p-4 text-sm bg-neutral-950 text-green-400 font-mono h-64 overflow-auto shadow">
				{output}
			</div>

		</div>

	</div>
</section>
