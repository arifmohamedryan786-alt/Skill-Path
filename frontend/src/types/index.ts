export type Role = 'learner' | 'admin';

export interface User {
  id: number;
  email: string;
  role: Role;
  full_name: string;
  name?: string;
  career_goal?: string;
  goal_status?: 'known' | 'rough' | 'unknown';
  profile?: Profile;
}

export interface AssessmentOut {
  id: number;
  skill_slug: string;
  title: string;
  description: string;
  passing_score: number;
  target_level?: number;
  questions: Array<{
    id: number;
    question: string;
    options: string[];
    explanation?: string;
  }>;
  practical_task?: {
    prompt: string;
    starter_code?: string;
    hint?: string;
    test_cases?: Array<{ input: string; expected: string }>;
  };
}

export interface Profile {
  id: number;
  user_id: number;
  full_name: string;
  education: string;
  branch: string;
  year: number;
  institution: string;
  interests: string[];
  strengths: string[];
  certifications: string[];
  projects: Array<{ title: string; description: string }>;
  career_goal: string;
  goal_status: 'known' | 'rough' | 'unknown';
  weekly_hours: number;
  language: string;
  learner_pace_factor: number;
  cohort_id?: number | null;
}

export interface CareerMatch {
  career_id: number;
  slug: string;
  name: string;
  match_pct: number;
  plain_reason: string;
  suits_who: string;
  demand_level: string;
  entry_titles: string[];
}

export interface CareerDetail {
  id: number;
  slug: string;
  name: string;
  plain_description: string;
  demand_level: string;
  salary_range_note: string;
  suits_who: string;
  entry_titles: string[];
  day_in_life: string;
  typical_tasks: string[];
  growth_path: string[];
  mini_project: {
    title: string;
    duration: string;
    description: string;
    steps: string[];
    starter_code?: string;
    expected_outcome: string;
  };
  skills: Array<{
    skill_id: number;
    name: string;
    category: string;
    target_level: number;
    weight: number;
    plain_explanation: string;
  }>;
}

export interface RoadmapItem {
  id: number;
  stage_id: number;
  skill_id?: number | null;
  title: string;
  description: string;
  item_type: 'skill' | 'project' | 'milestone' | 'internship' | 'certification' | 'remedial';
  order: number;
  status: 'pending' | 'in_progress' | 'completed' | 'skipped';
  due_week: number;
  est_hours: number;
  completed_at?: string | null;
}

export interface RoadmapStage {
  id: number;
  stage_number: number;
  title: string;
  description: string;
  status: 'locked' | 'current' | 'completed';
  est_weeks: number;
  items: RoadmapItem[];
}

export interface RoadmapData {
  career_goal: string;
  total_stages: number;
  completed_stages: number;
  overall_progress_pct: number;
  stages: RoadmapStage[];
  adjusted_for_year: number;
  timeline_view: { total_weeks: number; view_mode: string };
}

export interface HowToLearnCard {
  skill_id: number;
  slug: string;
  name: string;
  category: string;
  plain_explanation: string;
  why_it_matters: string;
  prerequisites: string[];
  current_level: number;
  target_level: number;
  estimated_hours: number;
  estimated_weeks: number;
  weekly_hours_assumed: number;
  learning_method: {
    watch_pct: number;
    practice_pct: number;
    build_pct: number;
    first_step: string;
    tip: string;
  };
  recommended_first_step: string;
  resources: Array<{
    id: number;
    title: string;
    type: string;
    url: string;
    difficulty: string;
    duration: string;
    provider: string;
    free: boolean;
  }>;
  common_mistakes: string[];
  done_criteria: string[];
  mini_exercise: {
    title: string;
    prompt: string;
    duration: string;
  };
}

export interface ForecastData {
  career_goal: string;
  current_match_pct: number;
  total_gap_hours: number;
  weekly_hours: number;
  learner_pace_factor: number;
  optimistic_date: string;
  realistic_date: string;
  optimistic_weeks: number;
  realistic_weeks: number;
  readiness_label: string;
  explanation: string;
  gaps_count: number;
  comparison_scenarios: Array<{
    name: string;
    target_career: string;
    weekly_hours: number;
    pace_factor: number;
    optimistic_date: string;
    realistic_date: string;
    total_hours_needed: number;
    weeks_needed: number;
    match_pct_4w: number;
    match_pct_8w: number;
    match_pct_12w: number;
    projection_points: Array<{ week: number; match: number; label?: string }>;
    explanation: string;
  }>;
}

export interface VerifiedSkill {
  id: number;
  skill_id: number;
  skill_name: string;
  category: string;
  verified_level: number;
  score_pct: number;
  evidence_type: string;
  evidence_ref: string;
  verification_hash: string;
  verified_at: string;
}

export interface PassportData {
  id: number;
  slug: string;
  full_name: string;
  target_career: string;
  readiness_pct: number;
  is_public: boolean;
  show_scores: boolean;
  show_evidence: boolean;
  verified_skills: VerifiedSkill[];
  all_skills: Array<{ skill_id: number; name: string; level: number; source: string }>;
  public_url: string;
  qr_data_url: string;
}

export interface GlossaryItem {
  id: number;
  term: string;
  category: string;
  plain_meaning: string;
  example: string;
}

export interface AgentLogItem {
  id: number;
  agent_name: string;
  action: string;
  reason: string;
  details: Record<string, any>;
  created_at: string;
}

export interface PracticeCategory {
  id: string;
  name: string;
  slug: string;
  description: string;
  icon: string;
  total_questions: number;
  completed_questions: number;
  attempted_questions: number;
  beginner_count: number;
  intermediate_count: number;
  advanced_count: number;
}

export interface PracticeQuestionSummary {
  id: number;
  category: string;
  category_slug: string;
  title: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  description: string;
  order_index: number;
  user_status: 'not_started' | 'attempted' | 'completed';
  has_saved_code: boolean;
}

export interface PracticeQuestionDetail {
  id: number;
  category: string;
  category_slug: string;
  title: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  description: string;
  example_input: string;
  example_output: string;
  hint: string;
  starter_code: string;
  solution: string;
  explanation: string;
  approach: string;
  time_complexity: string;
  space_complexity: string;
  order_index: number;
  user_status: 'not_started' | 'attempted' | 'completed';
  user_solution_code: string;
  completed_at?: string | null;
  next_question_id?: number | null;
  prev_question_id?: number | null;
}

export interface PracticeStats {
  total_completed: number;
  total_attempted: number;
  total_questions: number;
  completion_pct: number;
  current_streak: number;
  by_category: Record<string, { slug: string; completed: number; total: number; pct: number }>;
  by_difficulty: Record<string, { completed: number; total: number; pct: number }>;
  recent_activity: Array<{
    question_id: number;
    title: string;
    category: string;
    difficulty: string;
    completed_at: string;
  }>;
}
