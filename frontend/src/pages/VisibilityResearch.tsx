import { useState } from 'react';
import { Search, Play, Loader2, Activity, PieChart, Lightbulb, Target } from 'lucide-react';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { Button } from '@components/ui/Button';
import { Input } from '@components/ui/Input';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '@api/client';
import type { VisibilityReport } from '@types/index';

const VisibilityResearch = () => {
  const [category, setCategory] = useState('');
  const [report, setReport] = useState<VisibilityReport | null>(null);

  const runResearchMutation = useMutation({
    mutationFn: async (category: string) => {
      const response = await apiClient.post('/research/analyze', {
        category,
        question_count: 100,
        llm_engines: ['gpt-4', 'claude-3', 'gemini-pro']
      });
      return response.data;
    },
    onSuccess: (data) => {
      setReport(data);
    }
  });

  const handleRunResearch = () => {
    if (category.trim()) {
      runResearchMutation.mutate(category);
    }
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="LLM Visibility Research"
        subtitle="Analyze category performance before GEO investment"
        icon={<Search className="w-6 h-6 text-accent-400" />}
      />

      {/* Input Section */}
      <GlassCard className="p-8">
        <div className="max-w-2xl">
          <Input
            label="Product Category"
            placeholder="e.g., 火锅, 咖啡, 健身房"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleRunResearch()}
            icon={<Search className="w-5 h-5" />}
          />
          <div className="mt-4">
            <Button
              onClick={handleRunResearch}
              disabled={!category.trim() || runResearchMutation.isPending}
              loading={runResearchMutation.isPending}
              icon={<Play className="w-5 h-5" />}
              className="w-full sm:w-auto"
            >
              {runResearchMutation.isPending ? 'Analyzing...' : 'Run Analysis'}
            </Button>
          </div>
        </div>
      </GlassCard>

      {/* Results Section */}
      <AnimatePresence>
        {report && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-8"
          >
            {/* Maturity Assessment */}
            <GlassCard className="p-8">
              <div className="flex items-center gap-3 mb-6">
                <Activity className="w-5 h-5 text-accent-400" />
                <h2 className="text-xl font-semibold text-neutral-50">
                  Category Maturity Assessment
                </h2>
              </div>
              <MaturityIndicator level={report.maturity} />
            </GlassCard>

            {/* Share of Model Chart */}
            <GlassCard className="p-8">
              <div className="flex items-center gap-3 mb-6">
                <PieChart className="w-5 h-5 text-accent-400" />
                <h2 className="text-xl font-semibold text-neutral-50">
                  Share of Model
                </h2>
              </div>
              <ShareOfModelChart data={report.brand_shares} />
            </GlassCard>

            {/* Cognitive Gaps */}
            <GlassCard className="p-8">
              <div className="flex items-center gap-3 mb-6">
                <Lightbulb className="w-5 h-5 text-warning-400" />
                <h2 className="text-xl font-semibold text-neutral-50">
                  Cognitive Gaps & Opportunities
                </h2>
              </div>
              <CognitiveGapsTable gaps={report.cognitive_gaps} />
            </GlassCard>

            {/* GEO Strategies */}
            <GlassCard className="p-8">
              <div className="flex items-center gap-3 mb-6">
                <Target className="w-5 h-5 text-success-400" />
                <h2 className="text-xl font-semibold text-neutral-50">
                  Recommended GEO Strategies
                </h2>
              </div>
              <StrategyRecommendations strategies={report.strategies} />
            </GlassCard>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Maturity Indicator Component
const MaturityIndicator: React.FC<{ level: string }> = ({ level }) => {
  const maturityConfig = {
    low: {
      color: 'error',
      label: 'Low Maturity',
      description: 'Category is rarely mentioned in LLM responses. High opportunity for early positioning.',
      percentage: 33
    },
    medium: {
      color: 'warning',
      label: 'Medium Maturity',
      description: 'Category has moderate presence. Competition is building but opportunities remain.',
      percentage: 66
    },
    high: {
      color: 'success',
      label: 'High Maturity',
      description: 'Category is well-established in LLM knowledge. Focus on differentiation.',
      percentage: 100
    }
  };

  const config = maturityConfig[level as keyof typeof maturityConfig] || maturityConfig.medium;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-lg font-semibold text-neutral-200">{config.label}</span>
        <span className={`text-${config.color}-400 font-bold`}>{config.percentage}%</span>
      </div>
      <div className="w-full h-3 bg-neutral-800 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${config.percentage}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-full bg-${config.color}-500 rounded-full`}
        />
      </div>
      <p className="text-sm text-neutral-400">{config.description}</p>
    </div>
  );
};

// Share of Model Chart Component
const ShareOfModelChart: React.FC<{ data: Record<string, number> }> = ({ data }) => {
  const sortedData = Object.entries(data)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10);

  const colors = [
    'bg-primary-500',
    'bg-accent-500',
    'bg-success-500',
    'bg-warning-500',
    'bg-error-500',
    'bg-primary-400',
    'bg-accent-400',
    'bg-success-400',
    'bg-warning-400',
    'bg-error-400',
  ];

  return (
    <div className="space-y-4">
      {sortedData.map(([brand, share], index) => (
        <motion.div
          key={brand}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="space-y-2"
        >
          <div className="flex items-center justify-between text-sm">
            <span className="text-neutral-300 font-medium">{brand}</span>
            <span className="text-neutral-400">{share.toFixed(1)}%</span>
          </div>
          <div className="w-full h-2 bg-neutral-800 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${share}%` }}
              transition={{ duration: 0.8, delay: index * 0.1 }}
              className={`h-full ${colors[index % colors.length]} rounded-full`}
            />
          </div>
        </motion.div>
      ))}
    </div>
  );
};

// Cognitive Gaps Table Component
const CognitiveGapsTable: React.FC<{ gaps: any[] }> = ({ gaps }) => {
  return (
    <div className="space-y-3">
      {gaps.map((gap, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="p-4 bg-neutral-800/30 rounded-lg"
        >
          <div className="flex items-start justify-between mb-2">
            <h3 className="text-neutral-200 font-medium">{gap.topic}</h3>
            <span className="px-3 py-1 bg-warning-500/20 text-warning-400 text-xs rounded-full">
              {(gap.opportunity_score * 100).toFixed(0)}% opportunity
            </span>
          </div>
          {gap.description && (
            <p className="text-sm text-neutral-400">{gap.description}</p>
          )}
          {gap.current_leaders && gap.current_leaders.length > 0 && (
            <div className="mt-2 text-xs text-neutral-500">
              Current leaders: {gap.current_leaders.join(', ')}
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );
};

// Strategy Recommendations Component
const StrategyRecommendations: React.FC<{ strategies: any[] }> = ({ strategies }) => {
  const priorityColors = {
    high: 'error',
    medium: 'warning',
    low: 'success'
  };

  return (
    <div className="space-y-3">
      {strategies.map((strategy, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="p-4 bg-neutral-800/30 rounded-lg"
        >
          <div className="flex items-start gap-3">
            <div className={`w-2 h-2 rounded-full bg-${priorityColors[strategy.priority as keyof typeof priorityColors]}-500 mt-2`} />
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-neutral-200 font-medium">{strategy.title || strategy.description}</h3>
                <span className="text-xs text-neutral-500 uppercase">{strategy.priority}</span>
              </div>
              <p className="text-sm text-neutral-400">{strategy.description}</p>
              {strategy.expected_impact && (
                <div className="mt-2 text-xs text-accent-400">
                  Expected impact: +{(strategy.expected_impact * 100).toFixed(0)}%
                </div>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default VisibilityResearch;
