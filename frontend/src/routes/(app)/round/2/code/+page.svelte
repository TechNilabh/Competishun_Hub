<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import Editor from './editor.svelte';
	import { onMount, tick } from 'svelte';

	export const ssr = false;

	let language = "python";
	let showPreview = true;
	let hasSubmitted = false;

	interface TestCase { input: string; expected: string; }
	interface TestResult { input: string; output: string; expected: string; passed: boolean; }
	interface SubmitOutput { total: number; results: TestResult[]; }

	let runOutput = "";           
	let submitResult: SubmitOutput | null = null;  
	let preview: TestCase[] = []; 

	let customInput = "";
	let running = false;

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
}`
,
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

	function changeLang(l: string) {
		language = l;
		code = templates[l];
	}

	$: console.debug("[Parent] code (preview):", code.slice(0,200));

	async function runCode() {
		running = true;
		runOutput = "Running...";

		const res = await fetch('/round/2/code/api/run', {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ code, language, input: customInput })
		});

		const data = await res.json();
		runOutput = data.output;
		running = false;
	}

	async function submit() {
		await tick();

		running = true;
		showPreview = false;

		console.debug("[Parent] submitting code (sent):", code.slice(0,200));

		const res = await fetch('/round/2/code/api/submit', {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ code, language })
		});

		submitResult = await res.json();
		hasSubmitted = true;
		running = false;
	}

	onMount(async () => {
		const res = await fetch('/round/2/code/api/preview');
		preview = await res.json();
	});
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
				<Editor bind:code={code} {language} on:update:code={(e) => { code = e.detail; console.debug('[Parent] on:update:code', code.slice(0,200)) }} />
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

			<!-- RUN OUTPUT PANEL -->
			<div class="border rounded-xl p-3 bg-neutral-900 text-green-400 font-mono text-sm">
				<h3 class="font-bold mb-2">Run Output</h3>
				<div class="whitespace-pre-wrap">{runOutput}</div>
			</div>

			<!-- BEFORE SUBMIT: SHOW ONLY PREVIEW -->
			{#if showPreview}
				<div class="space-y-4">
					<h3 class="font-bold text-lg">Sample Test Cases (first 5)</h3>

					<ul class="space-y-2">
						{#each preview as p, i}
							<li class="p-2 border rounded">
								<div class="text-gray-400 text-sm">Input: {p.input}</div>
								<div class="text-gray-400 text-sm">Expected: {p.expected}</div>
								<div class="text-gray-500 italic text-xs">Test Case {i+1} (not submitted)</div>
							</li>
						{/each}
					</ul>

					<h4 class="font-semibold mt-4">Locked Test Cases</h4>
					<ul>
						{#each Array( preview.length + 1, 15 ) as _, i}
							<li class="text-gray-500 text-sm">Test Case {i + 6} (locked)</li>
						{/each}
					</ul>
				</div>
			{/if}

			<!-- AFTER SUBMIT -->
			{#if submitResult}
				<div class="space-y-4">
					<h3 class="font-bold text-lg">
						{submitResult.results.filter(r => r.passed).length} / {submitResult.total} Passed
					</h3>

					<h4 class="font-semibold mt-2">Sample Test Cases (first 5)</h4>
					<ul class="space-y-2">
						{#each submitResult.results.slice(0, 5) as r, i}
							<li class="p-2 border rounded flex justify-between">
								<div>
									<div class="text-gray-400 text-sm">Input: {r.input}</div>
									<div class="text-gray-400 text-sm">Output: {r.output}</div>
									<div class="text-gray-400 text-sm">Expected: {r.expected}</div>
								</div>
								<span class={r.passed ? "text-green-400 text-xl" : "text-red-400 text-xl"}>
									{r.passed ? "✔" : "✘"}
								</span>
							</li>
						{/each}
					</ul>

					<h4 class="font-semibold mt-4">Locked Test Cases</h4>
					<ul class="space-y-1">
						{#each submitResult.results.slice(5) as r, i}
							<li class="flex justify-between p-2 border rounded">
								<div class="text-gray-500 text-sm">
									Test Case {i + 6} (locked)
								</div>
								<span class={r.passed ? "text-green-400 text-xl" : "text-red-400 text-xl"}>
									{r.passed ? "✔" : "✘"}
								</span>
							</li>
						{/each}
					</ul>
				</div>
			{/if}


		</div>

	</div>
</section>
