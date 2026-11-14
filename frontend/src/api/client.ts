const getApiBase = (): string => {
  const envUrl = (import.meta as any).env?.VITE_API_URL;
  if (envUrl) {
    return envUrl;
  }
  if (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    return 'http://localhost:8000';
  }
  return '/api';
};

const API_BASE = getApiBase();

export function getAuthToken(): string | null {
  return localStorage.getItem('skillpath_token');
}

export function setAuthToken(token: string) {
  localStorage.setItem('skillpath_token', token);
}

export function clearAuthToken() {
  localStorage.removeItem('skillpath_token');
  localStorage.removeItem('skillpath_user');
}

export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
  let response: Response;
  try {
    response = await fetch(url, {
      ...options,
      headers,
    });
  } catch (netErr: any) {
    throw new Error(
      `Cannot connect to SkillPath backend server (${url}). Please ensure the backend server is running on http://localhost:8000.`
    );
  }

  if (!response.ok) {
    let errMsg = `Server returned error (${response.status}: ${response.statusText})`;
    try {
      const errJson = await response.json();
      if (errJson && errJson.detail) {
        errMsg = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
      }
    } catch {
      try {
        const textErr = await response.text();
        if (textErr && textErr.trim()) {
          errMsg = textErr.length > 200 ? textErr.slice(0, 200) + '...' : textErr;
        }
      } catch {
        // ignore
      }
    }
    throw new Error(errMsg);
  }

  // Handle binary / PDF or text responses if needed
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/pdf')) {
    return response.blob() as unknown as T;
  }

  return response.json();
}

