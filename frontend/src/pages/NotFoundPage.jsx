import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-20 text-center sm:px-6">
      <h1 className="font-display text-5xl font-black text-ink">404</h1>
      <p className="mt-3 text-ink/70">The page you are looking for does not exist.</p>
      <Link to="/" className="mt-6 inline-block rounded-xl bg-ink px-4 py-2 font-semibold text-white">
        Go Home
      </Link>
    </div>
  );
}
