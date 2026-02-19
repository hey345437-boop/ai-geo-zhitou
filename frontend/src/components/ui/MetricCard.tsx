import { motion } from 'framer-motion';
import { cn } from '@utils/cn';
import { TrendIndicator } from './TrendIndicator';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: number;
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  trend,
  icon,
  className
}) => {
  return (
    <motion.div
      className={cn("glass-card metric-card p-6", className)}
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <div className="flex items-start justify-between mb-4">
        {icon && (
          <div className="p-3 rounded-xl bg-primary-500/10 text-primary-400">
            {icon}
          </div>
        )}
        {trend !== undefined && <TrendIndicator value={trend} />}
      </div>
      
      <h3 className="text-sm font-medium text-neutral-400 mb-2">
        {title}
      </h3>
      
      <div className="text-3xl font-bold text-neutral-50 mb-1">
        {value}
      </div>
      
      {subtitle && (
        <p className="text-xs text-neutral-500">{subtitle}</p>
      )}
    </motion.div>
  );
};
