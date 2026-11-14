import {
  MOCK_CATEGORIES,
  MOCK_QUESTIONS,
  MOCK_PRACTICE_STATS,
  MOCK_PROFILE,
  MOCK_MATCH,
  MOCK_ROADMAP,
  MOCK_CAREERS,
  MOCK_AGENT_LOGS,
  MOCK_PROGRESS,
  MOCK_FIRST_WEEK,
  MOCK_CURRENT_SPRINT,
} from './mockData';

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

function getMockFallback(endpoint: string): any {
  const cleanEndpoint = endpoint.split('?')[0];

  if (cleanEndpoint.startsWith('/auth/demo/')) {
    const name = decodeURIComponent(cleanEndpoint.replace('/auth/demo/', '')).toLowerCase();
    return {
      access_token: 'demo-jwt-token-' + name,
      token_type: 'bearer',
      user_id: name === 'admin' ? 99 : 1,
      email: `${name}@skillpath.dev`,
      role: name === 'admin' ? 'admin' : 'learner',
      full_name:
        name === 'admin'
          ? 'Dr. Sarah Jenkins'
          : name === 'priya'
          ? 'Priya Sharma'
          : name === 'rohan'
          ? 'Rohan Patel'
          : 'Arif Mohamed',
      career_goal: name === 'rohan' ? 'Full Stack Developer' : 'AI/ML Engineer',
      goal_status: 'known',
    };
  }
  if (cleanEndpoint === '/auth/guest') {
    return {
      access_token: 'guest-jwt-token',
      token_type: 'bearer',
      user_id: 100,
      email: 'guest@skillpath.dev',
      role: 'learner',
      full_name: 'Guest Learner',
      career_goal: 'Explore Careers',
      goal_status: 'unknown',
    };
  }
  if (cleanEndpoint === '/profile') {
    return MOCK_PROFILE;
  }
  if (cleanEndpoint === '/match') {
    return MOCK_MATCH;
  }
  if (cleanEndpoint === '/roadmap') {
    return MOCK_ROADMAP;
  }
  if (cleanEndpoint === '/roadmap/first-week') {
    return MOCK_FIRST_WEEK;
  }
  if (cleanEndpoint === '/sprint/current') {
    return MOCK_CURRENT_SPRINT;
  }
  if (cleanEndpoint === '/progress') {
    return MOCK_PROGRESS;
  }
  if (cleanEndpoint === '/agents/logs') {
    return MOCK_AGENT_LOGS;
  }
  if (cleanEndpoint === '/careers') {
    return MOCK_CAREERS;
  }
  if (cleanEndpoint === '/practice/categories') {
    return MOCK_CATEGORIES;
  }
  if (cleanEndpoint === '/practice/questions') {
    const params = new URLSearchParams(endpoint.includes('?') ? endpoint.split('?')[1] : '');
    const cat = params.get('category');
    const diff = params.get('difficulty');
    let filtered = [...MOCK_QUESTIONS];
    if (cat && cat !== 'all') {
      filtered = filtered.filter(
        (q) => q.category_slug === cat || q.category.toLowerCase() === cat.toLowerCase()
      );
    }
    if (diff && diff !== 'all') {
      filtered = filtered.filter(
        (q) => q.difficulty.toLowerCase() === diff.toLowerCase()
      );
    }
    return filtered;
  }
  if (cleanEndpoint.startsWith('/practice/questions/')) {
    const parts = cleanEndpoint.split('/');
    const id = parseInt(parts[3], 10);
    const q = MOCK_QUESTIONS.find((item) => item.id === id) || MOCK_QUESTIONS[0];
    return q;
  }
  if (cleanEndpoint === '/practice/stats') {
    return MOCK_PRACTICE_STATS;
  }
  if (cleanEndpoint === '/analysis') {
    return {
      strengths: ['Python Programming', 'NumPy', 'Data Structures', 'Problem Solving'],
      gaps: ['MLOps Deployment', 'PyTorch Tensors', 'Docker Pipelines'],
      radar_scores: [
        { subject: 'Programming', score: 85, fullMark: 100 },
        { subject: 'Algorithms', score: 78, fullMark: 100 },
        { subject: 'System Design', score: 62, fullMark: 100 },
        { subject: 'Machine Learning', score: 80, fullMark: 100 },
        { subject: 'Cloud & DevOps', score: 55, fullMark: 100 },
      ],
    };
  }
  if (cleanEndpoint === '/glossary') {
    return [
      {
        term: 'Machine Learning',
        definition: 'The study of computer algorithms that improve automatically through experience and data.',
        category: 'AI',
      },
      {
        term: 'Supervised Learning',
        definition: 'Training a model on labeled training data.',
        category: 'AI',
      },
      {
        term: 'Gradient Descent',
        definition: 'Optimization algorithm used to minimize loss functions.',
        category: 'Math',
      },
    ];
  }
  if (cleanEndpoint === '/mentor/history') {
    return [
      {
        id: 1,
        role: 'assistant',
        content: 'Hello Arif! I am your SkillPath AI Mentor. How can I assist your learning path today?',
        created_at: new Date().toISOString(),
      },
    ];
  }
  if (cleanEndpoint === '/mentor/chat') {
    return {
      id: 2,
      role: 'assistant',
      content:
        'Great question! Focus on building hands-on projects with PyTorch and practicing algorithms daily. You are making great progress towards your goal as an AI/ML Engineer!',
      created_at: new Date().toISOString(),
    };
  }
  return null;
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
    const fallback = getMockFallback(endpoint);
    if (fallback !== null) {
      return fallback as T;
    }
    throw new Error(
      `Cannot connect to SkillPath backend server (${url}). Please ensure the backend server is running on http://localhost:8000.`
    );
  }

  if (!response.ok) {
    // If backend returns 404/502 on remote hosting without route, try fallback
    const fallback = getMockFallback(endpoint);
    if (fallback !== null && (response.status === 404 || response.status >= 500)) {
      return fallback as T;
    }

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

