<script lang="ts">
    import MLNavbar from "$lib/components/ml/MLNavbar.svelte";
</script>

<div class="min-h-screen mt-20 px-3 md:px-10 text-white">
    <MLNavbar />
    <main class="px-6 py-6 max-w-6xl mx-auto">
        <slot />
    </main>
</div>
