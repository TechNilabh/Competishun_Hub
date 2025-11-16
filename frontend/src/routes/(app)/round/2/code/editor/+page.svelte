<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import CodePage from "$lib/components/coding/codePage.svelte";
	import { codeFlow } from "../store";

	let timer = 0;

	let unsubscribe = codeFlow.subscribe((s) => {
		timer = s.timer;
	});

    let time: () => void;

	onMount(() => {
		time = () => {
        if (document.fullscreenElement) {

            document.documentElement.requestFullscreen().then(() => {
            }).catch(error => {
                console.error("Fullscreen failed:", error);
            });
        }
    };

		document.addEventListener("fullscreenchange", () => {
			if (!document.fullscreenElement) {
				codeFlow.update((s) => ({ ...s, step: 4, fullScreenExited: true }));
				goto("/round/2/code/completed");
			}
		});

		const interval = setInterval(() => {
			codeFlow.update((s) => {
				if (s.timer <= 1) {
					submitTest();
					return s;
				}
				return { ...s, timer: s.timer - 1 };
			});
		}, 1000);

		return () => {
			clearInterval(interval);
			unsubscribe();
		};
	});

	function saveCode(code: string) {
		codeFlow.update((s) => ({ ...s, code }));
	}

	function submitTest() {
		codeFlow.update((s) => ({ ...s, step: 4 }));
		goto("/round/2/code/completed");
	}
</script>

<section class="flex flex-col animate-fadeIn mt-3">
	<div
		class="sticky top-0 z-30 px-6 py-4 flex justify-between items-center
		       shadow-md backdrop-blur-md"
	>
		<div class="flex items-center gap-3">
			<div class="w-3 h-3 rounded-full bg-green-500 animate-pulse"></div>

			<h2 class="text-2xl font-bold text-[var(--text-primary)]">
				Time Left:
				<span class="text-indigo-500">{timer}s</span>
			</h2>
		</div>

		<button
			on:click={submitTest}
			class="px-6 py-2 rounded-lg bg-red-600 hover:bg-red-700
			       text-white font-semibold transition-colors shadow"
		>
			Finish Test
		</button>
	</div>

	<div class="flex-1 p-4 overflow-hidden bg-[var(--bg)]">
		<div
			class="h-full w-full rounded-xl 
			        shadow-xl overflow-hidden"
		>
			<CodePage on:codeChange={(e) => saveCode(e.detail)} />
		</div>
	</div>
</section>

<style>
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(10px); }
		to { opacity: 1; transform: translateY(0); }
	}

	.animate-fadeIn {
		animation: fadeIn 0.4s ease-out;
	}
</style>
