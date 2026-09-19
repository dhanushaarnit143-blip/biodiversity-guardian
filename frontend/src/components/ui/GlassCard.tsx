import type { FC, ReactNode } from "react";
import { cn } from "@/lib/utils";

// ── Prop types ────────────────────────────────────────────────────────────────

interface GlassCardProps {
  /** Card content */
  children: ReactNode;
  /** Additional Tailwind classes */
  className?: string;
  /** Glassmorphism intensity */
  variant?: "default" | "sm" | "heavy" | "accent";
  /** Optional left-border accent colour (hex or tailwind colour value) */
  accentColor?: string;
  /** Pad the card contents (default: true) */
  padded?: boolean;
  /** Click handler — makes the card interactive */
  onClick?: () => void;
  /** Optional custom CSS properties */
  style?: React.CSSProperties;
}

/**
 * GlassCard
 * ---------
 * The primary surface component for the Dark Eco design system.
 *
 * Maps directly to the Streamlit `render_glass_panel()` helper.
 * Uses `backdrop-filter: blur()` + dark obsidian background with subtle
 * border and box-shadow for the glassmorphism effect.
 *
 * @example
 * <GlassCard>
 *   <h3>Wetland Zone A</h3>
 *   <p>Shannon H': 2.81</p>
 * </GlassCard>
 *
 * @example <GlassCard variant="accent" accentColor="#EF4444">...</GlassCard>
 */
const GlassCard: FC<GlassCardProps> = ({
  children,
  className,
  variant = "default",
  accentColor,
  padded = true,
  onClick,
  style,
}) => {
  const variantClass = {
    default: "glass",
    sm:      "glass-sm",
    heavy:   "glass-heavy",
    accent:  "glass-accent",
  }[variant];

  const mergedStyle: React.CSSProperties = {
    ...(accentColor ? { borderLeft: `3px solid ${accentColor}` } : {}),
    ...style,
  };

  return (
    <div
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => e.key === "Enter" && onClick() : undefined}
      onClick={onClick}
      style={mergedStyle}
      className={cn(
        // Base glassmorphism (injected by Tailwind plugin)
        variantClass,
        // Animate in on mount
        "animate-fade-in",
        // Padding
        padded && "p-3",
        // Interactive state
        onClick &&
          "cursor-pointer hover:shadow-glow-emerald hover:border-emerald-500/40 transition-all duration-250",
        className,
      )}
    >
      {children}
    </div>
  );
};

export default GlassCard;
