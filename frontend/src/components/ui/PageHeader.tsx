interface PageHeaderProps {
  title: string;
  subtitle?: string;
  icon?: React.ReactNode;
  actions?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  icon,
  actions
}) => {
  return (
    <header className="mb-8">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3 mb-3">
            {icon && (
              <div className="p-2 rounded-lg bg-accent-500/10">
                {icon}
              </div>
            )}
            <h1 className="text-3xl font-semibold text-neutral-50">
              {title}
            </h1>
          </div>
          {subtitle && (
            <p className="text-neutral-400">{subtitle}</p>
          )}
        </div>
        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </header>
  );
};
