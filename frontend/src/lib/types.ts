export type CodingSubmission = {
  code: string;
  language: "python" | "cpp" | "javascript";
};

export type CodingResult = {
  passed: number;
  total: number;
  logs: string[];
};

export type MLSubmissionResult = {
  accuracy: number;
  mismatches: number;
  total: number;
};

export type LeaderboardEntry = {
  team: string;
  score: number;
  timestamp: number;
};
