import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { api } from '../api/client';
import { ArrowRight, ArrowLeft, Check, Sparkles, Compass, CheckCircle } from 'lucide-react';
import { CompassIllustration } from '../components/illustrations/LineArtIllustrations';

export const OnboardingPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { user } = useAuth();
  const { showToast } = useToast();

  // Step 0: Goal Clarity Gate
  // Step 1: Education
  // Step 2: Interests
  // Step 3: Strengths
  // Step 4: Existing Skills (never blocks with "None yet")
  // Step 5: Weekly Study Hours
  const [step, setStep] = useState(0);

  const [goalStatus, setGoalStatus] = useState<'known' | 'rough' | 'unknown'>('unknown');
  const [selectedGoal, setSelectedGoal] = useState('AI/ML Engineer');
  const [fullName, setFullName] = useState(user?.full_name || 'Arif Mohamed');
  const [education, setEducation] = useState('B.Tech');
  const [branch, setBranch] = useState('Artificial Intelligence and Data Science');
  const [year, setYear] = useState(3);
  const [institution, setInstitution] = useState('National Institute of Technology');

  const [selectedInterests, setSelectedInterests] = useState<string[]>(['building', 'teaching machines']);
  const [selectedStrengths, setSelectedStrengths] = useState<string[]>(['math', 'logical thinking']);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [weeklyHours, setWeeklyHours] = useState(8.0);
  const [submitting, setSubmitting] = useState(false);

  const interestOptions = [
    { id: 'building', label: 'Building apps, tools or systems', desc: 'Making functional software from scratch' },
    { id: 'analyzing', label: 'Analyzing data & numbers', desc: 'Finding trends, patterns, and insights' },
    { id: 'designing', label: 'Designing user interfaces', desc: 'Choosing colors, typography, and intuitive flows' },
    { id: 'teaching machines', label: 'Teaching smart machines (AI)', desc: 'Training models to recognize and predict' },
    { id: 'protecting', label: 'Protecting digital systems', desc: 'Finding vulnerabilities and cybersecurity defense' },
    { id: 'organizing', label: 'Automating & organizing pipelines', desc: 'Cloud servers, CI/CD, and fast infrastructure' }
  ];

  const strengthOptions = [
    { id: 'math', label: 'Mathematics & Statistics' },
    { id: 'logical thinking', label: 'Step-by-step Logical Thinking' },
    { id: 'visual creativity', label: 'Visual Creativity & Aesthetics' },
    { id: 'problem solving', label: 'Breaking Down Hard Problems' },
    { id: 'communication', label: 'Explaining Ideas to People' },
    { id: 'attention to detail', label: 'Spotting Minor Errors & Glitches' }
  ];

  const commonSkills = [
    'Python', 'SQL', 'JavaScript', 'HTML/CSS', 'C++', 'Java', 'Git/GitHub', 'Excel/Sheets', 'None yet'
  ];

  const toggleInterest = (id: string) => {
    setSelectedInterests((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleStrength = (id: string) => {
    setSelectedStrengths((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleSkill = (sk: string) => {
    if (sk === 'None yet') {
      setSelectedSkills(['None yet']);
      return;
    }
    const filtered = selectedSkills.filter((x) => x !== 'None yet');
    setSelectedSkills(
      filtered.includes(sk) ? filtered.filter((x) => x !== sk) : [...filtered, sk]
    );
  };

  const handleFinish = async () => {
    setSubmitting(true);
    try {
      await api.updateProfile({
        full_name: fullName,
        education,
        branch,
        year: Number(year),
        institution,
        interests: selectedInterests,
        strengths: selectedStrengths,
        career_goal: goalStatus === 'known' ? selectedGoal : '',
        goal_status: goalStatus,
        weekly_hours: Number(weeklyHours),
      });

      showToast('Profile saved! Loading your personalized path.', 'success');

      if (goalStatus === 'unknown') {
        onNavigate('/discovery');
      } else {
        onNavigate('/dashboard');
      }
    } catch (err: any) {
      showToast(err.message || 'Failed to save profile', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-6">
      {/* Step Indicator Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between text-xs font-semibold text-ink-secondary mb-2">
          <span>Step {step + 1} of 6</span>
          <span>{Math.round(((step + 1) / 6) * 100)}% Completed</span>
        </div>
        <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-300 rounded-full"
            style={{ width: `${((step + 1) / 6) * 100}%` }}
          />
        </div>
      </div>

      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card">
        {/* STEP 0: The Core Goal Question */}
        {step === 0 && (
          <div>
            <div className="w-12 h-12 rounded-full bg-primary-tint flex items-center justify-center text-primary mb-4">
              <Compass className="w-6 h-6" />
            </div>
            <h2 className="font-serif text-2xl font-bold text-ink mb-2">
              Do you already know the career you want?
            </h2>
            <p className="text-sm text-ink-secondary mb-6 leading-relaxed">
              We never assume you already know your path. Your answer decides how we guide you today.
            </p>

            <div className="space-y-3 mb-8">
              <button
                type="button"
                onClick={() => setGoalStatus('known')}
                className={`w-full p-4 rounded-md border text-left transition-all flex items-start gap-3 ${
                  goalStatus === 'known'
                    ? 'border-primary bg-primary-tint/30 ring-1 ring-primary'
                    : 'border-border hover:bg-bg'
                }`}
              >
                <div className={`w-5 h-5 rounded-full border mt-0.5 flex items-center justify-center shrink-0 ${goalStatus === 'known' ? 'border-primary bg-primary text-white' : 'border-border'}`}>
                  {goalStatus === 'known' && <Check className="w-3 h-3 stroke-[3]" />}
                </div>
                <div>
                  <div className="font-semibold text-sm text-ink">Yes, I know my goal</div>
                  <div className="text-xs text-ink-secondary mt-0.5">
                    e.g. Full Stack Developer, Data Analyst, AI/ML Engineer. We will skip discovery and take you straight to skill gap analysis.
                  </div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setGoalStatus('rough')}
                className={`w-full p-4 rounded-md border text-left transition-all flex items-start gap-3 ${
                  goalStatus === 'rough'
                    ? 'border-primary bg-primary-tint/30 ring-1 ring-primary'
                    : 'border-border hover:bg-bg'
                }`}
              >
                <div className={`w-5 h-5 rounded-full border mt-0.5 flex items-center justify-center shrink-0 ${goalStatus === 'rough' ? 'border-primary bg-primary text-white' : 'border-border'}`}>
                  {goalStatus === 'rough' && <Check className="w-3 h-3 stroke-[3]" />}
                </div>
                <div>
                  <div className="font-semibold text-sm text-ink">I have a rough idea</div>
                  <div className="text-xs text-ink-secondary mt-0.5">
                    You know you like tech or data, but want to compare 2 or 3 careers side by side before committing.
                  </div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => setGoalStatus('unknown')}
                className={`w-full p-4 rounded-md border text-left transition-all flex items-start gap-3 ${
                  goalStatus === 'unknown'
                    ? 'border-primary bg-primary-tint/30 ring-1 ring-primary'
                    : 'border-border hover:bg-bg'
                }`}
              >
                <div className={`w-5 h-5 rounded-full border mt-0.5 flex items-center justify-center shrink-0 ${goalStatus === 'unknown' ? 'border-primary bg-primary text-white' : 'border-border'}`}>
                  {goalStatus === 'unknown' && <Check className="w-3 h-3 stroke-[3]" />}
                </div>
                <div>
                  <div className="font-semibold text-sm text-ink">I have no idea yet</div>
                  <div className="text-xs text-ink-secondary mt-0.5">
                    Perfect! We will ask 15 friendly discovery questions to match careers with your interests and strengths.
                  </div>
                </div>
              </button>
            </div>

            {goalStatus === 'known' && (
              <div className="mb-6 p-4 rounded-md bg-bg border border-border">
                <label className="block text-xs font-semibold text-ink mb-1.5">Select your primary career goal</label>
                <select
                  value={selectedGoal}
                  onChange={(e) => setSelectedGoal(e.target.value)}
                  className="w-full text-xs p-2.5 border border-border rounded-md bg-surface text-ink focus:outline-none focus:border-primary"
                >
                  <option value="AI/ML Engineer">AI/ML Engineer</option>
                  <option value="Data Analyst">Data Analyst</option>
                  <option value="Data Scientist">Data Scientist</option>
                  <option value="Full Stack Developer">Full Stack Developer</option>
                  <option value="Frontend Developer">Frontend Developer</option>
                  <option value="Data Engineer">Data Engineer</option>
                  <option value="Cloud Engineer">Cloud Engineer</option>
                  <option value="DevOps Engineer">DevOps Engineer</option>
                  <option value="Cybersecurity Analyst">Cybersecurity Analyst</option>
                  <option value="UI/UX Designer">UI/UX Designer</option>
                  <option value="Product Analyst">Product Analyst</option>
                </select>
              </div>
            )}
          </div>
        )}

        {/* STEP 1: About You */}
        {step === 1 && (
          <div>
            <h2 className="font-serif text-2xl font-bold text-ink mb-2">Tell us about your studies</h2>
            <p className="text-sm text-ink-secondary mb-6">
              This helps us calibrate milestone dates, internship timing, and college-specific placement guidance.
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-ink-secondary mb-1">Full Name</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full text-xs p-2.5 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-ink-secondary mb-1">Degree</label>
                  <input
                    type="text"
                    value={education}
                    onChange={(e) => setEducation(e.target.value)}
                    placeholder="e.g. B.Tech / B.Sc / B.Com"
                    className="w-full text-xs p-2.5 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-ink-secondary mb-1">Year of Study</label>
                  <select
                    value={year}
                    onChange={(e) => setYear(Number(e.target.value))}
                    className="w-full text-xs p-2.5 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                  >
                    <option value={1}>1st Year (Exploring)</option>
                    <option value={2}>2nd Year (Foundations)</option>
                    <option value={3}>3rd Year (Internship Ready)</option>
                    <option value={4}>4th Year (Job Applications)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-ink-secondary mb-1">Major / Branch</label>
                <input
                  type="text"
                  value={branch}
                  onChange={(e) => setBranch(e.target.value)}
                  placeholder="e.g. Artificial Intelligence and Data Science"
                  className="w-full text-xs p-2.5 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-ink-secondary mb-1">Institution / College Name</label>
                <input
                  type="text"
                  value={institution}
                  onChange={(e) => setInstitution(e.target.value)}
                  placeholder="e.g. National Institute of Technology"
                  className="w-full text-xs p-2.5 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
                />
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: What You Enjoy */}
        {step === 2 && (
          <div>
            <h2 className="font-serif text-2xl font-bold text-ink mb-2">What kind of work excites you?</h2>
            <p className="text-sm text-ink-secondary mb-6">
              Pick 2 or 3 activities that feel natural and enjoyable.
            </p>

            <div className="grid sm:grid-cols-2 gap-3">
              {interestOptions.map((opt) => {
                const selected = selectedInterests.includes(opt.id);
                return (
                  <button
                    key={opt.id}
                    type="button"
                    onClick={() => toggleInterest(opt.id)}
                    className={`p-3.5 rounded-md border text-left transition-all flex flex-col justify-between ${
                      selected ? 'border-primary bg-primary-tint/40 ring-1 ring-primary' : 'border-border hover:bg-bg'
                    }`}
                  >
                    <div className="font-semibold text-xs text-ink">{opt.label}</div>
                    <div className="text-[11px] text-ink-secondary mt-1">{opt.desc}</div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* STEP 3: Strengths */}
        {step === 3 && (
          <div>
            <h2 className="font-serif text-2xl font-bold text-ink mb-2">What are you naturally good at?</h2>
            <p className="text-sm text-ink-secondary mb-6">
              Select the abilities that friends, teachers, or projects have recognized in you.
            </p>

            <div className="grid sm:grid-cols-2 gap-2.5">
              {strengthOptions.map((str) => {
                const selected = selectedStrengths.includes(str.id);
                return (
                  <button
                    key={str.id}
                    type="button"
                    onClick={() => toggleStrength(str.id)}
                    className={`p-3 rounded-md border text-left text-xs font-medium transition-all flex items-center justify-between ${
                      selected ? 'border-primary bg-primary-tint/50 text-primary font-semibold' : 'border-border text-ink hover:bg-bg'
                    }`}
                  >
                    <span>{str.label}</span>
                    {selected && <Check className="w-4 h-4 text-primary" />}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* STEP 4: Current Skills */}
        {step === 4 && (
          <div>
            <h2 className="font-serif text-2xl font-bold text-ink mb-2">Have you written any code or tools before?</h2>
            <p className="text-sm text-ink-secondary mb-6">
              Select anything you've touched even a little bit. If you have zero experience, click <b>"None yet"</b>—you are in the right place!
            </p>

            <div className="flex flex-wrap gap-2.5 mb-6">
              {commonSkills.map((sk) => {
                const selected = selectedSkills.includes(sk);
                return (
                  <button
                    key={sk}
                    type="button"
                    onClick={() => toggleSkill(sk)}
                    className={`px-3.5 py-2 rounded-full text-xs font-medium border transition-colors ${
                      selected
                        ? 'bg-primary text-white border-primary shadow-soft'
                        : 'bg-bg text-ink-secondary border-border hover:border-primary/40'
                    }`}
                  >
                    {sk}
                  </button>
                );
              })}
            </div>

            <div className="p-3.5 rounded-md bg-primary-tint/30 border border-primary/20 text-xs text-primary leading-relaxed">
              💡 <b>SkillPath Promise:</b> We never block or penalize learners with no skills or projects. Every expert was once at zero.
            </div>
          </div>
        )}

        {/* STEP 5: Study Hours */}
        {step === 5 && (
          <div>
            <h2 className="font-serif text-2xl font-bold text-ink mb-2">How much time can you study per week?</h2>
            <p className="text-sm text-ink-secondary mb-6">
              Be realistic with your college and life schedule. We use this to schedule your weekly sprint tasks.
            </p>

            <div className="p-6 rounded-md bg-bg border border-border mb-6 text-center">
              <div className="text-4xl font-serif font-bold text-primary mb-1">
                {weeklyHours} <span className="text-lg font-sans font-normal text-ink-secondary">hours / week</span>
              </div>
              <div className="text-xs text-ink-secondary mb-6">
                ~{Math.round((weeklyHours / 7) * 60)} minutes per day
              </div>

              <input
                type="range"
                min="4"
                max="25"
                step="1"
                value={weeklyHours}
                onChange={(e) => setWeeklyHours(Number(e.target.value))}
                className="w-full accent-primary h-2 bg-border rounded-lg cursor-pointer"
              />

              <div className="flex justify-between text-[11px] text-ink-muted mt-2">
                <span>4 hrs (Relaxed)</span>
                <span>8-10 hrs (Standard)</span>
                <span>20+ hrs (Bootcamp pace)</span>
              </div>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="mt-8 pt-6 border-t border-border flex items-center justify-between">
          {step > 0 ? (
            <button
              type="button"
              onClick={() => setStep(step - 1)}
              className="flex items-center gap-1.5 px-4 py-2 border border-border rounded-md text-xs font-medium text-ink-secondary hover:text-ink hover:bg-bg transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back</span>
            </button>
          ) : (
            <div />
          )}

          {step < 5 ? (
            <button
              type="button"
              onClick={() => setStep(step + 1)}
              className="flex items-center gap-1.5 px-5 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors"
            >
              <span>Next Step</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="button"
              disabled={submitting}
              onClick={handleFinish}
              className="flex items-center gap-1.5 px-6 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4 text-accent" />
              <span>{goalStatus === 'unknown' ? 'Begin Career Discovery' : 'Generate My Roadmap'}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