export const api = {
  // Auth
  register: (data: any) => apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data: any) => apiRequest('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  guestLogin: () => apiRequest('/auth/guest', { method: 'POST' }),
  demoLogin: (name: string) => apiRequest(`/auth/demo/${encodeURIComponent(name)}`, { method: 'POST' }),

  // Profile
  getProfile: () => apiRequest('/profile'),
  updateProfile: (data: any) => apiRequest('/profile', { method: 'PUT', body: JSON.stringify(data) }),
  parseResume: (resume_text: string) => apiRequest('/profile/resume', { method: 'POST', body: JSON.stringify({ resume_text }) }),

  // Discovery
  getDiscoveryQuestions: () => apiRequest('/discovery/questions'),
  submitDiscoveryAnswers: (answers: Record<string, any>) => apiRequest('/discovery/submit', { method: 'POST', body: JSON.stringify({ answers }) }),
  getDiscoveryResults: () => apiRequest('/discovery/results'),

  // Careers
  getCareers: () => apiRequest('/careers'),
  getCareerDetails: (id: number) => apiRequest(`/careers/${id}`),
  compareCareers: (career_ids: number[]) => apiRequest('/careers/compare', { method: 'POST', body: JSON.stringify({ career_ids }) }),
  getShortlist: () => apiRequest('/careers/shortlist'),
  addToShortlist: (career_id: number, is_primary = false, notes = '') => apiRequest('/careers/shortlist', { method: 'POST', body: JSON.stringify({ career_id, is_primary, notes }) }),
  getTryItTask: (career_id: number) => apiRequest(`/careers/${career_id}/try-it`),

  // Skills & Coach
  getHowToLearn: (skill_id: number) => apiRequest(`/skills/${skill_id}/how-to-learn`),

  // Roadmap & Sprints
  getRoadmap: () => apiRequest('/roadmap'),
  regenerateRoadmap: () => apiRequest('/roadmap/regenerate', { method: 'POST' }),
  getFirstWeekPlan: () => apiRequest('/roadmap/first-week'),
  updateItemStatus: (item_id: number, status: string) => apiRequest(`/roadmap/${item_id}/status`, { method: 'PUT', body: JSON.stringify({ status }) }),
  getCurrentSprint: () => apiRequest('/sprint/current'),
  completeSprint: (sprint_id: number) => apiRequest('/sprint/complete', { method: 'POST', body: JSON.stringify({ sprint_id }) }),

  // Simulator
  getForecast: () => apiRequest('/simulator/forecast'),
  runScenario: (scenario: any) => apiRequest('/simulator/scenario', { method: 'POST', body: JSON.stringify(scenario) }),
  applyScenario: (scenario: any) => apiRequest('/simulator/apply', { method: 'POST', body: JSON.stringify(scenario) }),

  // Assessments
  generateAssessment: (skill_slug: string) => apiRequest(`/assessments/generate?skill_slug=${encodeURIComponent(skill_slug)}`),
  submitAssessment: (data: any) => apiRequest('/assessments/submit', { method: 'POST', body: JSON.stringify(data) }),

  // Passport
  getPassport: () => apiRequest('/passport'),
  updatePassport: (data: any) => apiRequest('/passport', { method: 'PUT', body: JSON.stringify(data) }),
  getPublicPassport: (slug: string) => apiRequest(`/passport/public/${slug}`),
  verifySkillHash: (skill_id: number) => apiRequest(`/passport/verify/${skill_id}`),
  downloadPassportPdf: () => apiRequest('/passport/pdf'),

  // Interview Coach
  startInterview: (role?: string, difficulty?: string) => apiRequest('/interview/start', { method: 'POST', body: JSON.stringify({ role, difficulty }) }),
  submitInterviewAnswer: (session_id: number, question_id: number, answer_text: string) => apiRequest('/interview/answer', { method: 'POST', body: JSON.stringify({ session_id, question_id, answer_text }) }),
  finishInterview: (session_id: number) => apiRequest(`/interview/finish?session_id=${session_id}`, { method: 'POST' }),
  getInterviewHistory: () => apiRequest('/interview/history'),

  // Career Guide
  getCareerGuide: () => apiRequest('/guide'),
  regenerateCareerGuide: () => apiRequest('/guide/regenerate', { method: 'POST' }),
  downloadGuidePdf: () => apiRequest('/guide/pdf'),

  // AI Mentor
  sendMentorMessage: (message: string) => apiRequest('/mentor/chat', { method: 'POST', body: JSON.stringify({ message }) }),
  getMentorHistory: () => apiRequest('/mentor/history'),
  submitMentorFeedback: (message_id: number, feedback: string, notes?: string) => apiRequest('/mentor/feedback', { method: 'POST', body: JSON.stringify({ message_id, feedback, notes }) }),

  // General & Analytics
  getMatch: (career_id?: number) => apiRequest(`/match${career_id ? `?career_id=${career_id}` : ''}`),
  getSkillAnalysis: () => apiRequest('/analysis'),
  getProgress: () => apiRequest('/progress'),
  getAgentLogs: () => apiRequest('/agents/logs'),
  getGlossary: (category = '') => apiRequest(`/glossary${category ? `?category=${category}` : ''}`),
  getResources: (skill_slug = '', type = '') => apiRequest(`/resources?skill_slug=${skill_slug}&type=${type}`),

  // Admin
  getCohortGaps: (cohort_id = 1) => apiRequest(`/admin/cohort-gaps?cohort_id=${cohort_id}`),
  getAdminLearners: () => apiRequest('/admin/learners'),

  // Practice Questions
  getPracticeCategories: () => apiRequest('/practice/categories'),
  getPracticeQuestions: (params: { category?: string; difficulty?: string; status?: string } = {}) => {
    const query = new URLSearchParams();
    if (params.category && params.category !== 'all') query.append('category', params.category);
    if (params.difficulty && params.difficulty !== 'all') query.append('difficulty', params.difficulty);
    if (params.status && params.status !== 'all') query.append('status', params.status);
    const qs = query.toString();
    return apiRequest(`/practice/questions${qs ? `?${qs}` : ''}`);
  },
  getQuestionDetail: (id: number) => apiRequest(`/practice/questions/${id}`),
  updateQuestionProgress: (id: number, data: { status?: string; solution_code?: string }) =>
    apiRequest(`/practice/questions/${id}/progress`, { method: 'POST', body: JSON.stringify(data) }),
  getPracticeStats: () => apiRequest('/practice/stats'),

  // i18n
  getI18n: (lang: string) => apiRequest(`/i18n/${lang}`),
};

