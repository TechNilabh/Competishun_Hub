<script lang="ts">
  import * as SC from 'svelte-cubed';
  import * as THREE from 'three';
  import { OrbitControls } from 'svelte-cubed';
  import { onMount } from 'svelte';

  const CUBE_SIZE = 0.2;
  const RADIUS = 5;
  const NUM_CUBES = 800;
  const ROTATION_SPEED = 0.005;

  let cubes: Array<{
    position: THREE.Vector3;
    originalAngle: number;
    material: THREE.MeshStandardMaterial;
  }> = [];

  //  planetary materials
  const materials = [
    new THREE.MeshStandardMaterial({ color: 0x000000 }), 
    new THREE.MeshStandardMaterial({ color: 0x444444 }), 
    new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x101010 }), 
    new THREE.MeshStandardMaterial({ color: 0x111111 }) 
  ];

  // spherical cube distribution
  for(let i = 0; i < NUM_CUBES; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const radius = RADIUS + (Math.random() - 0.5) * 0.3;

    const pos = new THREE.Vector3().setFromSphericalCoords(
      radius,
      phi,
      theta
    );

    cubes.push({
      position: pos,
      originalAngle: theta,
      material: materials[Math.floor(Math.random() * materials.length)]
    });
  }

  // Animation loop
  onMount(() => {
    const animate = () => {
      cubes = cubes.map(cube => {
        const newPos = cube.position.clone().applyAxisAngle(
          new THREE.Vector3(0, 1, 0),
          ROTATION_SPEED
        );
        return { ...cube, position: newPos };
      });
      requestAnimationFrame(animate);
    };
    animate();
  });
</script>

<SC.Canvas background={new THREE.Color(0x000000)}>
  <SC.PerspectiveCamera position={[10, 5, 10]} />
  <OrbitControls 
    enableZoom={true} 
    autoRotate={true}
    autoRotateSpeed={0.5}
  />

  <SC.AmbientLight intensity={0.2} />
  <SC.DirectionalLight
    position={[10, 10, 5]}
    intensity={1.5}
    shadow
  />

  <!-- Core sphere -->
  <SC.Mesh
    geometry={new THREE.SphereGeometry(RADIUS * 0.7, 32, 32)}
    material={new THREE.MeshStandardMaterial({
      color: 0x888888,
      emissive: 0x000000,
      emissiveIntensity: 0.3
    })}
  />

  {#each cubes as cube}
    <SC.Mesh
      position={[cube.position.x, cube.position.y, cube.position.z]}
      geometry={new THREE.BoxGeometry(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)}
      material={cube.material}
      castShadow
      receiveShadow
    />
  {/each}

  <!-- Atmosphere effect -->
  <SC.Mesh
    geometry={new THREE.SphereGeometry(RADIUS * 0.9, 32, 32)}
    material={new THREE.MeshStandardMaterial({
      color: 0xC3F4E6,
      transparent: true,
      opacity: 0.01,
      side: THREE.DoubleSide
    })}
  />
</SC.Canvas>