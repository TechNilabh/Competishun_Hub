import { writable, derived } from 'svelte/store';
import type { ExamSession, QuizQuestion, QuizAnswer, CodingProblem } from '$lib/types/exam';

interface ExamState {
  session: ExamSession | null;
  quizQuestions: QuizQuestion[];
  codingProblems: CodingProblem[];
  quizAnswers: Map<string, QuizAnswer>;
  currentQuestionIndex: number;
  timeRemaining: number;
  isQuizPhase: boolean;
}

const initialState: ExamState = {
  session: null,
  quizQuestions: [],
  codingProblems: [],
  quizAnswers: new Map(),
  currentQuestionIndex: 0,
  timeRemaining: 0,
  isQuizPhase: true,
};

export const examStore = writable<ExamState>(initialState);

export const currentQuestion = derived(
  examStore,
  ($examStore) => $examStore.quizQuestions[$examStore.currentQuestionIndex] || null
);

export const questionStatuses = derived(
  examStore,
  ($examStore) => {
    const statuses = new Map<string, 'unattempted' | 'attempted' | 'solved'>();
    
    $examStore.quizQuestions.forEach((question) => {
      const answer = $examStore.quizAnswers.get(question.id);
      if (!answer || !answer.selected_answer) {
        statuses.set(question.id, 'unattempted');
      } else {
        statuses.set(question.id, 'attempted');
      }
    });
    
    return statuses;
  }
);

export const examProgress = derived(
  examStore,
  ($examStore) => {
    const total = $examStore.quizQuestions.length;
    const attempted = Array.from($examStore.quizAnswers.values()).filter(
      (a) => a.selected_answer
    ).length;
    
    return {
      total,
      attempted,
      unattempted: total - attempted,
      percentage: total > 0 ? (attempted / total) * 100 : 0,
    };
  }
);