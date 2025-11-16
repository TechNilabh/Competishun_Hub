import { writable } from 'svelte/store';

interface TeamMember {
  id: string;
  email: string;
  name: string;
  role: 'leader' | 'member';
  status: 'pending' | 'accepted';
}

interface Team {
  id: string;
  name: string;
  description: string;
  leader: string;
  members: TeamMember[];
  maxMembers: number;
  createdAt: string;
}

interface TeamState {
  team: Team | null;
  loading: boolean;
  error: string | null;
}

const initialState: TeamState = {
  team: null,
  loading: false,
  error: null,
};

function createTeamStore() {
  // Removed `set` since it was unused
  const { subscribe, update } = writable<TeamState>(initialState);

  const getToken = (): string | null => localStorage.getItem('auth_token');

  const loadTeam = async (teamId: string): Promise<void> => {
    update(state => ({ ...state, loading: true, error: null }));

    try {
      const token = getToken();
      const response = await fetch(`http://localhost:8000/api/teams/${teamId}/`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });

      if (!response.ok) throw new Error('Failed to load team');

      const team: Team = await response.json();
      update(state => ({ ...state, team, loading: false }));
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to load team';
      update(state => ({ ...state, loading: false, error: message }));
    }
  };

  const createTeam = async (
    teamData: { name: string; description: string; maxMembers: number }
  ): Promise<Team> => {
    update(state => ({ ...state, loading: true, error: null }));

    try {
      const token = getToken();
      const response = await fetch('http://localhost:8000/api/teams/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(teamData),
      });

      if (!response.ok) throw new Error('Failed to create team');

      const team: Team = await response.json();
      update(state => ({ ...state, team, loading: false }));
      return team;
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to create team';
      update(state => ({ ...state, loading: false, error: message }));
      throw error; // not "useless" since we update state
    }
  };

  const inviteMember = async (teamId: string, email: string): Promise<unknown> => {
    // Removed try/catch that only rethrew (no-useless-catch)
    const token = getToken();
    const response = await fetch(`http://localhost:8000/api/teams/${teamId}/invite/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ email }),
    });

    if (!response.ok) throw new Error('Failed to send invite');

    const result = await response.json();
    await loadTeam(teamId); 
    return result;
  };

  return {
    subscribe,
    createTeam,
    inviteMember,
    loadTeam,
  };
}

export const teamStore = createTeamStore();