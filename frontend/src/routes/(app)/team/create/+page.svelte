<script lang="ts">
  import { goto } from '$app/navigation';
  import { teamStore } from '$lib/stores/team';
  import { authStore } from '$lib/stores/auth';
  import { toast } from 'svelte-sonner';
  import { Users, Mail, Plus, Trash2, Loader, CreditCard } from 'lucide-svelte';
  
  let teamName = '';
  let teamDescription = '';
  let maxMembers = 4;
  let inviteEmails: string[] = [''];
  let loading = false;
  
  function addEmailField() {
    if (inviteEmails.length < maxMembers - 1) {
      inviteEmails = [...inviteEmails, ''];
    } else {
      toast.error(`Maximum ${maxMembers - 1} additional members allowed`);
    }
  }
  
  function removeEmailField(index: number) {
    inviteEmails = inviteEmails.filter((_, i) => i !== index);
  }
  
  async function handleCreateTeam() {
    if (!teamName.trim()) {
      toast.error('Please enter team name');
      return;
    }
    
    if (!teamDescription.trim()) {
      toast.error('Please enter team description');
      return;
    }
    
    loading = true;
    
    try {
      const team = await teamStore.createTeam({
        name: teamName,
        description: teamDescription,
        maxMembers,
      });
      
      const validEmails = inviteEmails.filter(email => email.trim() !== '');
      
      for (const email of validEmails) {
        try {
          await teamStore.inviteMember(team.id, email);
        } catch (error) {
          console.error(`Failed to invite ${email}:`, error);
        }
      }
      
      toast.success('Team created successfully!');
      
      goto(`/team/payment?team_id=${team.id}`);
      
    } catch (error: any) {
      toast.error(error.message || 'Failed to create team');
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Create Team - Exam Platform</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900 to-purple-900 py-12 px-4">
  <div class="max-w-4xl mx-auto">
    
    <div class="text-center mb-12">
      <div class="inline-block p-4 bg-indigo-500/20 rounded-full mb-4">
        <Users size={48} class="text-indigo-400" />
      </div>
      <h1 class="text-4xl font-bold text-white mb-3">Create Your Team</h1>
      <p class="text-xl text-gray-300">Build your hackathon squad</p>
    </div>
    
    <div class="mb-12">
      <div class="flex items-center justify-center">
        <div class="flex items-center">
          <div class="flex items-center justify-center w-10 h-10 rounded-full bg-indigo-500 text-white font-semibold">1</div>
          <div class="w-20 h-1 bg-indigo-500"></div>
          <div class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-700 text-white font-semibold">2</div>
          <div class="w-20 h-1 bg-gray-700"></div>
          <div class="flex items-center justify-center w-10 h-10 rounded-full bg-gray-700 text-white font-semibold">3</div>
        </div>
      </div>
      <div class="flex justify-center gap-24 mt-2">
        <span class="text-sm text-indigo-400 font-semibold">Team Info</span>
        <span class="text-sm text-gray-400">Invites</span>
        <span class="text-sm text-gray-400">Payment</span>
      </div>
    </div>
    
    <div class="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 p-8">
      <form on:submit|preventDefault={handleCreateTeam} class="space-y-8">
      
        <div>
          <h2 class="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <Users size={24} class="text-indigo-400" />
            Team Details
          </h2>
          
          <div class="space-y-6">
          
            <div>
              <label for="teamName" class="block text-sm font-medium text-gray-200 mb-2">
                Team Name <span class="text-red-400">*</span>
              </label>
              <input
                id="teamName"
                type="text"
                bind:value={teamName}
                placeholder="e.g., Code Warriors"
                class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                required
              />
            </div>
            
            <div>
              <label for="teamDescription" class="block text-sm font-medium text-gray-200 mb-2">
                Team Description <span class="text-red-400">*</span>
              </label>
              <textarea
                id="teamDescription"
                bind:value={teamDescription}
                placeholder="Tell us about your team..."
                rows="4"
                class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
                required
              />
              <p class="mt-2 text-sm text-gray-400">{teamDescription.length}/500 characters</p>
            </div>
            
            <div>
              <label for="maxMembers" class="block text-sm font-medium text-gray-200 mb-2">
                Team Size
              </label>
              <select
                id="maxMembers"
                bind:value={maxMembers}
                class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              >
                <option value={2}>2 Members</option>
                <option value={3}>3 Members</option>
                <option value={4}>4 Members</option>
                <option value={5}>5 Members</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="border-t border-white/20"></div>
        
        <div>
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-white flex items-center gap-2">
              <Mail size={24} class="text-indigo-400" />
              Invite Members
            </h2>
            <button
              type="button"
              on:click={addEmailField}
              class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors"
              disabled={inviteEmails.length >= maxMembers - 1}
            >
              <Plus size={18} />
              Add Member
            </button>
          </div>
          
          <div class="space-y-4">
            {#each inviteEmails as email, index}
              <div class="flex gap-3">
                <div class="flex-1 relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail size={20} class="text-gray-400" />
                  </div>
                  <input
                    type="email"
                    bind:value={inviteEmails[index]}
                    placeholder="teammate@example.com"
                    class="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  />
                </div>
                <button
                  type="button"
                  on:click={() => removeEmailField(index)}
                  class="p-3 bg-red-600 hover:bg-red-500 text-white rounded-lg transition-colors"
                  disabled={inviteEmails.length === 1}
                >
                  <Trash2 size={20} />
                </button>
              </div>
            {/each}
          </div>
          
          <p class="mt-4 text-sm text-gray-400">
             Tip: You can add more members later from your team dashboard
          </p>
        </div>
        
        <div class="flex gap-4 pt-6">
          <button
            type="button"
            on:click={() => goto('/exam')}
            class="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
          >
            Cancel
          </button>
          
          <button
            type="submit"
            disabled={loading}
            class="flex-1 py-3 px-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold rounded-lg transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
          >
            {#if loading}
              <Loader class="animate-spin" size={20} />
              <span>Creating Team...</span>
            {:else}
              <CreditCard size={20} />
              <span>Continue to Payment</span>
            {/if}
          </button>
        </div>
      </form>
    </div>
    <div class="grid md:grid-cols-3 gap-6 mt-8">

  <div class="bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 p-6 text-center">
    <img 
      src="https://res.cloudinary.com/dg361q5uv/image/upload/v1763215548/DALL_E_2025-11-15_19.31.42_-_A_clean_2.5D_futuristic_icon-style_illustration_representing_teamwork_in_hackathons__a_small_group_of_simplified_characters_collaborating_around_a_glo_k2grkf.webp"
      alt="Compete Together"
      class="w-20 h-20 mx-auto mb-4 object-contain rounded-lg shadow-lg"
    />
    <h3 class="text-lg font-semibold text-white mb-2">Compete Together</h3>
    <p class="text-sm text-gray-300">Join hackathons as a team and win amazing prizes</p>
  </div>

  <div class="bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 p-6 text-center">
    <img 
      src="https://res.cloudinary.com/dg361q5uv/image/upload/v1763215556/Gemini_Generated_Image_k53xl7k53xl7k53x_1_fttkba.png"
      alt="One Payment"
      class="w-20 h-20 mx-auto mb-4 object-contain rounded-lg shadow-lg"
    />
    <h3 class="text-lg font-semibold text-white mb-2">One Payment</h3>
    <p class="text-sm text-gray-300">Register your entire team with a single payment</p>
  </div>

  <div class="bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 p-6 text-center">
    <img 
      src="https://res.cloudinary.com/dg361q5uv/image/upload/v1763215552/Gemini_Generated_Image_d5dxutd5dxutd5dx_1_viipsq.png"
      alt="Track Progress"
      class="w-20 h-20 mx-auto mb-4 object-contain rounded-lg shadow-lg"
    />
    <h3 class="text-lg font-semibold text-white mb-2">Track Progress</h3>
    <p class="text-sm text-gray-300">Monitor your team's performance in real-time</p>
  </div>

</div>

  </div>
</div>