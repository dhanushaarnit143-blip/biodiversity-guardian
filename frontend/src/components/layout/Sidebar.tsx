import type { FC } from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Map,
  Mic,
  Camera,
  Bot,
  Leaf,
  Wifi,
  WifiOff,
  Satellite,
} from "lucide-react";
import { cn } from "@/lib/utils";

// ── Nav items — maps 1:1 to the Streamlit sidebar radio ──────────────────────

interface NavItem {
  path:   string;
  label:  string;
  icon:   any;
}

const NAV_ITEMS: NavItem[] = [
  { path: "/",                icon: LayoutDashboard, label: "Overview"          },
  { path: "/map",             icon: Map,             label: "Biodiversity Map"  },
  { path: "/sound-monitor",   icon: Mic,             label: "Sound Monitor"     },
  { path: "/wildlife-monitor",icon: Camera,          label: "Wildlife Monitor"  },
  { path: "/conservation-ai", icon: Bot,             label: "Conservation AI"   },
];

// ── Telemetry widget (static — wire to /api/v1/overview/metrics later) ────────

interface TelemetryRowProps {
  label:  string;
  value:  string;
  status: "online" | "syncing" | "offline";
}

const TelemetryRow: FC<TelemetryRowProps> = ({ label, value, status }) => {
  const statusColor =
    status === "online"  ? "text-emerald-400" :
    status === "syncing" ? "text-amber-400"   : "text-rose-400";

  return (
    <div className="flex items-center justify-between text-xs py-0.5">
      <span className="text-text-muted">{label}</span>
      <strong className={cn("font-mono font-semibold", statusColor)}>{value}</strong>
    </div>
  );
};

// ── Sidebar ───────────────────────────────────────────────────────────────────

/**
 * Sidebar
 * -------
 * Left-navigation component replacing the Streamlit sidebar.
 *
 * Structure:
 *   ┌─ Brand header (Leaf icon + title) ──────────┐
 *   │  nav items (NavLink — active state emerald)  │
 *   │  ─────────────────────────────────────────── │
 *   │  System Telemetry glass widget               │
 *   │  ─────────────────────────────────────────── │
 *   │  Version footer                              │
 *   └──────────────────────────────────────────────┘
 *
 * The sidebar is `fixed` on desktop; on mobile it should be toggled via a
 * hamburger button (not implemented here — add as a follow-up).
 */
const Sidebar: FC = () => {
  const location = useLocation();

  return (
    <aside
      className={cn(
        // Layout
        "fixed top-0 left-0 h-screen flex flex-col z-50",
        // Width from CSS var (also used in #root grid)
        "w-[var(--sidebar-width)]",
        // Glassmorphism background (heavier than cards — sidebar is always visible)
        "glass-heavy",
        "border-r border-border",
        "py-3",
      )}
    >
      {/* ── Brand header ──────────────────────────────────────────────── */}
      <div className="flex items-center gap-2 px-3 pb-3 border-b border-border-subtle">
        <div className="flex items-center justify-center h-9 w-9 rounded-xl bg-emerald-500/15 shadow-glow-sm flex-shrink-0">
          <Leaf size={18} className="text-emerald-400" />
        </div>
        <div className="min-w-0">
          <h1 className="font-panchang font-semibold text-lg leading-tight text-gradient-eco">
            Guardian AI
          </h1>
          <p className="text-2xs text-text-faint uppercase tracking-widest">
            Biodiversity Monitor
          </p>
        </div>
      </div>

      {/* ── Navigation ────────────────────────────────────────────────── */}
      <nav className="flex-1 px-2 py-2 flex flex-col gap-0.5 overflow-y-auto">
        <p className="px-2 pb-1 text-2xs text-text-faint uppercase tracking-widest font-semibold">
          Navigation
        </p>
        {NAV_ITEMS.map(({ path, icon: Icon, label }) => {
          // Exact match for "/" to avoid always-active on all routes
          const isActive =
            path === "/"
              ? location.pathname === "/"
              : location.pathname.startsWith(path);

          return (
            <NavLink
              key={path}
              to={path}
              className={cn(
                // Base nav item
                "flex items-center gap-2 px-2 py-2 rounded-lg text-sm transition-all duration-150 group",
                isActive
                  ? // Active state — emerald tint
                    "bg-emerald-500/12 text-emerald-400 shadow-glow-sm border border-emerald-500/20"
                  : // Inactive state
                    "text-text-muted hover:text-text-primary hover:bg-obsidian-700/60 border border-transparent",
              )}
            >
              <Icon
                size={15}
                className={cn(
                  "flex-shrink-0 transition-colors",
                  isActive ? "text-emerald-400" : "text-text-faint group-hover:text-text-muted",
                )}
              />
              <span className="font-medium truncate">{label}</span>
              {/* Active indicator line on right edge */}
              {isActive && (
                <span className="ml-auto w-1 h-4 rounded-full bg-emerald-400 shadow-glow-sm" />
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* ── System Telemetry ──────────────────────────────────────────── */}
      <div className="mx-2 my-2">
        <div className="glass-sm rounded-lg p-2">
          <p className="text-2xs text-text-faint uppercase tracking-widest font-semibold mb-1.5">
            System Telemetry
          </p>
          <TelemetryRow label="PAM Sensors"   value="72 / 72 Online"  status="online"  />
          <TelemetryRow label="Camera Traps"  value="48 / 50 Online"  status="online"  />
          <TelemetryRow label="Satellite Link" value="Syncing…"        status="syncing" />
          <div className="flex items-center justify-between text-xs pt-1.5 mt-1 border-t border-border-subtle">
            <span className="text-text-faint">Last Sync</span>
            <span className="text-text-secondary font-mono">2 min ago</span>
          </div>
        </div>
      </div>

      {/* ── Version footer ────────────────────────────────────────────── */}
      <div className="border-t border-border-subtle pt-2 px-3">
        <p className="text-2xs text-text-faint text-center uppercase tracking-widest">
          Biodiversity Guardian AI v2.5
        </p>
        <p className="text-2xs text-obsidian-400 text-center mt-0.5">
          Eco-Cybernetics Design System
        </p>
      </div>
    </aside>
  );
};

export default Sidebar;
