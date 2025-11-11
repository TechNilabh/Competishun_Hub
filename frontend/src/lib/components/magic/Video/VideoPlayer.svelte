<script lang="ts">
    export let src: string;
    export let active: boolean;
    export let poster: string | undefined = undefined;
    export let autoplay = false;
    export let loop = false;
    export let muted = false;
    export let controls = true;

    let videoElement: HTMLVideoElement;

    $: {
        if(videoElement) {
            if(active) {
                videoElement.play().catch(e => console.log('autoplay err: ', e));
            }else{
                videoElement.pause();
            }
        }
    }

</script>

<div
    class="relative w-full max-w-4xl mx-auto bg-black rounded-xl overflow-hidden shadow-xl p-3 md:p-4 lg:p-5 xl:p-6"
    role="region"
>
    <video
        bind:this={videoElement}
        {src}
        {poster}
        {autoplay}
        {loop}
        {muted}
        {controls}
        class="w-full aspect-video object-contain"
    />
</div>

