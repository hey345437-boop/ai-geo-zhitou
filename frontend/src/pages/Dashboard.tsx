import { useState, useEffect } from 'react';
import { TrendingUp, Target, Award, BarChart3 } from 'lucide-react';
import { PageHeader } from '@components/ui/PageHeader';
import { MetricCard } from '@components/ui/MetricCard';
import { GlassCard } from '@components/ui/GlassCard';
import { VisibilityTrendChart } from '@components/charts/VisibilityTrendChart';
import { EngineComparisonChart } from '@components/charts/EngineComparisonChart';

const Dashboard = () => {
  const [timeframe, setTimeframe] = useState('30d');

  const visibilityScore = {
    overall: 78.5,
    mention_rate: 85.0,
    position_score: 72.0,
    consistency: 80.0,
    trend: 5.2,
    citation_weighted: 76.3,
    competitive_ranking: 3,
  };

  const trendData = Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    visibility: 70 + Math.random() * 20,
    mentions: 60 + Math.random() * 30,
    citations: 50 + Math.random() * 25,
  }));

  const engineData = [
    { engine: 'GPT-4', score: 85, mentions: 120 },
    { engine: 'Claude 3', score: 78, mentions: 95 },
    { engine: 'Gemini Pro', score: 72, mentions: 88 },
    { engine: 'Perplexity', score: 68, mentions: 75 },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title="Visibility Dashboard"
        subtitle="Real-time performance metrics across LLM engines"
      />

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Overall Visibility"
          value={`${visibilityScore.overall}%`}
          trend={visibilityScore.trend}
          icon={<TrendingUp className="w-5 h-5" />}
        />
        <MetricCard
          title="Mention Rate"
          value={`${visibilityScore.mention_rate}%`}
          subtitle="Top-3 mentions"
          icon={<Target className="w-5 h-5" />}
        />
        <MetricCard
          title="Citation Score"
          value={`${visibilityScore.citation_weighted}%`}
          subtitle="Weighted by credibility"
          icon={<Award className="w-5 h-5" />}
        />
        <MetricCard
          title="Competitive Rank"
          value={`#${visibilityScore.competitive_ranking}`}
          subtitle="vs. competitors"
          icon={<BarChart3 className="w-5 h-5" />}
        />
      </div>

      {/* Trend Chart */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-neutral-50">
            Visibility Trend
          </h2>
          <div className="flex items-center gap-2">
            {['7d', '30d', '90d'].map((period) => (
              <button
                key={period}
                onClick={() => setTimeframe(period)}
                className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                  timeframe === period
                    ? 'bg-primary-500 text-white'
                    : 'text-neutral-400 hover:text-neutral-200 hover:bg-neutral-800/50'
                }`}
              >
                {period}
              </button>
            ))}
          </div>
        </div>
        <VisibilityTrendChart data={trendData} />
      </GlassCard>

      {/* Engine Comparison */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Engine Performance
        </h2>
        <EngineComparisonChart data={engineData} />
      </GlassCard>

      {/* Recommendations */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-neutral-50">
            Optimization Recommendations
          </h2>
          <button className="text-sm text-primary-400 hover:text-primary-300 transition-colors">
            View All
          </button>
        </div>
        <div className="space-y-3">
          {[
            { title: 'Improve content authority', priority: 'high', impact: 25 },
            { title: 'Add more citations', priority: 'medium', impact: 15 },
            { title: 'Update freshness signals', priority: 'low', impact: 10 },
          ].map((rec, idx) => (
            <div key={idx} className="p-4 bg-neutral-800/30 rounded-lg flex items-center justify-between hover:bg-neutral-800/50 transition-colors">
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${
                  rec.priority === 'high' ? 'bg-error-500' :
                  rec.priority === 'medium' ? 'bg-warning-500' :
                  'bg-success-500'
                }`}></div>
                <span className="text-neutral-300">{rec.title}</span>
              </div>
              <span className="text-sm text-neutral-500">+{rec.impact}% impact</span>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
};

export default Dashboard;
