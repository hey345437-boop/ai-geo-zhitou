import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface EngineData {
  engine: string;
  score: number;
  mentions: number;
}

interface EngineComparisonChartProps {
  data: EngineData[];
  className?: string;
}

const COLORS = ['#3B82F6', '#06B6D4', '#10B981', '#F59E0B', '#EF4444'];

export const EngineComparisonChart: React.FC<EngineComparisonChartProps> = ({ data, className }) => {
  return (
    <ResponsiveContainer width="100%" height={300} className={className}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
        <XAxis 
          dataKey="engine" 
          stroke="#94A3B8"
          style={{ fontSize: 12 }}
        />
        <YAxis 
          stroke="#94A3B8"
          style={{ fontSize: 12 }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(15, 23, 42, 0.9)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '12px',
            backdropFilter: 'blur(12px)',
          }}
          labelStyle={{ color: '#F8FAFC' }}
        />
        <Bar dataKey="score" radius={[8, 8, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};
