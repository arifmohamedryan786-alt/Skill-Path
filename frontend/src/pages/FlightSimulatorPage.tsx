import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { useToast } from '../context/ToastContext';
import { ForecastData } from '../types';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, Legend
} from 'recharts';
import { Plane, Sparkles, Clock, Check, RefreshCw, ArrowRight, AlertTriangle } from 'lucide-react';
import { FlightSimulatorIllustration } from '../components/illustrations/LineArtIllustrations';

export const FlightSimulatorPage: React.FC<{ onNavigate: (path: string) => void }> = ({ onNavigate }) => {
  const { showToast } = useToast();
  const [forecast, setForecast] = useState<ForecastData | null>(null);
  const [weeklyHours, setWeeklyHours] = useState(8.0);
  const [selectedCareer, setSelectedCareer] = useState('');
  const [simulateFail, setSimulateFail] = useState(false);
  const [simulatedResult, setSimulatedResult] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);

  useEffect(() => {
    loadForecast();
  }, []);

  const loadForecast = async () => {
    setLoading(true);
    try {
      const data = await api.getForecast();
      setForecast(data);
      setWeeklyHours(data.weekly_hours);
      setSelectedCareer(data.career_goal);
    } catch (err: any) {
      showToast(err.message || 'Failed to load forecast', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    try {
      const res = await api.runScenario({
        name: `${weeklyHours}h/wk on ${selectedCareer}`,
        weekly_hours: weeklyHours,
        simulated_career: selectedCareer.toLowerCase().replace(/[\s\/]+/g, '-'),
        simulate_fail: simulateFail
      });
      setSimulatedResult(res);
      showToast('Simulation updated with new parameters!', 'success');
    } catch (err: any) {
      showToast(err.message || 'Simulation failed', 'error');
    }
  };

  const handleApplyPlan = async () => {
    setApplying(true);
    try {
      const updated = await api.applyScenario({
        weekly_hours: weeklyHours,
        simulated_career: selectedCareer.toLowerCase().replace(/[\s\/]+/g, '-')
      });
      setForecast(updated);
      showToast('Plan applied! Your roadmap calendar and sprint tasks have adapted.', 'success');
      onNavigate('/roadmap');
    } catch (err: any) {
      showToast(err.message || 'Failed to apply plan', 'error');
    } finally {
      setApplying(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-sm text-ink-secondary animate-pulse">Running Flight Simulator calculations...</div>;
  }

  const activeData = simulatedResult || forecast;
  const chartData = [
    { week: 'Week 0', Current: forecast?.current_match_pct || 15, Simulated: activeData?.match_pct_4w ? forecast?.current_match_pct : 15, Accelerated: 15 },
    { week: 'Week 4', Current: forecast?.comparison_scenarios?.[0]?.match_pct_4w || 30, Simulated: activeData?.match_pct_4w || 38, Accelerated: 48 },
    { week: 'Week 8', Current: forecast?.comparison_scenarios?.[0]?.match_pct_8w || 55, Simulated: activeData?.match_pct_8w || 65, Accelerated: 75 },
    { week: 'Week 12', Current: forecast?.comparison_scenarios?.[0]?.match_pct_12w || 75, Simulated: activeData?.match_pct_12w || 88, Accelerated: 95 },
  ];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Plane className="w-5 h-5 text-primary" />
            <h1 className="font-serif text-2xl font-bold text-ink">Career Flight Simulator</h1>
          </div>
          <p className="text-xs text-ink-secondary">
            Predicts the exact date you become job-ready using mathematical velocity modeling. Test what-if schedules and apply to rebuild your roadmap.
          </p>
        </div>

        <button
          onClick={handleApplyPlan}
          disabled={applying}
          className="px-5 py-2.5 bg-primary text-white text-xs font-semibold rounded-md hover:bg-primary-hover shadow-soft transition-colors flex items-center gap-2"
        >
          <Sparkles className="w-4 h-4 text-accent" />
          <span>Apply This Plan</span>
        </button>
      </div>

      {/* Date Projection Banner */}
      <div className="bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-card grid md:grid-cols-12 gap-6 items-center">
        <div className="md:col-span-8 space-y-2">
          <span className="text-xs font-bold text-primary uppercase tracking-wider">
            Job-Ready Date Forecast
          </span>
          <div className="text-3xl sm:text-4xl font-serif font-bold text-ink">
            {activeData?.realistic_date}
          </div>
          <div className="text-xs text-ink-secondary flex items-center gap-2">
            <span>Optimistic Date: <b>{activeData?.optimistic_date}</b></span>
            <span>•</span>
            <span>Total Gap Hours: <b>{activeData?.total_gap_hours || activeData?.total_hours_needed} hrs</b></span>
          </div>
          <p className="text-xs text-ink leading-relaxed pt-2">
            {activeData?.explanation}
          </p>
        </div>

        <div className="md:col-span-4 flex justify-center">
          <FlightSimulatorIllustration className="w-40 h-28" />
        </div>
      </div>

      {/* Interactive Controls & Chart Section */}
      <div className="grid lg:grid-cols-12 gap-6">
        {/* Left What-If Controls */}
        <div className="lg:col-span-5 bg-surface border border-border rounded-lg p-6 shadow-card space-y-6">
          <h3 className="font-serif text-base font-bold text-ink">What-If Schedule Controls</h3>

          {/* Hours Slider */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="font-semibold text-ink">Weekly Study Time</span>
              <span className="font-serif font-bold text-primary text-base">{weeklyHours} hrs/week</span>
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
            <div className="flex justify-between text-[10px] text-ink-muted mt-1">
              <span>4 hrs (Relaxed)</span>
              <span>8-10 hrs (Standard)</span>
              <span>20+ hrs (Intensive)</span>
            </div>
          </div>

          {/* Compare With Different Career */}
          <div>
            <label className="block text-xs font-semibold text-ink mb-1.5">Target Career</label>
            <select
              value={selectedCareer}
              onChange={(e) => setSelectedCareer(e.target.value)}
              className="w-full text-xs p-2.5 border border-border rounded-md bg-bg text-ink focus:outline-none focus:border-primary"
            >
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="Data Analyst">Data Analyst</option>
              <option value="Data Scientist">Data Scientist</option>
              <option value="Full Stack Developer">Full Stack Developer</option>
              <option value="Cloud Engineer">Cloud Engineer</option>
              <option value="DevOps Engineer">DevOps Engineer</option>
              <option value="UI/UX Designer">UI/UX Designer</option>
            </select>
          </div>

          {/* Simulate Failure Toggle */}
          <div className="p-3.5 bg-bg rounded-md border border-border flex items-center justify-between">
            <div className="space-y-0.5">
              <div className="text-xs font-semibold text-ink flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-status-warning" />
                <span>Simulate Difficult Test / Setback</span>
              </div>
              <div className="text-[11px] text-ink-secondary">
                Increases pace factor by +25% to see delayed date
              </div>
            </div>
            <input
              type="checkbox"
              checked={simulateFail}
              onChange={(e) => setSimulateFail(e.target.checked)}
              className="w-4 h-4 accent-primary rounded cursor-pointer"
            />
          </div>

          <button
            onClick={handleSimulate}
            className="w-full py-2 bg-bg border border-border hover:border-primary text-ink text-xs font-semibold rounded-md transition-colors flex items-center justify-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5 text-primary" />
            <span>Recalculate Flight Simulator</span>
          </button>
        </div>

        {/* Right Match Progression Line Chart */}
        <div className="lg:col-span-7 bg-surface border border-border rounded-lg p-6 shadow-card flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="font-serif text-base font-bold text-ink">Readiness Match % Over Time</h3>
                <p className="text-xs text-ink-secondary">Comparing Current Pace vs Simulated What-If Scenarios</p>
              </div>
            </div>

            <div className="w-full h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E3E1DA" />
                  <XAxis dataKey="week" tick={{ fill: '#5E6B69', fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: '#8A9694', fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E3E1DA', borderRadius: '6px', fontSize: '11px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px' }} />
                  <Line type="monotone" dataKey="Current" stroke="#8A9694" strokeWidth={2} dot={{ r: 3 }} />
                  <Line type="monotone" dataKey="Simulated" stroke="#0F6E68" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                  <Line type="monotone" dataKey="Accelerated" stroke="#E8A33D" strokeDasharray="3 3" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Quick Stats Grid */}
          <div className="grid grid-cols-3 gap-3 pt-4 border-t border-border mt-4 text-center">
            <div className="p-2 bg-bg rounded">
              <div className="text-[10px] text-ink-muted">Match @ Week 4</div>
              <div className="text-sm font-bold text-ink">{activeData?.match_pct_4w || 38}%</div>
            </div>
            <div className="p-2 bg-bg rounded">
              <div className="text-[10px] text-ink-muted">Match @ Week 8</div>
              <div className="text-sm font-bold text-ink">{activeData?.match_pct_8w || 65}%</div>
            </div>
            <div className="p-2 bg-bg rounded">
              <div className="text-[10px] text-ink-muted">Match @ Week 12</div>
              <div className="text-sm font-bold text-ink">{activeData?.match_pct_12w || 88}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

