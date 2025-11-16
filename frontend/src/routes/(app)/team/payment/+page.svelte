<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { createCheckoutSession } from '$lib/utils/stripe';
  import { toast } from 'svelte-sonner';
  import { Check, CreditCard, Shield, Lock, Loader } from 'lucide-svelte';
  
  let teamId = '';
  let selectedPlan = 'standard';
  let loading = false;
  
  const plans = [
    {
      id: 'basic',
      name: 'Basic',
      price: 499,
      features: [
        'Access to 1 hackathon',
        'Basic proctoring',
        'Email support',
        'Certificate of participation',
      ],
      popular: false,
    },
    {
      id: 'standard',
      name: 'Standard',
      price: 999,
      features: [
        'Access to 3 hackathons',
        'Advanced proctoring',
        'Priority support',
        'Certificates + Badges',
        'Team analytics',
      ],
      popular: true,
    },
    {
      id: 'premium',
      name: 'Premium',
      price: 1999,
      features: [
        'Unlimited hackathons',
        'AI-powered proctoring',
        '24/7 dedicated support',
        'All certificates & badges',
        'Advanced team analytics',
        'Exclusive workshops',
      ],
      popular: false,
    },
  ];
  
  onMount(() => {
    teamId = $page.url.searchParams.get('team_id') || '';
    if (!teamId) {
      toast.error('No team ID provided');
      goto('/team/create');
    }
  });
  
  async function handlePayment() {
    loading = true;
    
    try {
      await createCheckoutSession(teamId, selectedPlan);
    } catch (error: any) {
      toast.error(error.message || 'Payment failed');
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Payment - Exam Platform</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 py-12 px-4">
  <div class="max-w-7xl mx-auto">
    
    <div class="text-center mb-12">
      <div class="inline-block p-4 bg-blue-500/20 rounded-full mb-4">
        <CreditCard size={48} class="text-blue-400" />
      </div>
      <h1 class="text-4xl font-bold text-white mb-3">Choose Your Plan</h1>
      <p class="text-xl text-gray-300">Select the perfect plan for your team</p>
    </div>
    
    <div class="mb-12">
      <div class="flex items-center justify-center">
        <div class="flex items-center">
          <div class="flex items-center justify-center w-10 h-10 rounded-full bg-green-500 text-white font-semibold">✓</div>
          <div class="w-20 h-1 bg-green-500"></div>
          <div class="flex items-center justify-center w-10 h-10 rounded-full bg-green-500 text-white font-semibold">✓</div>
          <div class="w-20 h-1 bg-blue-500"></div>
          <div class="flex items-center justify-center w-10 h-10 rounded-full bg-blue-500 text-white font-semibold">3</div>
        </div>
      </div>
      <div class="flex justify-center gap-24 mt-2">
        <span class="text-sm text-green-400 font-semibold">Team Info</span>
        <span class="text-sm text-green-400 font-semibold">Invites</span>
        <span class="text-sm text-blue-400 font-semibold">Payment</span>
      </div>
    </div>
    <div class="grid md:grid-cols-3 gap-8 mb-12">
      {#each plans as plan}
        <div class="relative">
          {#if plan.popular}
            <div class="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
              <span class="bg-gradient-to-r from-yellow-400 to-orange-500 text-black px-4 py-1 rounded-full text-sm font-bold">
                MOST POPULAR
              </span>
            </div>
          {/if}
          
          <div
            class="h-full bg-white/10 backdrop-blur-lg rounded-2xl border-2 {selectedPlan === plan.id ? 'border-blue-500' : 'border-white/20'} p-8 transition-all duration-300 hover:scale-105 cursor-pointer"
            class:ring-4={selectedPlan === plan.id}
            class:ring-blue-500={selectedPlan === plan.id}
            on:click={() => selectedPlan = plan.id}
          >
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-white mb-2">{plan.name}</h3>
              <div class="flex items-center justify-center gap-1">
                <span class="text-4xl font-bold text-white">₹{plan.price}</span>
                <span class="text-gray-400">/team</span>
              </div>
            </div>
            
            
            <ul class="space-y-4 mb-8">
              {#each plan.features as feature}
                <li class="flex items-start gap-3 text-gray-200">
                  <Check size={20} class="text-green-400 flex-shrink-0 mt-0.5" />
                  <span>{feature}</span>
                </li>
              {/each}
            </ul>
            
            <button
              type="button"
              on:click={() => selectedPlan = plan.id}
              class="w-full py-3 px-4 rounded-lg font-semibold transition-all {
                selectedPlan === plan.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-white/10 text-white hover:bg-white/20'
              }"
            >
              {selectedPlan === plan.id ? 'Selected' : 'Select Plan'}
            </button>
          </div>
        </div>
      {/each}
    </div>
    
    <div class="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6 mb-8">
      <div class="flex items-center justify-center gap-8">
        <div class="flex items-center gap-3">
          <Shield size={24} class="text-green-400" />
          <span class="text-white">SSL Secured</span>
        </div>
        <div class="flex items-center gap-3">
          <Lock size={24} class="text-blue-400" />
          <span class="text-white">256-bit Encryption</span>
        </div>
        <div class="flex items-center gap-3">
          <svg class="w-12 h-6" viewBox="0 0 48 24" fill="none">
            <rect width="48" height="24" rx="4" fill="#635BFF"/>
            <text x="50%" y="50%" fill="white" font-size="10" font-weight="bold" text-anchor="middle" dominant-baseline="middle">stripe</text>
          </svg>
          <span class="text-white">Powered by Stripe</span>
        </div>
      </div>
    </div>
    
    <div class="flex gap-4 justify-center">
      <button
        on:click={() => goto('/team/create')}
        class="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
      >
        Back
      </button>
      
      <button
        on:click={handlePayment}
        disabled={loading}
        class="px-12 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center gap-2"
      >
        {#if loading}
          <Loader class="animate-spin" size={20} />
          <span>Processing...</span>
        {:else}
          <CreditCard size={20} />
          <span>Proceed to Payment</span>
        {/if}
      </button>
    </div>
    
    <div class="text-center mt-8">
      <p class="text-gray-300">
        <strong class="text-white">30-day money-back guarantee.</strong> Not satisfied? Get a full refund, no questions asked.
      </p>
    </div>
  </div>
</div>