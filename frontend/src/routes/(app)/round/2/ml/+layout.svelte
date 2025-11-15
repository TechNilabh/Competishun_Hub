<script lang="ts">
    import MLNavbar from "$lib/components/ml/MLNavbar.svelte";
</script>

<div class="min-h-screen p-20 text-white">
    <MLNavbar />
    <main class="px-6 py-6 max-w-6xl mx-auto">
        <slot />
    </main>
</div>
