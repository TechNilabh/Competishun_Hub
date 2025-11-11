<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  // Game settings
  const gridSize = 20; // Size of each cell in pixels
  const boardSizeInCells = 20;
  const boardWidth = boardSizeInCells * gridSize; // 400px
  const boardHeight = boardSizeInCells * gridSize; // 400px
  const initialSnakeLength = 4;

  let snake: { x: number; y: number }[] = [];
  let food: { x: number; y: number } = { x: 0, y: 0 };
  let direction: string = "right"; // 'up', 'down', 'left', 'right'
  let gameOver: boolean = false;
  let score: number = 0;
  let gameInterval: number;
  let gameSpeed: number = 150; // Milliseconds per move (slower is easier)

  // Touch variables are now unused as touch handlers have been removed from the DOM.
  let touchStartX = 0;
  let touchStartY = 0;
  const swipeThreshold = 20; // Minimum distance to register a swipe

  function initializeGame() {
    snake = [];
    // Start the snake in the middle
    const startX = Math.floor(boardSizeInCells / 2);
    const startY = Math.floor(boardSizeInCells / 2);
    for (let i = 0; i < initialSnakeLength; i++) {
      snake.push({ x: startX - i, y: startY });
    }
    direction = "right";
    score = 0;
    gameOver = false;
    placeFood();
    startGameLoop();
  }

  function placeFood() {
    let newFoodX: number, newFoodY: number;
    let collisionWithSnake;
    const maxIndex = boardSizeInCells;
    do {
      newFoodX = Math.floor(Math.random() * maxIndex);
      newFoodY = Math.floor(Math.random() * maxIndex);
      collisionWithSnake = snake.some(
        (segment) => segment.x === newFoodX && segment.y === newFoodY
      );
    } while (collisionWithSnake); 

    food = { x: newFoodX, y: newFoodY };
  }

  function handleKey(e: KeyboardEvent) {
    if (gameOver) {
        if (e.key === "r" || e.key === "R") initializeGame();
        return;
    }

    // Standard WASD or Arrow Keys
    if (e.key === "ArrowUp" || e.key === "w") {
      if (direction !== "down") direction = "up";
    } else if (e.key === "ArrowDown" || e.key === "s") {
      if (direction !== "up") direction = "down";
    } else if (e.key === "ArrowLeft" || e.key === "a") {
      if (direction !== "right") direction = "left";
    } else if (e.key === "ArrowRight" || e.key === "d") {
      if (direction !== "left") direction = "right";
    }
  }

  // Mobile swipe functions kept in script but removed from DOM handlers
  function handleTouchStart(e: TouchEvent) {
    if (gameOver) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }

  function handleTouchEnd(e: TouchEvent) {
    if (gameOver) return;

    const touchEndX = e.changedTouches[0].clientX;
    const touchEndY = e.changedTouches[0].clientY;

    const dx = touchEndX - touchStartX;
    const dy = touchEndY - touchStartY;

    // Check if it's a significant swipe
    if (Math.abs(dx) > swipeThreshold || Math.abs(dy) > swipeThreshold) {
      if (Math.abs(dx) > Math.abs(dy)) {
        // Horizontal swipe
        if (dx > 0) {
          if (direction !== "left") direction = "right";
        } else {
          if (direction !== "right") direction = "left";
        }
      } else {
        // Vertical swipe
        if (dy > 0) {
          if (direction !== "up") direction = "down";
        } else {
          if (direction !== "down") direction = "up";
        }
      }
    }
  }

  function moveSnake() {
    if (gameOver) return;

    const head = { ...snake[0] }; 

    // Calculate new head position
    switch (direction) {
      case "up":
        head.y--;
        break;
      case "down":
        head.y++;
        break;
      case "left":
        head.x--;
        break;
      case "right":
        head.x++;
        break;
    }

    // --- INFINITE BOUNDARY (WALL WRAPPING) ---
    const maxIndex = boardSizeInCells;
    if (head.x < 0) {
      head.x = maxIndex - 1; // Wrap right
    } else if (head.x >= maxIndex) {
      head.x = 0; // Wrap left
    } else if (head.y < 0) {
      head.y = maxIndex - 1; // Wrap down
    } else if (head.y >= maxIndex) {
      head.y = 0; // Wrap up
    }

    // Check for self-collision
    if (snake.some((segment) => segment.x === head.x && segment.y === head.y)) {
      gameOver = true;
      clearInterval(gameInterval);
      return;
    }

    // Add new head
    snake = [head, ...snake];

    // Check if food is eaten
    if (head.x === food.x && head.y === food.y) {
      score++;
      placeFood(); 
      // Speed up slightly every 5 points, max speed at 100ms
      if (score % 5 === 0 && gameSpeed > 100) {
          gameSpeed -= 10;
          startGameLoop(); // Restart interval with new speed
      }
    } else {
      snake.pop(); // Remove tail if no food eaten
    }
  }

  function startGameLoop() {
    clearInterval(gameInterval); 
    gameInterval = setInterval(moveSnake, gameSpeed);
  }

  onMount(() => {
    window.addEventListener("keydown", handleKey);
    initializeGame(); 
  });

  onDestroy(() => {
    window.removeEventListener("keydown", handleKey);
    clearInterval(gameInterval); 
  });
</script>

<div>
    <!-- Score Display -->
    <div class="flex justify-center mb-4">
        <div class="text-slate-400 text-h2 font-bold px-4 py-1">
            {score}
        </div>
    </div>

    <!-- Game Board -->
    <div
      class="relative z-1000 overflow-hidden rounded-xl  touch-none"
      style="width: {boardWidth}px; height: {boardHeight}px;"
    >
        <!-- Snake Segments -->
        {#each snake as segment, i}
            <div
                class="absolute rounded-sm transition-all duration-100 ease-linear"
                class:bg-green-500={i !== 0}
                class:bg-green-400={i === 0}
                class:shadow-lg={i === 0}
                style="width: {gridSize}px; height: {gridSize}px; top: {segment.y * gridSize}px; left: {segment.x * gridSize}px;"
            ></div>
        {/each}

        <!-- Food -->
        <div
            class="absolute bg-red-500 rounded-full animate-pulse"
            style="width: {gridSize}px; height: {gridSize}px; top: {food.y * gridSize}px; left: {food.x * gridSize}px; transform: scale(0.8);"
        ></div>

        {#if gameOver}
            <div class="absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center text-white text-3xl font-extrabold p-8 rounded-xl backdrop-blur-sm">
                <span class="text-body text-white mb-2">CRASH!</span>
                <span class="text-small mt-4">Final Score: {score}</span>
                <button on:click={initializeGame} class="mt-8 px-6 py-3 bg-white hover:bg-slate-400 text-gray-900 font-bold rounded-full text-body shadow-lg transition duration-200 transform hover:scale-[1.001]">
                    RESTART (R)
                </button>
            </div>
        {/if}
    </div>
</div>

<style>
    /* Global styles for smooth transition */
    .transition-all {
        transition-property: top, left, transform;
    }
</style>
