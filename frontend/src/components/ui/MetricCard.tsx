import type { FC, ReactNode } from "react";
import { TrendingDown, TrendingUp, Minus } from "lucide-react";
import { cn } from "@/lib/utils";
import GlassCard from "./GlassCard";

// ── Types ─────────────────────────────────────────────────────────────────────

type Tone = "default" | "success" | "warning" | "danger" | "info";

interface MetricCardProps {
  /** Card title / label (e.g. "Biodiversity Score") */
  title: string;
  /** Primary value displayed prominently (e.g. "72 / 100" or "MODERATE") */
  value: string | number;
  /** Icon — Lucide component or any ReactNode */
  icon?: ReactNode;
  /** Small delta text (e.g. "-8.4%") — rendered with colour + trend icon */
  delta?: string;
  /** Contextual label for the delta (e.g. "vs 12m avg") */
  deltaLabel?: string;
  /** Sub-caption below the delta (e.g. "Shannon H': 3.41") */
  subtext?: string;
  /** Colour tone of the card — controls accent, shadow, and delta colour */
  tone?: Tone;
  /** When true the delta is rendered as negative even if the string is "+" */
  deltaIsNegative?: boolean;
  /** Additional Tailwind classes on the root GlassCard */
  className?: string;
}

// ── Tone → colour mapping ─────────────────────────────────────────────────────

const TONE_CONFIG: Record<Tone, {
  accent:      string;   // top border accent colour
  iconBg:      string;   // icon badge background
  iconColor:   string;   // icon colour
  valueShadow: string;   // text-shadow class on the KPI value
}> = {
  default: {
    accent:      "#10B981",
    iconBg:      "bg-emerald-500/15",
    iconColor:   "text-emerald-400",
    valueShadow: "drop-shadow-[0_0_10px_rgba(16,185,129,0.4)]",
  },
  success: {
    accent:      "#10B981",
    iconBg:      "bg-emerald-500/15",
    iconColor:   "text-emerald-400",
    valueShadow: "drop-shadow-[0_0_10px_rgba(16,185,129,0.4)]",
  },
  warning: {
    accent:      "#F59E0B",
    iconBg:      "bg-amber-500/15",
    iconColor:   "text-amber-400",
    valueShadow: "drop-shadow-[0_0_10px_rgba(245,158,11,0.4)]",
  },
  danger: {
    accent:      "#EF4444",
    iconBg:      "bg-rose-500/15",
    iconColor:   "text-rose-400",
    valueShadow: "drop-shadow-[0_0_10px_rgba(239,68,68,0.4)]",
  },
  info: {
    accent:      "#38BDF8",
    iconBg:      "bg-sky-500/15",
    iconColor:   "text-sky-400",
    valueShadow: "drop-shadow-[0_0_10px_rgba(56,189,248,0.4)]",
  },
};

// ── Delta helpers ─────────────────────────────────────────────────────────────

function parseDeltaDirection(delta: string, overrideNegative?: boolean): "up" | "down" | "neutral" {
  if (overrideNegative) return "down";
  if (delta.startsWith("+")) return "up";
  if (delta.startsWith("-")) return "down";
  return "neutral";
}

const DeltaIcon: FC<{ direction: "up" | "down" | "neutral" }> = ({ direction }) => {
  if (direction === "up")   return <TrendingUp  className="h-3 w-3" />;
  if (direction === "down") return <TrendingDown className="h-3 w-3" />;
  return <Minus className="h-3 w-3" />;
};

// ── Component ─────────────────────────────────────────────────────────────────

/**
 * MetricCard
 * ----------
 * KPI card component — maps 1:1 to the Streamlit `render_metric_card()` helper.
 *
 * Visual anatomy (top → bottom):
 *   ┌─ accent top border (tone colour) ─────────────────┐
 *   │  [Icon]          Title                            │
 *   │                  VALUE (large, font-panchang)     │
 *   │                  Δ delta   delta-label            │
 *   │                  subtext (muted caption)          │
 *   └───────────────────────────────────────────────────┘
 *
 * @example
 * <MetricCard
 *   title="Biodiversity Score"
 *   value="72 / 100"
 *   icon={<Leaf size={18} />}
 *   delta="-8.4%"
 *   deltaLabel="vs 12m avg"
 *   subtext="Shannon H': 3.41 (Healthy ref: 3.91)"
 *   tone="warning"
 *   deltaIsNegative
 * />
 */
const MetricCard: FC<MetricCardProps> = ({
  title,
  value,
  icon,
  delta,
  deltaLabel,
  subtext,
  tone = "default",
  deltaIsNegative,
  className,
}) => {
  const cfg = TONE_CONFIG[tone];
  const direction = delta ? parseDeltaDirection(String(delta), deltaIsNegative) : "neutral";

  const deltaColor =
    direction === "up"   ? "text-emerald-400" :
    direction === "down" ? "text-rose-400"    : "text-text-muted";

  return (
    <GlassCard
      className={cn("relative overflow-hidden group", className)}
      padded={false}
      style={{ borderTop: `2px solid ${cfg.accent}` } as React.CSSProperties}
    >
      {/* Subtle accent glow in top-left corner */}
      <div
        className="pointer-events-none absolute -top-8 -left-8 h-24 w-24 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-2xl"
        style={{ backgroundColor: `${cfg.accent}22` }}
      />

      <div className="relative p-3 flex flex-col gap-2">
        {/* ── Row 1: Icon + Title ─────────────────────────────── */}
        <div className="flex items-center gap-2">
          {icon && (
            <div className={cn("flex items-center justify-center h-8 w-8 rounded-lg flex-shrink-0", cfg.iconBg)}>
              <span className={cn("text-base leading-none", cfg.iconColor)}>
                {icon}
              </span>
            </div>
          )}
          <span className="text-xs font-semibold text-text-muted uppercase tracking-widest leading-tight">
            {title}
          </span>
        </div>

        {/* ── Row 2: KPI value ─────────────────────────────────── */}
        <div
          className={cn(
            "font-panchang font-bold leading-none text-text-primary",
            cfg.valueShadow,
            // Responsive font size — large for short values, smaller for long ones
            String(value).length > 8 ? "text-3xl" : "text-4xl",
          )}
        >
          {value}
        </div>

        {/* ── Row 3: Delta + delta label ─────────────────────────── */}
        {delta && (
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={cn("flex items-center gap-0.5 text-sm font-semibold font-mono", deltaColor)}>
              <DeltaIcon direction={direction} />
              {delta}
            </span>
            {deltaLabel && (
              <span className="text-xs text-text-faint">{deltaLabel}</span>
            )}
          </div>
        )}

        {/* ── Row 4: Subtext ────────────────────────────────────── */}
        {subtext && (
          <p className="text-xs text-text-muted leading-relaxed border-t border-border-subtle pt-2 mt-0.5">
            {subtext}
          </p>
        )}
      </div>
    </GlassCard>
  );
};

export default MetricCard;
