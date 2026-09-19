/**
 * TopNav.tsx — Biodiversity Guardian AI
 *
 * Fixed top command header replacing the left sidebar layout.
 * Features:
 *  - Logo + system status badges
 *  - Nav tabs (react-router-dom NavLink)
 *  - Search bar
 *  - Notification bell with flyout dropdown
 *  - User profile chip
 *  - Mobile bottom navigation bar
 */

import { useState, useEffect, useRef } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/apiClient";
import {
  LayoutDashboard,
  Map,
  Mic,
  Brain,
  Search,
  Bell,
  AlertTriangle,
  Info,
  X,
  RefreshCw,
} from "lucide-react";

// ── Nav items ──────────────────────────────────────────────────────────────────
const NAV_ITEMS = [
  { label: "Overview",       icon: LayoutDashboard, to: "/"                },
  { label: "Bio Map",        icon: Map,             to: "/map"             },
  { label: "Sound & Vision", icon: Mic,             to: "/sound-monitor"   },
  { label: "Analytics & AI", icon: Brain,           to: "/conservation-ai" },
] as const;

// ── Notification data ──────────────────────────────────────────────────────────
const NOTIFICATIONS = [
  {
    id: 1,
    icon: AlertTriangle,
    iconColor: "text-red-400",
    bgColor: "rgba(239,68,68,0.08)",
    borderColor: "rgba(239,68,68,0.2)",
    severity: "CRITICAL",
    severityColor: "text-red-400",
    message: "Zone 04 Chainsaw Acoustic Signature Detected",
    time: "2 min ago",
  },
  {
    id: 2,
    icon: AlertTriangle,
    iconColor: "text-amber-400",
    bgColor: "rgba(245,158,11,0.08)",
    borderColor: "rgba(245,158,11,0.2)",
    severity: "MODERATE",
    severityColor: "text-amber-400",
    message: "Jaguar IR Camera Triggered — Grid E-7",
    time: "8 min ago",
  },
  {
    id: 3,
    icon: Info,
    iconColor: "text-emerald-400",
    bgColor: "rgba(16,185,129,0.08)",
    borderColor: "rgba(16,185,129,0.2)",
    severity: "INFO",
    severityColor: "text-emerald-400",
    message: "Species Count Updated — 24 taxa confirmed",
    time: "15 min ago",
  },
] as const;

// ── Helper: is this route active? ─────────────────────────────────────────────
function useIsActive(to: string) {
  const { pathname } = useLocation();
  if (to === "/") return pathname === "/";
  return pathname.startsWith(to);
}

// ── Individual nav tab ─────────────────────────────────────────────────────────
function NavTab({ item }: { item: (typeof NAV_ITEMS)[number] }) {
  const Icon = item.icon;
  const active = useIsActive(item.to);

  return (
    <NavLink
      to={item.to}
      end={item.to === "/"}
      className={[
        "relative flex items-center gap-1.5 px-3 py-1 text-[11px] font-semibold tracking-widest uppercase",
        "transition-colors duration-200 whitespace-nowrap h-full",
        "hover:text-emerald-400",
        active ? "text-emerald-400" : "text-slate-400",
      ].join(" ")}
    >
      <Icon size={13} strokeWidth={2} />
      {item.label}
      {/* Active underline */}
      {active && (
        <span
          className="absolute bottom-0 left-0 right-0 h-[2px] rounded-t-full"
          style={{ background: "linear-gradient(90deg, #10B981, #34D399)" }}
        />
      )}
    </NavLink>
  );
}

