export interface Exam {
  id: string;
  title: string;
  description: string;
  duration_minutes: number;
  quiz_duration_minutes: number;
  is_active: boolean;
}
export interface User {
  id: string;
  email: string;
  name: string;
  roll_number?: string;
  created_at?: string;
}
export interface ExamSession {
  id: string;
  user: User;
  exam: Exam;
  status: 'not_started' | 'in_progress' | 'completed' | 'disqualified';
  started_at: string | null;
  submitted_at: string | null;
  quiz_score: number;
  coding_score: number;
  total_score: number;
  violation_count: number;
  is_camera_enabled: boolean;
  is_mic_enabled: boolean;
  is_screen_shared: boolean;
}

export interface QuizQuestion {
  id: string;
  question_text: string;
  option_a: string;
  option_b: string;
  option_c?: string;
  option_d?: string;
  marks: number;
  difficulty: string;
  category: string;
  order: number;
}

export interface QuizAnswer {
  id: string;
  session: string;
  question: string;
  selected_answer: string;
  is_correct: boolean;
  answered_at: string;
}

export interface CodingProblem {
  id: string;
  title: string;
  description: string;
  input_format: string;
  output_format: string;
  constraints: string;
  sample_input: string;
  sample_output: string;
  difficulty: string;
  max_marks: number;
  order: number;
  test_cases: TestCase[];
}

export interface TestCase {
  id: string;
  input_data: string;
  expected_output: string;
  is_sample: boolean;
  marks: number;
}

export interface CodingSubmission {
  id: string;
  session: string;
  problem: string;
  language: string;
  code: string;
  status: string;
  score: number;
  test_cases_passed: number;
  total_test_cases: number;
  execution_time_ms: number;
  memory_used_kb: number;
  error_message?: string;
  submitted_at: string;
}

export interface ProctoringLog {
  id: string;
  session: string;
  violation_type: string;
  severity: string;
  description: string;
  timestamp: string;
}

export type QuestionStatus = 'unattempted' | 'attempted' | 'solved';