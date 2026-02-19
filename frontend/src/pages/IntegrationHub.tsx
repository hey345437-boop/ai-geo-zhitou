import { useState } from 'react';
import { Plug, CheckCircle2, XCircle, Settings, ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';
import { Button } from '@components/ui/Button';

const IntegrationHub = () => {
  const [connectedIntegrations, setConnectedIntegrations] = useState<string[]>(['google-analytics', 'shopify']);

  const integrations = [
    {
      id: 'google-analytics',
      name: 'Google Analytics',
      description: 'Track GEO traffic and conversions',
      category: 'Analytics',
      status: 'connected',
      icon: '📊',
    },
    {
      id: 'shopify',
      name: 'Shopify',
      description: 'Sync product data and track sales',
      category: 'E-commerce',
      status: 'connected',
      icon: '🛍️',
    },
    {
      id: 'wordpress',
      name: 'WordPress',
      description: 'Publish optimized content automatically',
      category: 'CMS',
      status: 'available',
      icon: '📝',
    },
    {
      id: 'hubspot',
      name: 'HubSpot',
      description: 'Sync leads and track customer journey',
      category: 'CRM',
      status: 'available',
      icon: '🎯',
    },
    {
      id: 'slack',
      name: 'Slack',
      description: 'Get real-time alerts and notifications',
      category: 'Communication',
      status: 'available',
      icon: '💬',
    },
    {
      id: 'zapier',
      name: 'Zapier',
      description: 'Connect to 5000+ apps',
      category: 'Automation',
      status: 'available',
      icon: '⚡',
    },
  ];

  const categories = ['All', 'Analytics', 'E-commerce', 'CMS', 'CRM', 'Communication', 'Automation'];
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredIntegrations = selectedCategory === 'All'
    ? integrations
    : integrations.filter(i => i.category === selectedCategory);

  return (
    <div className="space-y-8">
      <PageHeader
        title="Integration Hub"
        subtitle="Connect your tools and platforms for seamless workflow"
        icon={<Plug className="w-6 h-6 text-accent-400" />}
      />

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlassCard className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-400">Connected</p>
              <p className="text-3xl font-bold text-neutral-50 mt-1">
                {connectedIntegrations.length}
              </p>
            </div>
            <CheckCircle2 className="w-10 h-10 text-success-400" />
          </div>
        </GlassCard>
        <GlassCard className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-400">Available</p>
              <p className="text-3xl font-bold text-neutral-50 mt-1">
                {integrations.length - connectedIntegrations.length}
              </p>
            </div>
            <Plug className="w-10 h-10 text-primary-400" />
          </div>
        </GlassCard>
        <GlassCard className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-400">Categories</p>
              <p className="text-3xl font-bold text-neutral-50 mt-1">
                {categories.length - 1}
              </p>
            </div>
            <Settings className="w-10 h-10 text-accent-400" />
          </div>
        </GlassCard>
      </div>

      {/* Category Filter */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
              selectedCategory === category
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-800/50 text-neutral-400 hover:bg-neutral-800 hover:text-neutral-200'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Integration Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredIntegrations.map((integration, index) => (
          <motion.div
            key={integration.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <GlassCard className="p-6 h-full flex flex-col">
              <div className="flex items-start justify-between mb-4">
                <div className="text-4xl">{integration.icon}</div>
                {integration.status === 'connected' ? (
                  <span className="px-2 py-1 text-xs rounded-full bg-success-500/20 text-success-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    Connected
                  </span>
                ) : (
                  <span className="px-2 py-1 text-xs rounded-full bg-neutral-700 text-neutral-400">
                    Available
                  </span>
                )}
              </div>

              <h3 className="text-lg font-semibold text-neutral-50 mb-2">
                {integration.name}
              </h3>
              <p className="text-sm text-neutral-400 mb-4 flex-1">
                {integration.description}
              </p>

              <div className="flex items-center justify-between pt-4 border-t border-neutral-800">
                <span className="text-xs text-neutral-500">{integration.category}</span>
                {integration.status === 'connected' ? (
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" icon={<Settings className="w-4 h-4" />}>
                      Configure
                    </Button>
                  </div>
                ) : (
                  <Button variant="secondary" size="sm">
                    Connect
                  </Button>
                )}
              </div>
            </GlassCard>
          </motion.div>
        ))}
      </div>

      {/* API Documentation */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-semibold text-neutral-50 mb-2">
              API & Webhooks
            </h2>
            <p className="text-sm text-neutral-400">
              Build custom integrations with our REST API
            </p>
          </div>
          <Button variant="secondary" icon={<ExternalLink className="w-4 h-4" />}>
            View Docs
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-neutral-800/30 rounded-lg">
            <h3 className="text-neutral-200 font-medium mb-2">REST API</h3>
            <p className="text-sm text-neutral-400 mb-3">
              完整的程序化访问所有智投功能
            </p>
            <code className="text-xs text-accent-400 bg-neutral-900 px-2 py-1 rounded">
              https://api.geo-optimizer.com/v1
            </code>
          </div>
          <div className="p-4 bg-neutral-800/30 rounded-lg">
            <h3 className="text-neutral-200 font-medium mb-2">Webhooks</h3>
            <p className="text-sm text-neutral-400 mb-3">
              Real-time notifications for visibility changes and alerts
            </p>
            <Button variant="ghost" size="sm">
              Configure Webhooks
            </Button>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};

export default IntegrationHub;
