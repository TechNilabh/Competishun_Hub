interface Permissions {
  is_camera_enabled: boolean;
  is_mic_enabled: boolean;
  is_screen_shared: boolean;
}

interface CodingSubmissionData {
  session: string;
  problem: string;
  language: string;
  code: string;
}

const API_BASE_URL = 'http://localhost:8000/api';

export async function fetchExams() {
  const response = await fetch(`${API_BASE_URL}/exams/`);
  if (!response.ok) throw new Error('Failed to fetch exams');
  return response.json();
}

export async function createExamSession(examId: string, permissions: Permissions) {
  const response = await fetch(`${API_BASE_URL}/exam-sessions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      exam: examId,
      ...permissions,
    }),
  });
  if (!response.ok) throw new Error('Failed to create exam session');
  return response.json();
}

export async function startExamSession(sessionId: string) {
  const response = await fetch(`${API_BASE_URL}/exam-sessions/${sessionId}/start/`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to start exam session');
  return response.json();
}

export async function getExamQuestions(examId: string) {
  const response = await fetch(`${API_BASE_URL}/exams/${examId}/questions/`);
  if (!response.ok) throw new Error('Failed to fetch questions');
  return response.json();
}

export async function submitQuizAnswer(sessionId: string, questionId: string, answer: string) {
  const response = await fetch(`${API_BASE_URL}/quiz-answers/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session: sessionId,
      question: questionId,
      selected_answer: answer,
    }),
  });
  if (!response.ok) throw new Error('Failed to submit answer');
  return response.json();
}

export async function submitCodingSubmission(data: CodingSubmissionData) {
  const response = await fetch(`${API_BASE_URL}/coding-submissions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to submit code');
  return response.json();
}

export async function getCodingSubmissions(sessionId: string, problemId: string) {
  const response = await fetch(
    `${API_BASE_URL}/coding-submissions/problem_submissions/?session_id=${sessionId}&problem_id=${problemId}`
  );
  if (!response.ok) throw new Error('Failed to fetch submissions');
  return response.json();
}

export async function submitExam(sessionId: string) {
  const response = await fetch(`${API_BASE_URL}/exam-sessions/${sessionId}/submit/`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to submit exam');
  return response.json();
}

export async function getSessionStatus(sessionId: string) {
  const response = await fetch(`${API_BASE_URL}/exam-sessions/${sessionId}/status/`);
  if (!response.ok) throw new Error('Failed to fetch session status');
  return response.json();
}

export async function logProctoringViolation(sessionId: string, violationType: string, description: string) {
  const response = await fetch(`${API_BASE_URL}/proctoring-logs/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session: sessionId,
      violation_type: violationType,
      severity: 'medium',
      description,
    }),
  });
  if (!response.ok) throw new Error('Failed to log violation');
  return response.json();
}