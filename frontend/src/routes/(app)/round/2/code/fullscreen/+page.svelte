<script lang="ts">
	import { onMount } from "svelte";
    import { codeFlow } from "../store";

    async function enterFullscreen() {
        await document.documentElement.requestFullscreen();
        codeFlow.update((s) => ({ ...s, step: 3 }));
        window.location.href = "/round/2/code/editor";
    }

    function checkFullscreen() {
        if (!document.fullscreenElement) {
            codeFlow.update((s) => ({
                ...s,
                fullScreenExited: true,
                step: 4
            }));
            window.location.href = "/round/2/code/completed";
        }
    }

    onMount(() => {
        document.addEventListener("fullscreenchange", checkFullscreen);
    });
</script>

<section class="max-w-3xl mx-auto mt-20 px-4">
    <h1 class="text-2xl font-bold mb-4">Enable Fullscreen Mode</h1>

    <p class="mb-6">Once you enter fullscreen, the test will begin.</p>

    <button
        on:click={enterFullscreen}
        class="bg-green-600 text-white px-6 py-3 rounded-xl">
        Go Fullscreen & Start →
    </button>
</section>
