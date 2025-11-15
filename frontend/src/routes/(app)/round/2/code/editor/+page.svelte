<script lang="ts">
    import { onMount } from "svelte";
    import CodePage from "$lib/components/coding/codePage.svelte";
    import { codeFlow } from "../store";

    let timer = 0;

    // Subscribe store
    const unsubscribe = codeFlow.subscribe((state) => {
        timer = state.timer;
    });

    onMount(() => {
        const interval = setInterval(() => {
            codeFlow.update((s) => {
                if (s.timer <= 1) {
                    submitTest();  // Auto submit
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

    function saveCode(code: any) {
        codeFlow.update((s) => ({ ...s, code }));
    }

    function submitTest() {
        codeFlow.update((s) => ({ ...s, step: 4 }));
        window.location.href = "/round/2/code/completed";
    }
</script>

<section class="w-screen h-full p-3 mt-20 flex flex-col gap-4">
    
    <div class="flex justify-between items-center bg-gray-200 dark:bg-gray-900 p-4 rounded shadow">
        <h2 class="text-2xl font-bold">
            Time Left: {timer}s
        </h2>

        <button
            on:click={submitTest}
            class="px-5 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold"
        >
            Finish Test
        </button>
    </div>

    <div class="flex-1 overflow-hidden">
        <CodePage on:codeChange={(e) => saveCode(e.detail)} />
    </div>
</section>
