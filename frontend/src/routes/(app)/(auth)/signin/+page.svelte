<script lang="ts">
  import { goto } from '$app/navigation';
  import authStore from '$lib/stores/auth';
  import { toast } from 'svelte-sonner';
  import { ChevronLeft, Loader, Mail, Lock, Github } from 'lucide-svelte';

  let email = '';
  let password = '';
  let loading = false;
  let showPassword = false;

  async function handleSubmit() {
    if (!email || !password) {
      toast.error('Please fill in all fields');
      return;
    }

    loading = true;

    try {
      await authStore.login(email, password);
      toast.success('Logged in successfully!');
      goto('/exam');
    } catch (error: any) {
      toast.error(error.message || 'Login failed');
    } finally {
      loading = false;
    }
  }

  async function handleGoogleAuth() {
    toast.info('Google auth coming soon!');
  }

  async function handleGithubAuth() {
    toast.info('GitHub auth coming soon!');
  }
</script>

<svelte:head>
  <title>Sign In - Exam Platform</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center p-4">
  <button
    on:click={() => goto('/')}
    class="absolute top-4 left-4 flex items-center gap-2 text-white/80 hover:text-white transition-colors"
  >
    <ChevronLeft size={20} />
    <span>Back</span>
  </button>

  <div class="w-full max-w-md">
    <div class="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-8">

      <!-- Header -->
      <div class="text-center mb-8">
        <div class="inline-block p-3 bg-blue-500/20 rounded-full mb-4">
          <svg class="w-12 h-12 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">Welcome Back</h1>
        <p class="text-gray-300">Sign in to your account to continue</p>
      </div>

      <form on:submit|preventDefault={handleSubmit} class="space-y-6">

        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-200 mb-2">
            Email Address
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail size={20} class="text-gray-400" />
            </div>
            <input
              id="email"
              type="email"
              bind:value={email}
              placeholder="you@example.com"
              class="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              required
            />
          </div>
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-200 mb-2">
            Password
          </label>
          <div class="relative">

            <!-- Hidden password -->
            {#if !showPassword}
              <input
                id="password"
                type="password"
                bind:value={password}
                placeholder="••••••••"
                class="w-full pl-10 pr-12 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                required
              />
            {:else}
              <!-- Visible password -->
              <input
                id="password"
                type="text"
                bind:value={password}
                placeholder="••••••••"
                class="w-full pl-10 pr-12 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                required
              />
            {/if}

            <button
              type="button"
              on:click={() => showPassword = !showPassword}
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white"
            >
              {showPassword ? '👁️' : '👁️‍🗨️'}
            </button>
          </div>
        </div>

        <div class="flex items-center justify-between">
          <label class="flex items-center">
            <input type="checkbox" class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
            <span class="ml-2 text-sm text-gray-300">Remember me</span>
          </label>
          <a href="/forgot-password" class="text-sm text-blue-400 hover:text-blue-300">
            Forgot password?
          </a>
        </div>

        <button
          type="submit"
          disabled={loading}
          class="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
        >
          {#if loading}
            <Loader class="animate-spin" size={20} />
            <span>Signing in...</span>
          {:else}
            <span>Sign In</span>
          {/if}
        </button>

      </form>

      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-white/20"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-4 bg-transparent text-gray-400">Or continue with</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <button
          on:click={handleGoogleAuth}
          class="flex items-center justify-center gap-2 py-2 px-4 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white transition-all"
        >
          <span>Google</span>
        </button>

        <button
          on:click={handleGithubAuth}
          class="flex items-center justify-center gap-2 py-2 px-4 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white transition-all"
        >
          <Github size={20} />
          <span>GitHub</span>
        </button>
      </div>

      <p class="mt-6 text-center text-sm text-gray-300">
        Don't have an account?
        <a href="/signup" class="text-blue-400 hover:text-blue-300 font-semibold">
          Sign up
        </a>
      </p>

    </div>
  </div>
</div>

<style>
  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .animate-spin {
    animation: spin 1s linear infinite;
  }
</style>