// ── Mobile nav item ────────────────────────────────────────────────────────────
function MobileNavItem({
  to,
  label,
  Icon,
}: {
  to: string;
  label: string;
  Icon: React.ComponentType<any>;
}) {
  const active = useIsActive(to);
  return (
    <NavLink
      to={to}
      end={to === "/"}
      className="relative flex-1 flex flex-col items-center justify-center gap-1 transition-colors"
    >
      <Icon
        size={18}
        strokeWidth={2}
        className={active ? "text-emerald-400" : "text-slate-500"}
      />
      <span
        className={[
          "text-[9px] font-semibold tracking-widest uppercase",
          active ? "text-emerald-400" : "text-slate-500",
        ].join(" ")}
      >
        {label}
      </span>
      {active && (
        <span
          className="absolute bottom-0 w-8 h-[2px] rounded-t-full"
          style={{ background: "linear-gradient(90deg, #10B981, #34D399)" }}
        />
      )}
    </NavLink>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────
export default function TopNav() {
  const [notificationOpen, setNotificationOpen] = useState(false);
  const [searchValue, setSearchValue] = useState("");
  const [isSyncing, setIsSyncing] = useState(false);
  const notifRef = useRef<HTMLDivElement>(null);
  const queryClient = useQueryClient();

  const handleSyncTelemetry = async () => {
    try {
      setIsSyncing(true);
      await apiClient.post("/api/v1/overview/sync");
      await queryClient.invalidateQueries();
    } catch (err) {
      console.error("Telemetry sync error:", err);
    } finally {
      setIsSyncing(false);
    }
  };

  // Close notification dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) {
        setNotificationOpen(false);
      }
    }
    if (notificationOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [notificationOpen]);

  return (
    <>
      {/* ── Desktop top bar ─────────────────────────────────────────────────── */}
      <header
        className="fixed top-0 left-0 right-0 z-50 flex items-center gap-3 px-4"
        style={{
          height: "60px",
          background: "rgba(6, 12, 24, 0.92)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderBottom: "1px solid rgba(0, 255, 135, 0.2)",
        }}
      >
        {/* ── Logo section ──────────────────────────────────────────────────── */}
        <div className="flex items-center gap-2.5 shrink-0">
          <img
            src="https://lh3.googleusercontent.com/aida/AEtjO1WSDn9WbpenjC7--BqXHi8_05jQ7R1fNxNcsegjL0OKYa1ZRmipZmiYorO-dDs82_agbKPEgrsZSnMQ9TuGrJYZmkj6UHnD76NWVXuGb8GetDTWyMoCqlxgxe7g_csq2NwBDNJ9ZPTIOZpSPHzo4RMnCvPHB3jbzsAup7CGDMU9Eq0AnUQ_bWHRcefZaSWK9tO0sOqYknvmVojs8iYpJMkly1VUptFlhkmUHhGxFO_2djxNrnZdVgseBxA"
            alt="Biodiversity Guardian AI logo"
            className="h-8 w-8 rounded-lg object-cover"
            draggable={false}
          />
          <div className="flex flex-col leading-none">
            <span
              className="text-[11px] font-bold tracking-[0.18em] uppercase"
              style={{
                fontFamily: "var(--font-panchang)",
                background: "linear-gradient(90deg, #10B981, #34D399, #6EE7B7)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              Biodiversity Guardian AI
            </span>
            <span className="text-[9px] text-slate-500 tracking-[0.22em] uppercase mt-0.5">
              Canopy Prime // Sec-04
            </span>
          </div>
        </div>

        {/* ── Status badges ─────────────────────────────────────────────────── */}
        <div className="hidden lg:flex items-center gap-2 shrink-0">
          {/* System Online */}
          <div
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[9px] font-semibold tracking-widest uppercase"
            style={{
              background: "rgba(16,185,129,0.1)",
              border: "1px solid rgba(16,185,129,0.25)",
              color: "#34D399",
            }}
          >
            <span className="relative flex h-1.5 w-1.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-400" />
            </span>
            System Online
          </div>
          {/* Offline Ready */}
          <div
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[9px] font-semibold tracking-widest uppercase"
            style={{
              background: "rgba(100,116,139,0.12)",
              border: "1px solid rgba(100,116,139,0.25)",
              color: "#94A3B8",
            }}
          >
            <span className="h-1.5 w-1.5 rounded-full bg-slate-400 inline-block" />
            Local AI • Offline Ready
          </div>
          {/* Sync Live Telemetry Button */}
          <button
            onClick={handleSyncTelemetry}
            disabled={isSyncing}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[9px] font-semibold tracking-widest uppercase transition-all bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/40 text-emerald-300 disabled:opacity-50"
            title="Fetch live telemetry from Open-Meteo & iNaturalist"
          >
            <RefreshCw
              size={11}
              className={isSyncing ? "animate-spin text-emerald-400" : "text-emerald-400"}
            />
            {isSyncing ? "Syncing..." : "Sync Live APIs"}
          </button>
        </div>

        {/* ── Spacer ────────────────────────────────────────────────────────── */}
        <div className="flex-1" />

        {/* ── Nav tabs (center) ─────────────────────────────────────────────── */}
        <nav className="hidden md:flex items-stretch h-full gap-0.5">
          {NAV_ITEMS.map((item) => (
            <NavTab key={item.to} item={item} />
          ))}
        </nav>

        {/* ── Spacer ────────────────────────────────────────────────────────── */}
        <div className="flex-1" />

        {/* ── Search bar ────────────────────────────────────────────────────── */}
        <div className="hidden md:flex items-center gap-2 shrink-0">
          <div
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
            style={{
              width: "220px",
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.1)",
            }}
          >
            <Search size={12} className="text-slate-500 shrink-0" />
            <input
              type="text"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              placeholder="Search species, zones, audio nodes..."
              className="bg-transparent text-[11px] text-slate-300 placeholder:text-slate-600 w-full focus:outline-none"
            />
          </div>
        </div>

        {/* ── Right cluster: Notification + Profile ─────────────────────────── */}
        <div className="flex items-center gap-3 shrink-0">

          {/* Notification bell */}
          <div className="relative" ref={notifRef}>
            <button
              onClick={() => setNotificationOpen((v) => !v)}
              className="relative flex items-center justify-center w-8 h-8 rounded-lg hover:bg-white/5 transition-colors"
              aria-label="Toggle notifications"
            >
              <Bell size={16} className="text-slate-400 hover:text-emerald-400 transition-colors" />
              {/* Badge */}
              <span
                className="absolute -top-0.5 -right-0.5 flex items-center justify-center w-4 h-4 rounded-full text-[9px] font-bold text-white"
                style={{ background: "#EF4444" }}
              >
                3
              </span>
            </button>

            {/* Notification flyout */}
            {notificationOpen && (
              <div
                className="absolute right-0 top-[calc(100%+8px)] w-[340px] rounded-xl overflow-hidden z-50"
                style={{
                  background: "rgba(9,15,30,0.97)",
                  backdropFilter: "blur(24px)",
                  WebkitBackdropFilter: "blur(24px)",
                  border: "1px solid rgba(51,65,85,0.6)",
                  boxShadow: "0 8px 32px rgba(0,0,0,0.6)",
                }}
              >
                {/* Header */}
                <div
                  className="flex items-center justify-between px-4 py-3"
                  style={{ borderBottom: "1px solid rgba(51,65,85,0.4)" }}
                >
                  <div className="flex items-center gap-2">
                    <Bell size={13} className="text-emerald-400" />
                    <span className="text-[11px] font-bold tracking-widest uppercase text-slate-300">
                      Active Alerts
                    </span>
                    <span
                      className="px-1.5 py-0.5 rounded-full text-[9px] font-bold text-white"
                      style={{ background: "#EF4444" }}
                    >
                      3
                    </span>
                  </div>
                  <button
                    onClick={() => setNotificationOpen(false)}
                    className="text-slate-500 hover:text-slate-300 transition-colors"
                  >
                    <X size={13} />
                  </button>
                </div>

                {/* Alert list */}
                <div className="flex flex-col p-2 gap-1.5">
                  {NOTIFICATIONS.map((n) => {
                    const Icon = n.icon;
                    return (
                      <div
                        key={n.id}
                        className="flex items-start gap-3 px-3 py-2.5 rounded-lg cursor-pointer hover:brightness-125 transition-all"
                        style={{
                          background: n.bgColor,
                          border: `1px solid ${n.borderColor}`,
                        }}
                      >
                        <div className={`mt-0.5 shrink-0 ${n.iconColor}`}>
                          <Icon size={14} strokeWidth={2} />
                        </div>
                        <div className="flex flex-col gap-0.5 min-w-0">
                          <span className={`text-[9px] font-black tracking-widest uppercase ${n.severityColor}`}>
                            {n.severity}
                          </span>
                          <p className="text-[11px] text-slate-200 leading-snug">
                            {n.message}
                          </p>
                          <span className="text-[9px] text-slate-500 mt-0.5">
                            {n.time}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Footer */}
                <div
                  className="px-4 py-2.5 text-center"
                  style={{ borderTop: "1px solid rgba(51,65,85,0.4)" }}
                >
                  <button className="text-[10px] text-emerald-400 hover:text-emerald-300 tracking-widest uppercase font-semibold transition-colors">
                    View All Alerts →
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User profile */}
          <div className="hidden md:flex items-center gap-2 shrink-0">
            {/* Avatar */}
            <div
              className="flex items-center justify-center w-8 h-8 rounded-full text-[11px] font-black text-white tracking-wide shrink-0"
              style={{
                background: "linear-gradient(135deg, #059669, #10B981)",
                boxShadow: "0 0 0 2px rgba(16,185,129,0.3)",
              }}
            >
              VM
            </div>
            <div className="flex flex-col leading-none">
              <span className="text-[10px] font-bold text-slate-200 tracking-wide uppercase">
                Dr. V. Moreau
              </span>
              <span className="text-[9px] text-slate-500 tracking-wider uppercase mt-0.5">
                Field Bio-Analyst
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* ── Mobile bottom navigation bar ──────────────────────────────────────── */}
      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 z-50 flex items-stretch"
        style={{
          background: "rgba(6, 12, 24, 0.96)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderTop: "1px solid rgba(0, 255, 135, 0.2)",
          height: "56px",
        }}
      >
        {NAV_ITEMS.map((item) => (
          <MobileNavItem
            key={item.to}
            to={item.to}
            label={item.label}
            Icon={item.icon}
          />
        ))}
      </nav>
    </>
  );
}
