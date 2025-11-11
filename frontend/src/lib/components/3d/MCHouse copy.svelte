<script lang="ts">
  import * as SC from 'svelte-cubed';
  import * as THREE from 'three';
  import { OrbitControls } from 'svelte-cubed';
  import { onMount } from 'svelte';
  import { theme } from '$lib/stores/theme'; // Assuming you have a theme store

  // Colors that adapt to your theme
  let chipColor: THREE.Color;
  let pinColor: THREE.Color;
  let textColor: THREE.Color;
  let highlightColor: THREE.Color;
  
  $: {
    chipColor = new THREE.Color($theme === 'dark' ? '#333333' : '#e0e0e0');
    pinColor = new THREE.Color($theme === 'dark' ? '#666666' : '#999999');
    textColor = new THREE.Color($theme === 'dark' ? '#ffffff' : '#000000');
    highlightColor = new THREE.Color($theme === 'dark' ? '#9e7aff' : '#9e7aff');
  }

  // Microprocessor dimensions
  const CHIP_WIDTH = 5;
  const CHIP_HEIGHT = 0.3;
  const CHIP_DEPTH = 5;
  const PIN_LENGTH = 0.5;
  const PIN_RADIUS = 0.1;

  // Create pins (40 pins for 8085)
  const pins = Array.from({ length: 40 }).map((_, i) => {
    const angle = (i / 40) * Math.PI * 2;
    const radius = CHIP_WIDTH / 2 + PIN_LENGTH / 2;
    
    return {
      position: new THREE.Vector3(
        Math.cos(angle) * radius,
        -CHIP_HEIGHT / 2 - PIN_RADIUS,
        Math.sin(angle) * radius
      ),
      rotation: [0, angle, 0] as [number, number, number]
    };
  });

  // Important pins to highlight
  const importantPins = [1, 6, 7, 8, 9, 10, 29, 30, 31, 40]; // Example important pins

  // Create address/data bus lines (reactive so highlightColor is assigned)
  $: busLines = [
    { name: 'AD0-AD7', color: highlightColor, position: [0, CHIP_HEIGHT/2 + 0.1, -CHIP_DEPTH/2 + 0.5] },
    { name: 'A8-A15', color: highlightColor, position: [0, CHIP_HEIGHT/2 + 0.1, CHIP_DEPTH/2 - 0.5] },
    { name: 'Control Bus', color: highlightColor, position: [CHIP_WIDTH/2 - 0.5, CHIP_HEIGHT/2 + 0.1, 0] }
  ];

  // Rotation controls
  let autoRotate = true;
  let rotationSpeed = 0.5;
</script>

<SC.Canvas background={new THREE.Color(`hsl(var(--background))`)}>
  <SC.PerspectiveCamera position={[8, 5, 8]} />
  <OrbitControls 
    enableZoom={true}
    autoRotate={autoRotate}
    autoRotateSpeed={rotationSpeed}
  />

  <!-- Lighting that adapts to theme -->
  <SC.AmbientLight intensity={$theme === 'dark' ? 0.8 : 1} />
  <SC.DirectionalLight
    position={[10, 10, 5]}
    intensity={$theme === 'dark' ? 1 : 1.5}
    color={$theme === 'dark' ? 0x444444 : 0xffffff}
  />
  <SC.DirectionalLight
    position={[-10, -10, -5]}
    intensity={0.5}
    color={$theme === 'dark' ? 0x222222 : 0xdddddd}
  />

  <!-- Main chip body -->
  <SC.Mesh
    geometry={new THREE.BoxGeometry(CHIP_WIDTH, CHIP_HEIGHT, CHIP_DEPTH)}
    material={new THREE.MeshStandardMaterial({
      color: chipColor,
      metalness: 0.1,
      roughness: 0.7
    })}
    castShadow
    receiveShadow
  >
    <!-- Chip label -->
    <!-- Replace with a placeholder or remove until a compatible 3D text solution is implemented -->
    <!-- <SC.Text ... /> is not supported in svelte-cubed v0.2.1 -->
  </SC.Mesh>

  <!-- Pins -->
  {#each pins as pin, i}
    <SC.Mesh
      position={[pin.position.x, pin.position.y, pin.position.z]}
      rotation={pin.rotation}
      geometry={new THREE.CylinderGeometry(
        PIN_RADIUS, 
        PIN_RADIUS, 
        PIN_LENGTH, 
        6
      )}
      material={new THREE.MeshStandardMaterial({
        color: importantPins.includes(i + 1) ? highlightColor : pinColor,
        metalness: 0.3,
        roughness: 0.8
      })}
      castShadow
      receiveShadow
    >
      <!-- Pin numbers -->
      <!-- Pin numbers: 3D text not supported in svelte-cubed v0.2.1, placeholder only -->
      <!-- <SC.Text
        text={(i + 1).toString()}
        position={[0, PIN_LENGTH/2 + 0.1, 0]}
        size={0.15}
        color={textColor}
      /> -->
    </SC.Mesh>
  {/each}

  <!-- Bus labels: 3D text not supported in svelte-cubed v0.2.1, placeholder only -->
  
</SC.Canvas>

  <!-- Info panel (3D text) -->
  <!-- <SC.Text ... /> is not supported in svelte-cubed v0.2.1 -->
<!-- <div class="flex items-center gap-2">
  <span class="text-sm">Speed:</span>
  <input 
    type="range" 
    min="0.1" 
    max="2" 
    step="0.1" 
    bind:value={rotationSpeed}
    class="w-24 accent-primary"
  >
</div> -->