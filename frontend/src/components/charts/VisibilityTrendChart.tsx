import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface TrendData {
  date: string;
  visibility: number;
  mentions: number;
  citations: number;
}

interface VisibilityTrendChartProps {
  data: TrendData[];
  className?: string;
}

export const VisibilityTrendChart: React.FC<VisibilityTrendChartProps> = ({ data, className }) => {
  return (
    <ResponsiveContainer width="100%" height={320} className={className}>
      <LineChart data={data}>
        <defs>
          <linearGradient id="colorVisibility" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3}/>
            <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
          </linearGradient>
          <linearGradient id="colorMentions" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.3}/>
            <stop offset="95%" stopColor="#06B6D4" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
        <XAxis 
          dataKey="date" 
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
        <Legend />
        <Line 
          type="monotone" 
          dataKey="visibility" 
          stroke="#3B82F6"
          strokeWidth={2}
          dot={{ fill: '#3B82F6', r: 4 }}
          activeDot={{ r: 6 }}
          name="Visibility Score"
        />
        <Line 
          type="monotone" 
          dataKey="mentions" 
          stroke="#06B6D4"
          strokeWidth={2}
          dot={{ fill: '#06B6D4', r: 4 }}
          activeDot={{ r: 6 }}
          name="Mentions"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
