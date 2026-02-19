import { useState } from 'react';
import { Globe2, MapPin, TrendingUp, Users } from 'lucide-react';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { MetricCard } from '@components/ui/MetricCard';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell } from 'recharts';

const GeoAnalysis = () => {
  const [selectedRegion, setSelectedRegion] = useState('all');

  // Mock regional data
  const regionalPerformance = [
    { region: 'Beijing', visibility: 85, mentions: 1200, conversions: 450 },
    { region: 'Shanghai', visibility: 78, mentions: 980, conversions: 380 },
    { region: 'Guangzhou', visibility: 72, mentions: 850, conversions: 320 },
    { region: 'Shenzhen', visibility: 68, mentions: 720, conversions: 280 },
    { region: 'Chengdu', visibility: 65, mentions: 650, conversions: 240 },
  ];

  // Mock language distribution
  const languageData = [
    { language: 'Chinese', value: 65, color: '#3B82F6' },
    { language: 'English', value: 25, color: '#10B981' },
    { language: 'Japanese', value: 6, color: '#F59E0B' },
    { language: 'Korean', value: 4, color: '#EF4444' },
  ];

  // Mock localization opportunities
  const opportunities = [
    {
      region: 'Chengdu',
      opportunity: 'Local dialect content',
      impact: 'high',
      score: 85,
      description: 'Create content in Sichuan dialect to improve local engagement',
    },
    {
      region: 'Shanghai',
      opportunity: 'International audience',
      impact: 'medium',
      score: 72,
      description: 'Add English content for expat community',
    },
    {
      region: 'Guangzhou',
      opportunity: 'Cantonese optimization',
      impact: 'high',
      score: 80,
      description: 'Optimize for Cantonese queries and local preferences',
    },
  ];

  const totalMetrics = {
    regions: 5,
    languages: 4,
    totalVisibility: 73.6,
    topRegion: 'Beijing',
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="Geographic Analysis"
        subtitle="Regional performance insights and localization opportunities"
        icon={<Globe2 className="w-6 h-6 text-accent-400" />}
      />

      {/* Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Active Regions"
          value={totalMetrics.regions.toString()}
          icon={<MapPin className="w-5 h-5" />}
        />
        <MetricCard
          title="Languages"
          value={totalMetrics.languages.toString()}
          icon={<Globe2 className="w-5 h-5" />}
        />
        <MetricCard
          title="Avg Visibility"
          value={`${totalMetrics.totalVisibility}%`}
          trend={5.2}
          icon={<TrendingUp className="w-5 h-5" />}
        />
        <MetricCard
          title="Top Region"
          value={totalMetrics.topRegion}
          subtitle="85% visibility"
          icon={<Users className="w-5 h-5" />}
        />
      </div>

      {/* Regional Performance */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Regional Performance
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={regionalPerformance}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="region" stroke="#9CA3AF" />
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
            <Bar dataKey="conversions" fill="#F59E0B" name="Conversions" />
          </BarChart>
        </ResponsiveContainer>
      </GlassCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Language Distribution */}
        <GlassCard className="p-8">
          <h2 className="text-xl font-semibold text-neutral-50 mb-6">
            Language Distribution
          </h2>
          <div className="flex items-center justify-center mb-6">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={languageData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {languageData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-2">
            {languageData.map((lang) => (
              <div key={lang.language} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: lang.color }}
                  />
                  <span className="text-neutral-300">{lang.language}</span>
                </div>
                <span className="text-neutral-400">{lang.value}%</span>
              </div>
            ))}
          </div>
        </GlassCard>

        {/* Regional Details */}
        <GlassCard className="p-8">
          <h2 className="text-xl font-semibold text-neutral-50 mb-6">
            Regional Details
          </h2>
          <div className="space-y-4">
            {regionalPerformance.map((region) => (
              <div
                key={region.region}
                className="p-4 bg-neutral-800/30 rounded-lg hover:bg-neutral-800/50 transition-colors cursor-pointer"
                onClick={() => setSelectedRegion(region.region)}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-neutral-200 font-medium">{region.region}</h3>
                  <span className="text-primary-400 font-semibold">
                    {region.visibility}%
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-neutral-500">Mentions</p>
                    <p className="text-neutral-300">{region.mentions.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-neutral-500">Conversions</p>
                    <p className="text-neutral-300">{region.conversions.toLocaleString()}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>

      {/* Localization Opportunities */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Localization Opportunities
        </h2>
        <div className="space-y-4">
          {opportunities.map((opp, index) => (
            <div
              key={index}
              className="p-4 bg-neutral-800/30 rounded-lg"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <MapPin className="w-4 h-4 text-accent-400" />
                    <h3 className="text-neutral-200 font-medium">{opp.region}</h3>
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        opp.impact === 'high'
                          ? 'bg-error-500/20 text-error-400'
                          : 'bg-warning-500/20 text-warning-400'
                      }`}
                    >
                      {opp.impact} impact
                    </span>
                  </div>
                  <h4 className="text-neutral-300 font-medium mb-1">
                    {opp.opportunity}
                  </h4>
                  <p className="text-sm text-neutral-400">{opp.description}</p>
                </div>
                <div className="text-right ml-4">
                  <p className="text-2xl font-bold text-primary-400">{opp.score}</p>
                  <p className="text-xs text-neutral-500">opportunity score</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Regional Insights */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Key Regional Insights
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-success-500/10 border border-success-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <TrendingUp className="w-5 h-5 text-success-400 mt-1" />
              <div>
                <h3 className="text-success-400 font-semibold mb-1">
                  Beijing Leading Performance
                </h3>
                <p className="text-sm text-neutral-400">
                  Beijing shows 85% visibility, 15% above national average. Strong brand recognition in tier-1 cities.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-primary-500/10 border border-primary-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Globe2 className="w-5 h-5 text-primary-400 mt-1" />
              <div>
                <h3 className="text-primary-400 font-semibold mb-1">
                  Multi-language Opportunity
                </h3>
                <p className="text-sm text-neutral-400">
                  25% of queries are in English. Consider expanding English content for international audience.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-warning-500/10 border border-warning-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <MapPin className="w-5 h-5 text-warning-400 mt-1" />
              <div>
                <h3 className="text-warning-400 font-semibold mb-1">
                  Tier-2 City Growth
                </h3>
                <p className="text-sm text-neutral-400">
                  Chengdu and other tier-2 cities show 20% growth potential with localized content strategies.
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-accent-500/10 border border-accent-500/20 rounded-lg">
            <div className="flex items-start gap-3">
              <Users className="w-5 h-5 text-accent-400 mt-1" />
              <div>
                <h3 className="text-accent-400 font-semibold mb-1">
                  Regional Preferences
                </h3>
                <p className="text-sm text-neutral-400">
                  Each region shows distinct query patterns. Tailor content to local preferences for better engagement.
                </p>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};

export default GeoAnalysis;
