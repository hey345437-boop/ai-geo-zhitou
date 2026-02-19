import { motion, HTMLMotionProps } from 'framer-motion';
import { cn } from '@utils/cn';

interface GlassCardProps extends HTMLMotionProps<'div'> {
  hover?: boolean;
}

export const GlassCard: React.FC<GlassCardProps> = ({ 
  children, 
  className,
  hover = true,
  ...props
}) => {
  return (
    <motion.div
      className={cn(
        "glass-card",
        className
      )}
      whileHover={hover ? { y: -4 } : undefined}
      transition={{ duration: 0.2 }}
      {...props}
    >
      {children}
    </motion.div>
  );
};
