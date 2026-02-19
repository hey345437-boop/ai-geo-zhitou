import { useState } from 'react';
import { Award, TrendingUp, Target, BarChart3 } from 'lucide-react';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { MetricCard } from '@components/ui/MetricCard';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const DomainBenchmark = () => {
  const [selectedIndustry, setSelectedIndustry] = useState('restaurant');

  // Mock benchmark data
  const industries = [
    { id: 'restaurant', name: 'Restaurant & Food Service' },
    { id: 'retail', name: 'Retail & E-commerce' },
    { id: 'healthcare', name: 'Healthcare' },
    { id: 'finance', name: 'Financial Services' },
  ];

  // Mock performance comparison
  const performanceData = [
    { metric: 'Visibility', yourBrand: 85, industryAvg: 65, topPerformer: 95 },
    { metric: 'Mentions', yourBrand: 78, industryAvg: 60, topPerformer: 90 },
    { metric: 'Citations', yourBrand: 72, industryAvg: 55, topPerformer: 88 },
    { metric: 'Consistency', yourBrand: 88, industryAvg: 70, topPerformer: 92 },
    { metric: 'Authority', yourBrand: 75, industryAvg: 58, topPerformer: 85 },
  ];

  // Mock competitor comparison
  const competitors = [
    { name: 'Your Brand', score: 85, visibility: 85, mentions: 1200, citations: 450 },
    { name: 'Competitor A', score: 78, visibility: 78, mentions: 980, citations: 380 },
    { name: 'Competitor B', score: 72, visibility: 72, mentions: 850, citations: 320 },
    { name: 'Competitor C', score: 68, visibility: 68, mentions: 720, citations: 280 },
    { name: 'Industry Avg', score: 65, visibility: 65, mentions: 650, citations: 240 },
  ];

  // Mock best practices
  const bestPractices = [
    {
      category: 'Content Strategy',
      practices: [
        { name: 'Regular content updates', adoption: 85, impact: 'high' },
        { name: 'Multi-format content', adoption: 72, impact: 'high' },
        { name: 'Expert citations', adoption: 68, impact: 'medium' },
      ],
    },
    {
      category: 'Technical Optimization',
      practices: [
        { name: 'Structured data markup', adoption: 78, impact: 'high' },
        { name: 'Mobile optimization', adoption: 92, impact: 'high' },
        { name: 'Page speed optimization', adoption: 85, impact: 'medium' },
      ],
    },
    {
      category: 'Authority Building',
      practices: [
        { name: 'Industry partnerships', adoption: 65, impact: 'high' },
        { name: 'Thought leadership', adoption: 58, impact: 'medium' },
        { name: 'Awards & recognition', adoption: 45, impact: 'medium' },
      ],
    },
  ];

  const benchmarkMetrics = {
    ranking: 1,
    totalCompetitors: 50,
    percentile: 98,
    gapToLeader: 10,
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="Domain & Local Benchmark"
        subtitle="Industry-specific performance standards and best practices"
        icon={<Award className="w-6 h-6 text-accent-400" />}
      />

      {/* Industry Selector */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {industries.map((industry) => (
          <button
            key={industry.id}
            onClick={() => setSelectedIndustry(industry.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
              selectedIndustry === industry.id
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-800/50 text-neutral-400 hover:bg-neutral-800 hover:text-neutral-200'
            }`}
          >
            {industry.name}
          </button>
        ))}
      </div>

      {/* Benchmark Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Industry Ranking"
          value={`#${benchmarkMetrics.ranking}`}
          subtitle={`Top ${benchmarkMetrics.percentile}%`}
          icon={<Award className="w-5 h-5" />}
        />
        <MetricCard
          title="Competitors Tracked"
          value={benchmarkMetrics.totalCompetitors.toString()}
          icon={<Target className="w-5 h-5" />}
        />
        <MetricCard
          title="Gap to Leader"
          value={`${benchmarkMetrics.gapToLeader}%`}
          subtitle="Opportunity to improve"
          icon={<TrendingUp className="w-5 h-5" />}
        />
        <MetricCard
          title="Overall Score"
          value="85"
          trend={5.2}
          icon={<BarChart3 className="w-5 h-5" />}
        />
      </div>

      {/* Performance Radar */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Performance vs Industry
        </h2>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={performanceData}>
            <PolarGrid stroke="#374151" />
            <PolarAngleAxis dataKey="metric" stroke="#9CA3AF" />
            <PolarRadiusAxis stroke="#9CA3AF" />
            <Radar
              name="Your Brand"
              dataKey="yourBrand"
              stroke="#3B82F6"
              fill="#3B82F6"
              fillOpacity={0.3}
            />
            <Radar
              name="Industry Average"
              dataKey="industryAvg"
              stroke="#6B7280"
              fill="#6B7280"
              fillOpacity={0.2}
            />
            <Radar
              name="Top Performer"
              dataKey="topPerformer"
              stroke="#10B981"
              fill="#10B981"
              fillOpacity={0.2}
            />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* Competitor Comparison */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Competitive Landscape
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={competitors}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Bar dataKey="visibility" fill="#3B82F6" name="Visibility %" />
            <Bar dataKey="mentions" fill="#10B981" name="Mentions" />
            <Bar dataKey="citations" fill="#F59E0B" name="Citations" />
          </BarChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* Best Practices */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Industry Best Practices
        </h2>
        <div className="space-y-6">
          {bestPractices.map((category) => (
            <div key={category.category}>
              <h3 className="text-lg font-semibold text-neutral-200 mb-4">
                {category.category}
              </h3>
              <div className="space-y-3">
                {category.practices.map((practice) => (
                  <div
                    key={practice.name}
                    className="p-4 bg-neutral-800/30 rounded-lg"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <span className="text-neutral-300 font-medium">
                          {practice.name}
                        </span>
                        <span
                          className={`px-2 py-1 text-xs rounded-full ${
                            practice.impact === 'high'
                              ? 'bg-error-500/20 text-error-400'
                              : 'bg-warning-500/20 text-warning-400'
                          }`}
                        >
                          {practice.impact} impact
                        </span>
                      </div>
                      <span className="text-neutral-400 text-sm">
                        {practice.adoption}% adoption
                      </span>
                    </div>
                    <div className="w-full h-2 bg-neutral-800 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          practice.adoption >= 80
                            ? 'bg-success-500'
                            : practice.adoption >= 60
                            ? 'bg-primary-500'
                            : 'bg-warning-500'
                        }`}
                        style={{ width: `${practice.adoption}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Insights */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Competitive Insights
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-success-500/10 border border-success-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Award className="w-5 h-5 text-success-400 mt-1" />
              <div>
                <h3 className="text-success-400 font-semibold mb-1">
                  Market Leader Position
                </h3>
                <p className="text-sm text-neutral-400">
                  You rank #1 in the restaurant category with 85% visibility, 20 points above industry average.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-primary-500/10 border border-primary-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Target className="w-5 h-5 text-primary-400 mt-1" />
              <div>
                <h3 className="text-primary-400 font-semibold mb-1">
                  Consistency Advantage
                </h3>
                <p className="text-sm text-neutral-400">
                  Your 88% consistency score is 18 points above average, indicating strong brand presence.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-warning-500/10 border border-warning-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <TrendingUp className="w-5 h-5 text-warning-400 mt-1" />
              <div>
                <h3 className="text-warning-400 font-semibold mb-1">
                  Citation Gap Opportunity
                </h3>
                <p className="text-sm text-neutral-400">
                  Your citation score (72%) has room to reach top performer level (88%). Focus on authority building.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-accent-500/10 border border-accent-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <BarChart3 className="w-5 h-5 text-accent-400 mt-1" />
              <div>
                <h3 className="text-accent-400 font-semibold mb-1">
                  Best Practice Adoption
                </h3>
                <p className="text-sm text-neutral-400">
                  You've adopted 78% of high-impact practices, above the 65% industry average.
                </p>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};

export default DomainBenchmark;
