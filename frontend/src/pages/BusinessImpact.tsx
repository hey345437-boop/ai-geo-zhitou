import { useState } from 'react';
import { TrendingUp, DollarSign, Users, Target, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { MetricCard } from '@components/ui/MetricCard';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const BusinessImpact = () => {
  const [timeframe, setTimeframe] = useState('30d');

  const roiMetrics = {
    totalInvestment: 50000,
    totalRevenue: 125000,
    roi: 150,
    conversions: 1250,
    conversionRate: 3.2,
    avgOrderValue: 100,
  };

  const revenueTrend = Array.from({ length: 12 }, (_, i) => ({
    month: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i],
    revenue: 8000 + Math.random() * 4000,
    investment: 3000 + Math.random() * 2000,
  }));

  const conversionFunnel = [
    { stage: 'LLM Impressions', count: 50000, rate: 100 },
    { stage: 'Click-throughs', count: 5000, rate: 10 },
    { stage: 'Website Visits', count: 4000, rate: 8 },
    { stage: 'Conversions', count: 1250, rate: 2.5 },
  ];

  const attributionData = [
    { source: 'GPT-4', conversions: 450, revenue: 45000 },
    { source: 'Claude 3', conversions: 380, revenue: 38000 },
    { source: 'Gemini Pro', conversions: 280, revenue: 28000 },
    { source: 'Perplexity', conversions: 140, revenue: 14000 },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title="Business Impact Analysis"
        subtitle="Measure ROI and business outcomes from GEO optimization"
        icon={<TrendingUp className="w-6 h-6 text-success-400" />}
      />

      {/* ROI Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total ROI"
          value={`${roiMetrics.roi}%`}
          trend={25}
          icon={<DollarSign className="w-5 h-5" />}
        />
        <MetricCard
          title="Total Revenue"
          value={`$${(roiMetrics.totalRevenue / 1000).toFixed(0)}K`}
          subtitle="From GEO traffic"
          icon={<TrendingUp className="w-5 h-5" />}
        />
        <MetricCard
          title="Conversions"
          value={roiMetrics.conversions.toLocaleString()}
          trend={12}
          icon={<Users className="w-5 h-5" />}
        />
        <MetricCard
          title="Conversion Rate"
          value={`${roiMetrics.conversionRate}%`}
          trend={8}
          icon={<Target className="w-5 h-5" />}
        />
      </div>

      {/* Revenue Trend */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-neutral-50">
            Revenue vs Investment
          </h2>
          <div className="flex items-center gap-2">
            {['30d', '90d', '1y'].map((period) => (
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
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={revenueTrend}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="month" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#10B981"
              strokeWidth={2}
              name="Revenue"
            />
            <Line
              type="monotone"
              dataKey="investment"
              stroke="#3B82F6"
              strokeWidth={2}
              name="Investment"
            />
          </LineChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* Conversion Funnel */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Conversion Funnel
        </h2>
        <div className="space-y-4">
          {conversionFunnel.map((stage, index) => (
            <div key={stage.stage} className="relative">
              <div className="flex items-center justify-between mb-2">
                <span className="text-neutral-300 font-medium">{stage.stage}</span>
                <div className="flex items-center gap-4">
                  <span className="text-neutral-400 text-sm">
                    {stage.count.toLocaleString()} ({stage.rate}%)
                  </span>
                  {index > 0 && (
                    <span className="text-error-400 text-sm flex items-center gap-1">
                      <ArrowDownRight className="w-4 h-4" />
                      {((1 - stage.rate / conversionFunnel[index - 1].rate) * 100).toFixed(0)}% drop
                    </span>
                  )}
                </div>
              </div>
              <div className="w-full h-12 bg-neutral-800 rounded-lg overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary-500 to-accent-500 flex items-center justify-center text-white font-semibold transition-all duration-500"
                  style={{ width: `${stage.rate}%` }}
                >
                  {stage.rate}%
                </div>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Attribution by Engine */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Revenue Attribution by Engine
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={attributionData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="source" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '8px',
              }}
            />
            <Legend />
            <Bar dataKey="conversions" fill="#3B82F6" name="Conversions" />
            <Bar dataKey="revenue" fill="#10B981" name="Revenue ($)" />
          </BarChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* Key Insights */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Key Insights
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-success-500/10 border border-success-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <ArrowUpRight className="w-5 h-5 text-success-400 mt-1" />
              <div>
                <h3 className="text-success-400 font-semibold mb-1">
                  Strong ROI Performance
                </h3>
                <p className="text-sm text-neutral-400">
                  Your GEO investment is generating 150% ROI, significantly above industry average of 80%.
                </p>
              </div>
            </div>
          </div>
          <div className="p-4 bg-primary-500/10 border border-primary-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Target className="w-5 h-5 text-primary-400 mt-1" />
              <div>
                <h3 className="text-primary-400 font-semibold mb-1">
                  GPT-4 Leading Attribution
                </h3>
                <p className="text-sm text-neutral-400">
                  GPT-4 drives 36% of conversions. Consider increasing optimization efforts for this engine.
                </p>
              </div>
            </div>
          </div>
          <div className="p-4 bg-warning-500/10 border border-warning-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <ArrowDownRight className="w-5 h-5 text-warning-400 mt-1" />
              <div>
                <h3 className="text-warning-400 font-semibold mb-1">
                  Funnel Drop-off at Visits
                </h3>
                <p className="text-sm text-neutral-400">
                  20% drop from click-throughs to visits. Improve landing page relevance to LLM queries.
                </p>
              </div>
            </div>
          </div>
          <div className="p-4 bg-accent-500/10 border border-accent-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <DollarSign className="w-5 h-5 text-accent-400 mt-1" />
              <div>
                <h3 className="text-accent-400 font-semibold mb-1">
                  High Average Order Value
                </h3>
                <p className="text-sm text-neutral-400">
                  $100 AOV from GEO traffic is 25% higher than other channels, indicating quality traffic.
                </p>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};

export default BusinessImpact;
