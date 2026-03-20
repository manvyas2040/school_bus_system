export default function Spinner({ label = "Loading..." }) {
  return (
    <div className="inline-flex items-center gap-2 text-sm text-ink/70">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-ink/20 border-t-skyrail" />
      {label}
    </div>
  );
}
