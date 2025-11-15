<script lang="ts">
    import { codeFlow } from "../store";
</script>

<section class="max-w-3xl mx-auto mt-20 px-4">

    <h1 class="text-3xl font-bold mb-4">Test Completed</h1>

    {#await new Promise((r) => setTimeout(r, 0))}
    {:then}
        <p class="mb-6">
            {#if $codeFlow.fullScreenExited}
                You exited fullscreen — test forcibly ended.  
                Your code was auto-saved.
            {:else}
                Congratulations! Your submission has been recorded.
            {/if}
        </p>
    {/await}

    <a href="/round/2"
        class="bg-blue-600 text-white px-5 py-3 rounded-xl">
        Go Back to Rounds
    </a>
</section>
