<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore } from '$lib/stores/auth';
  import { toast } from 'svelte-sonner';
  import { ChevronLeft, Loader, Mail, Lock, User } from 'lucide-svelte';

  let name = '';
  let email = '';
  let password = '';
  let confirmPassword = '';
  let loading = false;
  let showPassword = false;
  let agreeToTerms = false;

  async function handleSubmit() {
    if (!name || !email || !password || !confirmPassword) {
      toast.error('Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }

    if (!agreeToTerms) {
      toast.error('Please agree to terms and conditions');
      return;
    }

    loading = true;

    try {
      await authStore.signup(email, password, name);
      toast.success('Account created successfully!');
      goto('/team/create');
    } catch (error: any) {
      toast.error(error.message || 'Signup failed');
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Sign Up - Exam Platform</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-pink-900 flex items-center justify-center p-4">
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
        <div class="inline-block p-3 bg-purple-500/20 rounded-full mb-4">
          <svg class="w-12 h-12 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">Create Account</h1>
        <p class="text-gray-300">Join us and start your journey</p>
      </div>

      <form on:submit|preventDefault={handleSubmit} class="space-y-5">
        <!-- Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-200 mb-2">
            Full Name
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User size={20} class="text-gray-400" />
            </div>
            <input
              id="name"
              type="text"
              bind:value={name}
              placeholder="John Doe"
              class="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400
                focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              required
            />
          </div>
        </div>

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
              class="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400
                focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
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
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock size={20} class="text-gray-400" />
            </div>

            {#if showPassword}
              <input
                id="password"
                type="text"
                bind:value={password}
                placeholder="••••••••"
                class="w-full pl-10 pr-12 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400
                  focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                required
              />
            {:else}
              <input
                id="password"
                type="password"
                bind:value={password}
                placeholder="••••••••"
                class="w-full pl-10 pr-12 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400
                  focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
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

        <!-- Confirm Password -->
        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-200 mb-2">
            Confirm Password
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock size={20} class="text-gray-400" />
            </div>
            <input
              id="confirmPassword"
              type="password"
              bind:value={confirmPassword}
              placeholder="••••••••"
              class="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400
                focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              required
            />
          </div>
        </div>

        <!-- Terms -->
        <label class="flex items-start gap-2">
          <input
            type="checkbox"
            bind:checked={agreeToTerms}
            class="w-4 h-4 mt-1 rounded border-gray-300 text-purple-600 focus:ring-purple-500"
          />
          <span class="text-sm text-gray-300">
            I agree to the <a href="/terms" class="text-purple-400 hover:text-purple-300">Terms of Service</a>
            and <a href="/privacy" class="text-purple-400 hover:text-purple-300">Privacy Policy</a>
          </span>
        </label>

        <!-- Submit -->
        <button
          type="submit"
          disabled={loading}
          class="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500
            text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed
            disabled:transform-none flex items-center justify-center gap-2"
        >
          {#if loading}
            <Loader class="animate-spin" size={20} />
            <span>Creating account...</span>
          {:else}
            <span>Create Account</span>
          {/if}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-gray-300">
        Already have an account?
        <a href="/signin" class="text-purple-400 hover:text-purple-300 font-semibold">
          Sign in
        </a>
      </p>
    </div>
  </div>
</div>
