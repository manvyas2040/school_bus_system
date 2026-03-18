/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        surge: "#ef4444",
        skyrail: "#0ea5e9",
        mintline: "#22c55e",
        amberline: "#f59e0b",
      },
      boxShadow: {
        glow: "0 20px 50px rgba(14, 165, 233, 0.2)",
      },
      keyframes: {
        rise: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        rise: "rise 0.45s ease-out forwards",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Bricolage Grotesque'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
