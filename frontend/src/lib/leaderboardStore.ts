import { writable } from "svelte/store";
import type { LeaderboardEntry } from "./types";

export const leaderboard = writable<LeaderboardEntry[]>([]);
