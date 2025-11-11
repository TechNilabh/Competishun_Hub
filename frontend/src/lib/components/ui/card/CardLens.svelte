<script>
  import Lens from "$lib/components/ui/card/Lens.svelte";
//   import v0_1_0 from '$lib/imgs/v0.1.0.png';
  import v22_1 from '$lib/imgs/Features/exe.gif';
  let hovering = false;
</script>


  <div class="relative z-10">
      <Lens bind:hovering>
        <img
          src={v22_1}
          alt="image_code"
          width={500}
          height={500}
        />
      </Lens>
    </div>

