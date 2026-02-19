import { useState, useEffect } from 'react';
import { Network } from 'lucide-react';
import { motion } from 'framer-motion';
import { PageHeader } from '@components/ui/PageHeader';
import { GlassCard } from '@components/ui/GlassCard';

const EntityGraph = () => {
  const [selectedEntity, setSelectedEntity] = useState<string | null>(null);
  const [graphData, setGraphData] = useState<any>(null);

  // Mock graph data
  useEffect(() => {
    const mockData = {
      nodes: [
        { id: '1', label: '海底捞', type: 'brand', connections: 15 },
        { id: '2', label: '火锅', type: 'category', connections: 25 },
        { id: '3', label: '川菜', type: 'cuisine', connections: 12 },
        { id: '4', label: '呷哺呷哺', type: 'brand', connections: 10 },
        { id: '5', label: '小龙坎', type: 'brand', connections: 8 },
        { id: '6', label: '成都', type: 'location', connections: 18 },
        { id: '7', label: '重庆', type: 'location', connections: 16 },
      ],
      edges: [
        { source: '1', target: '2', weight: 0.9 },
        { source: '1', target: '3', weight: 0.7 },
        { source: '1', target: '6', weight: 0.8 },
        { source: '4', target: '2', weight: 0.85 },
        { source: '5', target: '2', weight: 0.75 },
        { source: '5', target: '7', weight: 0.9 },
      ]
    };
    setGraphData(mockData);
  }, []);

  const entityTypes = [
    { type: 'brand', label: 'Brands', count: 3, color: 'primary' },
    { type: 'category', label: 'Categories', count: 1, color: 'accent' },
    { type: 'cuisine', label: 'Cuisines', count: 1, color: 'success' },
    { type: 'location', label: 'Locations', count: 2, color: 'warning' },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title="Entity Relationship Graph"
        subtitle="Explore connections between brands, content, and entities"
        icon={<Network className="w-6 h-6 text-accent-400" />}
      />

      {/* Entity Type Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {entityTypes.map((entity) => (
          <GlassCard key={entity.type} className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-neutral-400">{entity.label}</p>
                <p className="text-3xl font-bold text-neutral-50 mt-1">
                  {entity.count}
                </p>
              </div>
              <div className={`w-12 h-12 rounded-full bg-${entity.color}-500/20 flex items-center justify-center`}>
                <Network className={`w-6 h-6 text-${entity.color}-400`} />
              </div>
            </div>
          </GlassCard>
        ))}
      </div>

      {/* Graph Visualization */}
      <GlassCard className="p-8">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-neutral-50">
            Entity Network
          </h2>
          <div className="flex items-center gap-2">
            <button className="px-3 py-1.5 text-sm bg-neutral-800/50 text-neutral-300 rounded-lg hover:bg-neutral-800 transition-colors">
              Reset View
            </button>
            <button className="px-3 py-1.5 text-sm bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors">
              Export Graph
            </button>
          </div>
        </div>

        {/* Graph Container */}
        <div className="relative h-[500px] bg-neutral-900/50 rounded-lg border border-neutral-800 overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <Network className="w-16 h-16 text-neutral-700 mx-auto mb-4" />
              <p className="text-neutral-500">
                Interactive graph visualization
              </p>
              <p className="text-sm text-neutral-600 mt-2">
                Connect Neo4j to see real entity relationships
              </p>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* Entity List */}
      <GlassCard className="p-8">
        <h2 className="text-xl font-semibold text-neutral-50 mb-6">
          Entity Details
        </h2>
        <div className="space-y-3">
          {graphData?.nodes.map((node: any) => (
            <motion.div
              key={node.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="p-4 bg-neutral-800/30 rounded-lg hover:bg-neutral-800/50 transition-colors cursor-pointer"
              onClick={() => setSelectedEntity(node.id)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${
                    node.type === 'brand' ? 'bg-primary-500' :
                    node.type === 'category' ? 'bg-accent-500' :
                    node.type === 'cuisine' ? 'bg-success-500' :
                    'bg-warning-500'
                  }`}></div>
                  <div>
                    <p className="text-neutral-200 font-medium">{node.label}</p>
                    <p className="text-sm text-neutral-500 capitalize">{node.type}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-neutral-400 text-sm">{node.connections} connections</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
};

export default EntityGraph;
