import type { Config } from "tailwindcss";
import plugin from "tailwindcss/plugin";

/**
 * Tailwind CSS configuration — Biodiversity Guardian "Dark Eco" design system.
 *
 * Design token map (from the Streamlit design-system.css):
 *
 *   Background  (60%) →  obsidian.*     (#0B1120 base)
 *   Accent      (30%) →  emerald.*      (#10B981 primary)
 *   Highlights  (10%) →  sky / amber / rose / violet
 *
 * 8-point spacing scale is surfaced via the `spacing` extension so Tailwind
 * utility classes (p-1, m-2, gap-4…) map directly to the design system:
 *   1 unit = 8px → p-1 = 8px, p-2 = 16px, p-4 = 32px, etc.
 *
 * Custom utilities added via plugin:
 *   - Glassmorphism variants:  .glass, .glass-sm, .glass-heavy
 *   - Text gradient:           .text-gradient-eco
 *   - Sensor status badges:    .badge-{online|offline|warning}
 */
const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}",
  ],
  darkMode: "class",  // controlled via <html class="dark"> — always dark in this app
  theme: {
    // ── Override Tailwind's default spacing with the 8-point scale ──────────
    spacing: {
      px: "1px",
      0:  "0",
      0.5: "4px",   // half-unit
      1:  "8px",
      2:  "16px",
      3:  "24px",
      4:  "32px",
      5:  "40px",
      6:  "48px",
      7:  "56px",
      8:  "64px",
      9:  "72px",
      10: "80px",
      11: "88px",
      12: "96px",
      14: "112px",
      16: "128px",
      20: "160px",
      24: "192px",
      28: "224px",
      32: "256px",
    },

    extend: {
      // ── Color Palette ────────────────────────────────────────────────────
      colors: {
        /**
         * Obsidian — 60% rule — background surfaces
         * Maps to CSS `--color-obsidian-*`
         */
        obsidian: {
          950: "#060C18",    // deepest page background
          900: "#0B1120",    // primary page bg
          850: "#0D1629",    // sidebar bg
          800: "#0F1A30",    // card bg
          750: "#111E38",    // card hover
          700: "#152140",    // borders / dividers
          600: "#1E2D4D",    // elevated panels
          500: "#243558",    // input backgrounds
          400: "#2E4170",    // active states
        },

        /**
         * Emerald — 30% rule — primary accent (the ecosystem "life" colour)
         * Maps to CSS `--color-emerald-*`
         */
        emerald: {
          50:  "#ECFDF5",
          100: "#D1FAE5",
          200: "#A7F3D0",
          300: "#6EE7B7",
          400: "#34D399",   // light glow / secondary text
          500: "#10B981",   // PRIMARY_ACCENT — borders, icons, hover
          600: "#059669",
          700: "#047857",
          800: "#065F46",
          900: "#064E3B",
          950: "#022C22",
        },

        /**
         * 10% rule highlights — status colours and data visualisation
         */
        sky: {
          300: "#7DD3FC",
          400: "#38BDF8",   // INFO, camera-trap markers
          500: "#0EA5E9",
          600: "#0284C7",
        },
        amber: {
          300: "#FCD34D",
          400: "#FBBF24",
          500: "#F59E0B",   // WARNING
          600: "#D97706",
        },
        rose: {
          400: "#F87171",
          500: "#EF4444",   // DANGER / CRITICAL
          600: "#DC2626",
        },
        violet: {
          400: "#C084FC",
          500: "#A855F7",   // reptile category colour
        },
        orange: {
          400: "#FB923C",
          500: "#F97316",   // fire / wildfire highlights
        },

        /**
         * Text scale — maps 1:1 to the Streamlit CSS vars
         */
        text: {
          primary:   "#F8FAFC",  // --text-primary
          secondary: "#CBD5E1",  // --text-secondary
          muted:     "#94A3B8",  // --text-muted
          faint:     "#64748B",  // --text-faint
        },

        /**
         * Border scale
         */
        border: {
          DEFAULT: "rgba(51, 65, 85, 0.5)",
          subtle:  "rgba(30, 41, 59, 0.4)",
          accent:  "rgba(16, 185, 129, 0.3)",
          danger:  "rgba(239, 68, 68, 0.4)",
        },
      },

      // ── Typography ───────────────────────────────────────────────────────
      fontFamily: {
        /**
         * Panchang — loaded via @import in index.css from Fontshare CDN.
         * Used for headings, KPI values, and brand identity.
         */
        panchang: ["Panchang", "system-ui", "sans-serif"],
        /**
         * Inter — clean sans-serif for body/UI text.
         * Google Fonts CDN import also in index.css.
         */
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        /**
         * JetBrains Mono — monospace for numeric readouts.
         */
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },

      // ── Font sizes with matching line-heights ────────────────────────────
      fontSize: {
        "2xs": ["10px", { lineHeight: "14px" }],
        xs:    ["11px", { lineHeight: "16px" }],
        sm:    ["12px", { lineHeight: "18px" }],
        base:  ["13px", { lineHeight: "20px" }],
        md:    ["14px", { lineHeight: "22px" }],
        lg:    ["15px", { lineHeight: "24px" }],
        xl:    ["16px", { lineHeight: "26px" }],
        "2xl": ["18px", { lineHeight: "28px" }],
        "3xl": ["20px", { lineHeight: "30px" }],
        "4xl": ["24px", { lineHeight: "34px" }],
        "5xl": ["28px", { lineHeight: "38px" }],
        "6xl": ["32px", { lineHeight: "44px" }],
        kpi:   ["36px", { lineHeight: "48px", fontWeight: "700" }],
      },

      // ── Border radius ────────────────────────────────────────────────────
      borderRadius: {
        none: "0",
        sm:   "4px",
        DEFAULT: "8px",
        md:   "10px",
        lg:   "12px",
        xl:   "16px",
        "2xl":"20px",
        full: "9999px",
      },

      // ── Box shadows — glassmorphism + glow effects ───────────────────────
      boxShadow: {
        // Standard glassmorphism card shadow
        glass: "0 4px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06)",
        // Heavier panel shadow
        "glass-lg": "0 8px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08)",
        // Emerald glow — active / hover states
        "glow-emerald": "0 0 20px rgba(16, 185, 129, 0.3), 0 0 40px rgba(16, 185, 129, 0.1)",
        // Danger glow — alert states
        "glow-danger":  "0 0 20px rgba(239, 68, 68, 0.3)",
        // Ambient glow for KPI cards
        "glow-sm":      "0 0 12px rgba(16, 185, 129, 0.2)",
        // Inset border highlight (top edge shimmer)
        "inner-highlight": "inset 0 1px 0 rgba(255, 255, 255, 0.1)",
        none: "none",
      },

      // ── Backdrop blur ────────────────────────────────────────────────────
      backdropBlur: {
        xs:  "4px",
        sm:  "8px",
        DEFAULT: "12px",
        lg:  "20px",
        xl:  "32px",
      },

      // ── Animations ───────────────────────────────────────────────────────
      keyframes: {
        "fade-in": {
          "0%":   { opacity: "0", transform: "translateY(6px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pulse-emerald": {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(16, 185, 129, 0.4)" },
          "50%":       { boxShadow: "0 0 0 8px rgba(16, 185, 129, 0)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "status-blink": {
          "0%, 100%": { opacity: "1" },
          "50%":       { opacity: "0.3" },
        },
      },
      animation: {
        "fade-in":       "fade-in 0.35s ease-out both",
        "pulse-emerald": "pulse-emerald 2s ease-in-out infinite",
        shimmer:         "shimmer 2.5s linear infinite",
        "status-blink":  "status-blink 1.5s ease-in-out infinite",
      },

      // ── Grid template areas shortcut ─────────────────────────────────────
      gridTemplateColumns: {
        "kpi-4":  "repeat(4, minmax(0, 1fr))",
        "kpi-2":  "repeat(2, minmax(0, 1fr))",
        sidebar:  "260px 1fr",
      },
    },
  },

  plugins: [
    /**
     * Custom utility classes for the glassmorphism design system.
     * These can't be expressed as simple Tailwind utilities because they
     * require multiple CSS properties together.
     */
    plugin(function ({ addComponents, addUtilities, theme }) {
      // ── Glassmorphism card variants ──────────────────────────────────────
      addComponents({
        ".glass": {
          backgroundColor: "rgba(11, 17, 32, 0.7)",
          backdropFilter:  "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
          border:          "1px solid rgba(51, 65, 85, 0.5)",
          boxShadow:       theme("boxShadow.glass"),
          borderRadius:    theme("borderRadius.lg"),
        },
        ".glass-sm": {
          backgroundColor: "rgba(11, 17, 32, 0.5)",
          backdropFilter:  "blur(8px)",
          WebkitBackdropFilter: "blur(8px)",
          border:          "1px solid rgba(30, 41, 59, 0.4)",
          boxShadow:       theme("boxShadow.glass"),
          borderRadius:    theme("borderRadius.DEFAULT"),
        },
        ".glass-heavy": {
          backgroundColor: "rgba(6, 12, 24, 0.85)",
          backdropFilter:  "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border:          "1px solid rgba(51, 65, 85, 0.6)",
          boxShadow:       theme("boxShadow.glass-lg"),
          borderRadius:    theme("borderRadius.xl"),
        },
        // Accent (emerald) bordered variant
        ".glass-accent": {
          backgroundColor: "rgba(11, 17, 32, 0.7)",
          backdropFilter:  "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
          border:          "1px solid rgba(16, 185, 129, 0.3)",
          boxShadow:       theme("boxShadow.glass"),
          borderRadius:    theme("borderRadius.lg"),
        },
      });

      // ── Text gradient utility ────────────────────────────────────────────
      addUtilities({
        ".text-gradient-eco": {
          background: "linear-gradient(135deg, #10B981 0%, #34D399 50%, #38BDF8 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
        },
        ".text-gradient-danger": {
          background: "linear-gradient(135deg, #EF4444 0%, #F97316 100%)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
        },
      });

      // ── Status indicator dots ─────────────────────────────────────────────
      addComponents({
        ".status-dot": {
          display: "inline-block",
          width: "8px",
          height: "8px",
          borderRadius: "50%",
          flexShrink: "0",
        },
        ".status-dot-online":  { backgroundColor: "#10B981" },
        ".status-dot-offline": { backgroundColor: "#EF4444" },
        ".status-dot-warning": { backgroundColor: "#F59E0B", animation: "status-blink 1.5s ease-in-out infinite" },
      });

      // ── Risk level badge variants ─────────────────────────────────────────
      addComponents({
        ".badge-risk": {
          display: "inline-flex",
          alignItems: "center",
          gap: "4px",
          padding: "3px 10px",
          borderRadius: "9999px",
          fontSize: "11px",
          fontWeight: "600",
          textTransform: "uppercase",
          letterSpacing: "0.05em",
        },
        ".badge-LOW":      { backgroundColor: "rgba(16, 185, 129, 0.15)", color: "#34D399", border: "1px solid rgba(16, 185, 129, 0.4)" },
        ".badge-MODERATE": { backgroundColor: "rgba(245, 158, 11, 0.15)", color: "#FBBF24", border: "1px solid rgba(245, 158, 11, 0.4)" },
        ".badge-HIGH":     { backgroundColor: "rgba(239, 68, 68, 0.15)",  color: "#F87171", border: "1px solid rgba(239, 68, 68, 0.4)" },
        ".badge-CRITICAL": { backgroundColor: "rgba(239, 68, 68, 0.25)",  color: "#EF4444", border: "1px solid rgba(239, 68, 68, 0.6)" },
        ".badge-Stable":   { backgroundColor: "rgba(16, 185, 129, 0.15)", color: "#34D399", border: "1px solid rgba(16, 185, 129, 0.4)" },
        ".badge-Declining":{ backgroundColor: "rgba(245, 158, 11, 0.15)", color: "#FBBF24", border: "1px solid rgba(245, 158, 11, 0.4)" },
        ".badge-Critical": { backgroundColor: "rgba(239, 68, 68, 0.25)",  color: "#EF4444", border: "1px solid rgba(239, 68, 68, 0.6)" },
      });
    }),
  ],
};

export default config;
