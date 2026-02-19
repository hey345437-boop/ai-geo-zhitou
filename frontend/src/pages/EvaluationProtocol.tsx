import { useState } from 'react';
import { FileCheck, Play, Download, Plus, CheckCircle2, XCircle, Clock } from 'lucide-react';
import { motion } from 'framer-motion';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { Button } from '@components/ui/Button';

const EvaluationProtocol = () => {
  const [selectedProtocol, setSelectedProtocol] = useState<string | null>(null);

  const protocols = [
    {
      id: '1',
      name: 'Brand Visibility Test',
      description: 'Measure brand mention rate across 100 queries',
      status: 'completed',
      lastRun: '2 hours ago',
      queries: 100,
      engines: 4,
      passRate: 85,
    },
    {
      id: '2',
      name: 'Citation Quality Check',
      description: 'Verify citation accuracy and credibility',
      status: 'running',
      lastRun: 'Running now',
      queries: 50,
      engines: 3,
      passRate: null,
    },
    {
      id: '3',
      name: 'Position Consistency',
      description: 'Track ranking stability over time',
      status: 'scheduled',
      lastRun: 'Scheduled for tomorrow',
      queries: 75,
      engines: 4,
      passRate: null,
    },
  ];

  const testResults = [
    {
      engine: 'GPT-4',
      passed: 42,
      failed: 5,
      pending: 3,
      score: 89,
    },
    {
      engine: 'Claude 3',
      passed: 38,
      failed: 8,
      pending: 4,
      score: 82,
    },
    {
      engine: 'Gemini Pro',
      passed: 35,
      failed: 10,
      pending: 5,
      score: 78,
    },
    {
      engine: 'Perplexity',
      passed: 30,
      failed: 15,
      pending: 5,
      score: 67,
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'running':
        return 'primary';
      case 'scheduled':
        return 'warning';
      default:
        return 'neutral';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5" />;
      case 'running':
        return <Clock className="w-5 h-5 animate-spin" />;
      case 'scheduled':
        return <Clock className="w-5 h-5" />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-8">
      <PageHeader
        title="Evaluation Protocol"
        subtitle="Reproducible testing framework for consistent measurement"
        icon={<FileCheck className="w-6 h-6 text-accent-400" />}
      />

      {/* Action Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Button icon={<Plus className="w-5 h-5" />}>
            Create Protocol
          </Button>
          <Button variant="secondary" icon={<Download className="w-5 h-5" />}>
            Export Results
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-neutral-400">
            {protocols.length} protocols
          </span>
        </div>
      </div>

      {/* Protocol List */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {protocols.map((protocol) => (
          <motion.div
            key={protocol.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          >
            <GlassCard
              className={`p-6 cursor-pointer transition-all ${
                selectedProtocol === protocol.id
                  ? 'ring-2 ring-primary-500'
                  : ''
              }`}
              onClick={() => setSelectedProtocol(protocol.id)}
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`text-${getStatusColor(protocol.status)}-400`}>
                  {getStatusIcon(protocol.status)}
                </div>
                <span className={`px-2 py-1 text-xs rounded-full bg-${getStatusColor(protocol.status)}-500/20 text-${getStatusColor(protocol.status)}-400 capitalize`}>
                  {protocol.status}
                </span>
              </div>

              <h3 className="text-lg font-semibold text-neutral-50 mb-2">
                {protocol.name}
              </h3>
              <p className="text-sm text-neutral-400 mb-4">
                {protocol.description}
              </p>

              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-neutral-500">Queries</span>
                  <span className="text-neutral-300">{protocol.queries}</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-neutral-500">Engines</span>
                  <span className="text-neutral-300">{protocol.engines}</span>
                </div>
                {protocol.passRate !== null && (
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-neutral-500">Pass Rate</span>
                    <span className="text-success-400 font-semibold">
                      {protocol.passRate}%
                    </span>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-neutral-800">
                <p className="text-xs text-neutral-500">
                  Last run: {protocol.lastRun}
                </p>
              </div>

              {protocol.status === 'completed' && (
                <Button
                  variant="secondary"
                  icon={<Play className="w-4 h-4" />}
                  className="w-full mt-4"
                  onClick={(e) => {
                    e.stopPropagation();
                  }}
                >
                  Run Again
                </Button>
              )}
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {/* Test Results */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Latest Test Results
        </h2>
        <div className="space-y-4">
          {testResults.map((result) => (
            <div
              key={result.engine}
              className="p-4 bg-neutral-800/30 rounded-lg"
            >
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-neutral-200 font-medium">{result.engine}</h3>
                <span className="text-2xl font-bold text-neutral-50">
                  {result.score}%
                </span>
              </div>

              <div className="grid grid-cols-3 gap-4 mb-3">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <CheckCircle2 className="w-4 h-4 text-success-400" />
                    <span className="text-success-400 font-semibold">
                      {result.passed}
                    </span>
                  </div>
                  <p className="text-xs text-neutral-500">Passed</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <XCircle className="w-4 h-4 text-error-400" />
                    <span className="text-error-400 font-semibold">
                      {result.failed}
                    </span>
                  </div>
                  <p className="text-xs text-neutral-500">Failed</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <Clock className="w-4 h-4 text-warning-400" />
                    <span className="text-warning-400 font-semibold">
                      {result.pending}
                    </span>
                  </div>
                  <p className="text-xs text-neutral-500">Pending</p>
                </div>
              </div>

              <div className="w-full h-2 bg-neutral-800 rounded-full overflow-hidden">
                <div className="h-full flex">
                  <div
                    className="bg-success-500"
                    style={{
                      width: `${(result.passed / (result.passed + result.failed + result.pending)) * 100}%`,
                    }}
                  />
                  <div
                    className="bg-error-500"
                    style={{
                      width: `${(result.failed / (result.passed + result.failed + result.pending)) * 100}%`,
                    }}
                  />
                  <div
                    className="bg-warning-500"
                    style={{
                      width: `${(result.pending / (result.passed + result.failed + result.pending)) * 100}%`,
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Protocol Details */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Protocol Configuration
        </h2>
        <div className="space-y-4">
          <div className="p-4 bg-neutral-800/30 rounded-lg">
            <h3 className="text-neutral-200 font-medium mb-2">Test Queries</h3>
            <p className="text-sm text-neutral-400 mb-3">
              Standardized question set for reproducible testing
            </p>
            <div className="flex items-center gap-2">
              <Button variant="secondary" size="sm">
                View Queries
              </Button>
              <Button variant="ghost" size="sm">
                Edit
              </Button>
            </div>
          </div>

          <div className="p-4 bg-neutral-800/30 rounded-lg">
            <h3 className="text-neutral-200 font-medium mb-2">Success Criteria</h3>
            <p className="text-sm text-neutral-400 mb-3">
              Define what constitutes a passing test
            </p>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-neutral-400">Minimum mention rate</span>
                <span className="text-neutral-200">80%</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-neutral-400">Required position</span>
                <span className="text-neutral-200">Top 3</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-neutral-400">Citation accuracy</span>
                <span className="text-neutral-200">95%</span>
              </div>
            </div>
          </div>

          <div className="p-4 bg-neutral-800/30 rounded-lg">
            <h3 className="text-neutral-200 font-medium mb-2">Schedule</h3>
            <p className="text-sm text-neutral-400 mb-3">
              Automated testing frequency
            </p>
            <div className="flex items-center gap-2">
              <select className="px-3 py-2 bg-neutral-800 border border-neutral-700 rounded-lg text-neutral-200 text-sm">
                <option>Daily</option>
                <option>Weekly</option>
                <option>Monthly</option>
              </select>
              <Button variant="secondary" size="sm">
                Update Schedule
              </Button>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};

export default EvaluationProtocol;
