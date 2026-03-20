export default function Card({ title, subtitle, children, className = "", delay = 0 }) {
  return (
    <section
      className={`animate-rise rounded-3xl border border-white/60 bg-white/80 p-5 shadow-glow backdrop-blur-sm ${className}`}
      style={{ animationDelay: `${delay}ms` }}
    >
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="font-display text-xl font-bold text-ink">{title}</h3>}
          {subtitle && <p className="text-sm text-ink/60">{subtitle}</p>}
        </div>
      )}
      {children}
    </section>
  );
}
