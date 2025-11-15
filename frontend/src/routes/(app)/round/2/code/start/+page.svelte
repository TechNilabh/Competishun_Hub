<script lang="ts">
    import { codeFlow } from "../store";

    function start() {
        codeFlow.update((s) => ({ ...s, step: 2 }));
        window.location.href = "/round/2/code/fullscreen";
    }
</script>

<section class="max-w-3xl mx-auto mt-20 px-4 h-[400px]">
    <h1 class="text-3xl font-bold mb-6">Coding Round Instructions</h1>
    <p class="mb-8">Read all instructions before starting...</p>

    <button
        class="bg-blue-600 text-white px-6 py-3 rounded-xl"
        on:click={start}>
        Next →
    </button>
</section>
