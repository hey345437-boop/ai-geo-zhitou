import { TrendingUp, TrendingDown } from 'lucide-react';
import { cn } from '@utils/cn';

interface TrendIndicatorProps {
  value: number;
  className?: string;
}

export const TrendIndicator: React.FC<TrendIndicatorProps> = ({ value, className }) => {
  const isPositive = value > 0;
  const Icon = isPositive ? TrendingUp : TrendingDown;
  
  return (
    <div className={cn(
      "flex items-center gap-1 text-sm font-medium",
      isPositive ? "text-success-500" : "text-error-500",
      className
    )}>
      <Icon className="w-4 h-4" />
      {Math.abs(value)}%
    </div>
  );
};
