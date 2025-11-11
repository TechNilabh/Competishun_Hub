<script lang="ts">
  import { onMount } from 'svelte';
  import * as SC from 'svelte-cubed';
  import * as THREE from 'three';
  import { OrbitControls } from 'svelte-cubed';
  import { STLLoader } from 'three-stdlib';

  let model: THREE.Mesh | null = null;
  let error: string | null = null;

  onMount(() => {
    const loader = new STLLoader();
    loader.load(
      '/models/transistor.stl',
      (geometry: THREE.BufferGeometry) => {
        const material = new THREE.MeshStandardMaterial({ 
          color: 0x88ccff,
          metalness: 0.2,
          roughness: 0.8
        });
        
        model = new THREE.Mesh(geometry, material);
        geometry.center(); // Center geometry
        model.rotation.set(-Math.PI/2, 0, 0);
        model.scale.set(0.1, 0.1, 0.1);
        model.castShadow = true;
        model.receiveShadow = true;
      },
      undefined,
      (err: ErrorEvent) => {
        error = `Error loading model: ${err.message}`;
        console.error(err);
      }
    );
  });
</script>

<SC.Canvas>
  <SC.PerspectiveCamera position={[1, 1, 1]}>
    <OrbitControls enableZoom={true} enableRotate={true} />
  </SC.PerspectiveCamera>

  <SC.AmbientLight intensity={0.8} />
  <SC.DirectionalLight
    position={[5, 5, 5]}
    intensity={1.2}
    shadow
  />

  {#if error}
    <div class="error">{error}</div>
  {:else if model}
    <SC.Mesh
      geometry={model.geometry}
      material={Array.isArray(model.material) ? model.material[0] : model.material}
      rotation={[model.rotation.x, model.rotation.y, model.rotation.z]}
      scale={[model.scale.x, model.scale.y, model.scale.z]}
      castShadow
      receiveShadow
    />
  {/if}
</SC.Canvas>

<style>
  .error {
    position: fixed;
    top: 20px;
    left: 20px;
    color: red;
    background: white;
    padding: 10px;
    border-radius: 5px;
    z-index: 1000;
  }
</style>