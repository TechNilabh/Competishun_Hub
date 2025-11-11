import { writable } from 'svelte/store';

function createTheme() {
  const defaultTheme = typeof localStorage !== 'undefined'
    ? (localStorage.getItem('theme') === 'dark' ? 'dark' : 'light')
    : 'light';

  const { subscribe, set, update } = writable<'light' | 'dark'>(defaultTheme);

  const applyTheme = (theme: 'light' | 'dark') => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    localStorage.setItem('theme', theme);
    set(theme);
  };

  return {
    subscribe,
    toggle: () => update(t => {
      const next = t === 'light' ? 'dark' : 'light';
      applyTheme(next);
      return next;
    }),
    set: (t: 'light' | 'dark') => applyTheme(t)
  };
}

export const theme = createTheme();
