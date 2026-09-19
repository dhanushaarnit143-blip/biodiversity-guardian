import { useState } from "react";
import {
  FileText,
  Navigation,
  Zap,
  Activity,
  Leaf,
  Eye,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
  Radio,
  X,
  Plus,
  Shield,
  CheckCircle,
  Download,
  Crosshair,
} from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import MetricCard from "@/components/ui/MetricCard";

const CANOPY_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuCJ8L-HmDUv7A82WjHj79aQBuHaI6soubxVBptfJzTubGzo42M8LWL17h88WhjI6E1DuuMZukoR0Exv4Tp0CYbU-J2i-ZQu_OsFUffrICFFzCbjJsEwbp1pkXN_d58srRXtWMmeDBv-5gCNn-C-sT3MfOflTkRB5TtNhoNuEqPkCWxEUsRW8tkjSiKoBwNyf74Vmonhh1ItdT3HlUeFERvP9KKqA7ep7MCp9Zmquy3U8y_dQXjyXYlFUw";
const JAGUAR_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuBLzADIm0FTKdvvGKvL1L-PWqiiK1OOnEKtvad8UBoe90PM-Zvvu1ei6uxIhQSi8Pq9k4LSSKAl1bmBZVQZ16OzrPKQdbm9haKt7j8dwaFx9oVii3TdWkcWMlOWoW1SezhEQCU3olvhbaCh1rVIpJrTaSeuttIila4iR82Zi1aJ2ERD3FMBxPbGhK_W2w_u8cSgymxbtfBQ6QrP27PwvXYP3TgY-HEGQmDobIiprEU_y1ZEUY-U0yhxnw";

export default function OverviewPage() {
  const [showExportModal, setShowExportModal] = useState(false);
  const [showUavModal, setShowUavModal] = useState(false);
  const [showClimateModal, setShowClimateModal] = useState(false);
  const [showActionPlanModal, setShowActionPlanModal] = useState(false);

  const [aiRationaleExpanded, setAiRationaleExpanded] = useState(false);

  // UAV Modal state
  const [flightSpeed, setFlightSpeed] = useState(35);
  const [uavLaunched, setUavLaunched] = useState(false);

  // Climate Simulator state
  const [tempAnomaly, setTempAnomaly] = useState(2.5);
  const [humidityDeficit, setHumidityDeficit] = useState(35);

  // Action Center state
  const [priority1Dispatched, setPriority1Dispatched] = useState(false);
  const [priority2PatrolActive, setPriority2PatrolActive] = useState(false);

  return (
    <div className="space-y-4 pb-12">
      {/* ── 1. Telemetry Strip ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 rounded-xl bg-obsidian-850/80 border border-emerald-500/20 backdrop-blur-md">
        <div className="flex items-center gap-3 font-mono text-xs text-text-muted">
          <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="font-semibold tracking-wider">CANOPY-04 ARRAY</span>
          </div>
          <span>LAT <strong className="text-emerald-300">-03.4653°</strong></span>
          <span className="text-slate-600">|</span>
          <span>LON <strong className="text-emerald-300">-62.2159°</strong></span>
          <span className="text-slate-600">|</span>
          <span className="text-slate-400">ELEVATION <strong>142m MSL</strong></span>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setShowExportModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wider uppercase transition-all bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 hover:border-amber-500/60"
          >
            <FileText size={14} />
            <span>Export PDF Briefing</span>
          </button>

          <button
            onClick={() => setShowUavModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wider uppercase transition-all bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 hover:border-sky-500/60"
          >
            <Navigation size={14} />
            <span>Dispatch Field Patrol</span>
          </button>

          <button
            onClick={() => setShowClimateModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wider uppercase transition-all bg-rose-500/15 hover:bg-rose-500/25 text-rose-300 border border-rose-500/30 hover:border-rose-500/60"
          >
            <Zap size={14} />
            <span>Simulate Climate Shock</span>
          </button>
        </div>
      </div>

      {/* ── 2. Mission Banner ── */}
      <GlassCard variant="heavy" className="relative overflow-hidden border-emerald-500/30">
        <div className="absolute -right-20 -top-20 w-80 h-80 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none" />
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div className="space-y-2 max-w-3xl">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono tracking-widest uppercase bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                ACTIVE RECON PROTOCOL
              </span>
              <span className="flex items-center gap-1 text-xs text-text-muted">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
                Live 96kHz bioacoustic buffer active
              </span>
            </div>

            <h1 className="text-xl sm:text-2xl font-panchang font-bold tracking-wide text-gradient-eco leading-tight">
              Understand ecosystems before they become endangered
            </h1>

            <div className="flex items-center gap-2 p-2 rounded-lg bg-obsidian-950/60 border border-border-subtle font-mono text-xs">
              <span className="text-amber-400 font-semibold flex items-center gap-1">
                <Radio size={13} className="text-amber-400 animate-pulse" />
                DETECTION:
              </span>
              <span className="text-text-primary italic">Harpyhaliaetus solitarius</span>
              <span className="text-text-muted">(Solitary Crowned Eagle)</span>
              <span className="ml-auto text-emerald-400 font-bold bg-emerald-500/15 px-2 py-0.5 rounded text-[11px] border border-emerald-500/30">
                98.4% CONFIDENCE
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 shrink-0 font-mono text-xs">
            <div className="p-2 rounded-lg bg-obsidian-900/80 border border-border text-center">
              <span className="text-text-faint text-[10px] block">ACOUSTIC ARRAY</span>
              <span className="text-emerald-400 font-bold text-sm">48 PAM NODES</span>
            </div>
            <div className="p-2 rounded-lg bg-obsidian-900/80 border border-border text-center">
              <span className="text-text-faint text-[10px] block">OPTICAL TRAPS</span>
              <span className="text-sky-400 font-bold text-sm">CAM ACTIVE</span>
            </div>
            <div className="p-2 rounded-lg bg-obsidian-900/80 border border-border text-center">
              <span className="text-text-faint text-[10px] block">INFERENCE MODEL</span>
              <span className="text-emerald-400 font-bold text-sm">AI ENGINE v2.4</span>
            </div>
            <div className="p-2 rounded-lg bg-obsidian-900/80 border border-border text-center">
              <span className="text-text-faint text-[10px] block">EXPLAINABILITY</span>
              <span className="text-amber-400 font-bold text-sm">SHAP REALTIME</span>
            </div>
          </div>
        </div>
      </GlassCard>

      {/* ── 3. Four Metric Cards ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard
          title="Species Monitored"
          value="24+"
          icon={<Leaf size={18} />}
          delta="+3 taxa"
          deltaLabel="this season"
          subtext="Covering 4 key taxonomic classes"
          tone="default"
        />
        <MetricCard
          title="Biodiversity Score"
          value="82.4"
          icon={<Activity size={18} />}
          delta="+4.2%"
          deltaLabel="vs baseline"
          subtext="Health Index: 82% Optimal Range"
          tone="success"
        />
        <MetricCard
          title="24H Observations"
          value="1,248"
          icon={<Eye size={18} />}
          delta="+184"
          deltaLabel="sensor triggers"
          subtext="1,024 automated · 224 verified"
          tone="info"
        />
        <MetricCard
          title="Threats Detected"
          value="31"
          icon={<AlertTriangle size={18} />}
          delta="27 mod · 4 crit"
          deltaLabel="unresolved"
          subtext="Zone 04: Acoustic chainsaw anomaly"
          tone="danger"
          deltaIsNegative
        />
      </div>

      {/* ── 4. BHI Dual-Ring Gauge + Ecosystem Risk Engine ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Biodiversity Health Index Card */}
        <GlassCard className="space-y-4">
          <div className="flex items-center justify-between border-b border-border-subtle pb-2">
            <div className="flex items-center gap-2">
              <Shield size={16} className="text-emerald-400" />
              <h2 className="text-sm font-panchang font-bold uppercase tracking-wider text-text-primary">
                Biodiversity Health Index (BHI)
              </h2>
            </div>
            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              HEALTHY TIER
            </span>
          </div>

          <div className="flex flex-col sm:flex-row items-center gap-6">
            {/* Dual Ring Circular Gauge */}
            <div className="relative w-40 h-40 shrink-0 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
                {/* Background tracks */}
                <circle cx="80" cy="80" r="68" stroke="#152140" strokeWidth="10" fill="none" />
                <circle cx="80" cy="80" r="50" stroke="#152140" strokeWidth="8" fill="none" />
                
                {/* Outer Ring: BHI 82% (circumference = 2 * PI * 68 = 427.25) */}
                <circle
                  cx="80"
                  cy="80"
                  r="68"
                  stroke="#10B981"
                  strokeWidth="10"
                  fill="none"
                  strokeDasharray="427.25"
                  strokeDashoffset={427.25 * (1 - 0.82)}
                  strokeLinecap="round"
                  className="transition-all duration-1000 ease-out"
                />

                {/* Inner Ring: Stability / Pressure 68% (circumference = 2 * PI * 50 = 314.15) */}
                <circle
                  cx="80"
                  cy="80"
                  r="50"
                  stroke="#38BDF8"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray="314.15"
                  strokeDashoffset={314.15 * (1 - 0.68)}
                  strokeLinecap="round"
                  className="transition-all duration-1000 ease-out"
                />
              </svg>

              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <span className="text-3xl font-panchang font-black text-emerald-400 leading-none">
                  82<span className="text-sm font-sans font-normal text-text-muted">%</span>
                </span>
                <span className="text-[10px] font-mono tracking-widest text-text-faint uppercase mt-1">
                  INDEX SCORE
                </span>
              </div>
            </div>

            {/* Progress breakdown */}
            <div className="flex-1 space-y-2.5 w-full font-mono text-xs">
              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-text-muted">Simpson Diversity</span>
                  <span className="text-emerald-400 font-semibold">85%</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: "85%" }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-text-muted">Canopy Density</span>
                  <span className="text-emerald-400 font-semibold">72%</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: "72%" }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-text-muted">Environmental Stability</span>
                  <span className="text-emerald-400 font-semibold">88%</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: "88%" }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-text-muted">Human Pressure (Inverse)</span>
                  <span className="text-amber-400 font-semibold">42%</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-amber-500 rounded-full" style={{ width: "42%" }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[11px]">
                  <span className="text-text-muted">Population Trend</span>
                  <span className="text-emerald-400 font-semibold">78%</span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: "78%" }} />
                </div>
              </div>
            </div>
          </div>
        </GlassCard>

        {/* Ecosystem Risk Engine Card */}
        <GlassCard className="space-y-4">
          <div className="flex items-center justify-between border-b border-border-subtle pb-2">
            <div className="flex items-center gap-2">
              <Activity size={16} className="text-amber-400" />
              <h2 className="text-sm font-panchang font-bold uppercase tracking-wider text-text-primary">
                Ecosystem Risk Engine & SHAP
              </h2>
            </div>
            <div className="flex items-center gap-2 font-mono">
              <span className="text-sm font-bold text-amber-400">63 / 100</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                MODERATE RISK
              </span>
            </div>
          </div>

          <div className="space-y-3">
            <p className="text-xs text-text-muted leading-relaxed">
              Real-time feature attributions for risk elevation calculated using TreeSHAP on current 72h bioacoustic and microclimate readings:
            </p>

            {/* SHAP Bars */}
            <div className="space-y-2 font-mono text-xs">
              <div className="flex items-center gap-2">
                <span className="w-36 text-text-secondary text-[11px] truncate">Biophony Drop</span>
                <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-emerald-400 rounded" style={{ width: "62%" }} />
                </div>
                <span className="w-12 text-right font-bold text-emerald-400">+0.31</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="w-36 text-text-secondary text-[11px] truncate">Human Pressure</span>
                <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-teal-400 rounded" style={{ width: "48%" }} />
                </div>
                <span className="w-12 text-right font-bold text-teal-300">+0.24</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="w-36 text-text-secondary text-[11px] truncate">Predator Variance</span>
                <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-sky-400 rounded" style={{ width: "38%" }} />
                </div>
                <span className="w-12 text-right font-bold text-sky-300">+0.19</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="w-36 text-text-secondary text-[11px] truncate">Temp Shift</span>
                <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                  <div className="h-full bg-amber-400 rounded" style={{ width: "24%" }} />
                </div>
                <span className="w-12 text-right font-bold text-amber-300">+0.12</span>
              </div>
            </div>

            {/* Expandable AI rationale */}
            <div className="pt-2 border-t border-border-subtle">
              <button
                onClick={() => setAiRationaleExpanded(!aiRationaleExpanded)}
                className="flex items-center justify-between w-full text-xs font-semibold text-text-secondary hover:text-emerald-400 transition-colors"
              >
                <span>AI Risk Rationale & Diagnostics</span>
                {aiRationaleExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
              </button>

              {aiRationaleExpanded && (
                <div className="mt-2 p-2.5 rounded-lg bg-obsidian-950/70 border border-emerald-500/20 text-xs text-slate-300 leading-relaxed space-y-1.5 animate-fade-in font-mono">
                  <p>
                    <strong className="text-emerald-400">Diagnosis:</strong> Sustained 18% biophony drop over 72h indicates localized canopy disturbance in Sector 04.
                  </p>
                  <p>
                    <strong className="text-amber-400">Correlation:</strong> Elevated human acoustic signatures in Grid E-7 correlate directly with predator avoidance behavior in Panthera onca trail telemetry.
                  </p>
                  <p className="text-text-faint text-[10px]">
                    Model Confidence: 87.3% · XGBoost Ensemble v4 · Feature importance updated 3m ago.
                  </p>
                </div>
              )}
            </div>
          </div>
        </GlassCard>
      </div>

      {/* ── 5. Live Sensory Feeds: Dual Optical Traps ── */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Eye size={16} className="text-emerald-400" />
            <h2 className="text-sm font-panchang font-bold uppercase tracking-wider text-text-primary">
              Live Sensory Feeds — Optical Traps
            </h2>
          </div>
          <span className="flex items-center gap-1.5 text-xs text-text-muted font-mono">
            <span className="h-2 w-2 rounded-full bg-red-500 animate-ping" />
            LIVE SYNC 24FPS
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Feed 1: Canopy Alpha */}
          <GlassCard padded={false} className="relative overflow-hidden group">
            <div className="relative h-64 sm:h-72 w-full bg-obsidian-950">
              <img
                src={CANOPY_IMAGE}
                alt="Canopy Sensor Alpha Feed"
                className="w-full h-full object-cover opacity-85 group-hover:opacity-95 transition-opacity"
              />
              
              {/* Camera Overlays */}
              <div className="absolute top-3 left-3 flex items-center gap-2">
                <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-red-600/90 text-white font-mono text-[10px] font-bold tracking-wider">
                  <span className="h-1.5 w-1.5 rounded-full bg-white animate-pulse" />
                  REC // CAM-04A
                </span>
                <span className="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md text-emerald-400 font-mono text-[10px] border border-emerald-500/30">
                  CANOPY PRIME
                </span>
              </div>

              <div className="absolute top-3 right-3 text-right font-mono text-[10px] text-white/80 bg-black/50 px-2 py-0.5 rounded backdrop-blur-sm">
                4K HDR · 60FPS · IR FILTER OFF
              </div>

              {/* Bounding Box: Harpyhaliaetus solitarius */}
              <div className="absolute top-1/4 left-1/3 w-40 h-36 border-2 border-emerald-400 bg-emerald-400/10 rounded-sm pointer-events-none animate-pulse">
                <div className="absolute -top-6 left-0 px-1.5 py-0.5 bg-emerald-500 text-obsidian-950 font-mono text-[10px] font-bold whitespace-nowrap">
                  Harpyhaliaetus solitarius [98.4%]
                </div>
                <Crosshair size={14} className="absolute -bottom-2 -right-2 text-emerald-400" />
              </div>

              {/* Bottom metadata strip */}
              <div className="absolute bottom-0 inset-x-0 p-2.5 bg-gradient-to-t from-black/90 via-black/60 to-transparent flex items-center justify-between text-xs font-mono text-slate-300">
                <span>SECTOR 04-NW · 38m ELEV</span>
                <span className="text-emerald-400 font-semibold">STATUS: TARGET TRACKING</span>
              </div>
            </div>
          </GlassCard>

          {/* Feed 2: Understory Bio-Trap (Jaguar) */}
          <GlassCard padded={false} className="relative overflow-hidden group">
            <div className="relative h-64 sm:h-72 w-full bg-obsidian-950">
              <img
                src={JAGUAR_IMAGE}
                alt="Understory Bio-Trap Feed"
                className="w-full h-full object-cover opacity-85 group-hover:opacity-95 transition-opacity filter contrast-125"
              />

              {/* Camera Overlays */}
              <div className="absolute top-3 left-3 flex items-center gap-2">
                <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-red-600/90 text-white font-mono text-[10px] font-bold tracking-wider">
                  <span className="h-1.5 w-1.5 rounded-full bg-white animate-pulse" />
                  REC // IR-09B
                </span>
                <span className="px-2 py-0.5 rounded bg-black/60 backdrop-blur-md text-amber-400 font-mono text-[10px] border border-amber-500/30">
                  INFRARED TRAP
                </span>
              </div>

              <div className="absolute top-3 right-3 text-right font-mono text-[10px] text-white/80 bg-black/50 px-2 py-0.5 rounded backdrop-blur-sm">
                850nm THERMAL ILLUM · PIR TRIGGER
              </div>

              {/* Bounding Box: Panthera onca */}
              <div className="absolute top-1/5 left-1/4 w-48 h-44 border-2 border-amber-400 bg-amber-400/10 rounded-sm pointer-events-none animate-pulse">
                <div className="absolute -top-6 left-0 px-1.5 py-0.5 bg-amber-500 text-obsidian-950 font-mono text-[10px] font-bold whitespace-nowrap">
                  Panthera onca [87.2%]
                </div>
                <Crosshair size={14} className="absolute -bottom-2 -right-2 text-amber-400" />
              </div>

              {/* Bottom metadata strip */}
              <div className="absolute bottom-0 inset-x-0 p-2.5 bg-gradient-to-t from-black/90 via-black/60 to-transparent flex items-center justify-between text-xs font-mono text-slate-300">
                <span>GRID E-7 CORRIDOR · TRAIL-02</span>
                <span className="text-amber-400 font-semibold">PREDATOR GAIT VERIFIED</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>

      {/* ── 6. Conservation Action Center ── */}
      <GlassCard className="space-y-3 border-emerald-500/30">
        <div className="flex items-center justify-between border-b border-border-subtle pb-2">
          <div className="flex items-center gap-2">
            <Shield size={16} className="text-emerald-400" />
            <h2 className="text-sm font-panchang font-bold uppercase tracking-wider text-text-primary">
              Conservation Action Center
            </h2>
          </div>
          <span className="text-xs font-mono text-text-muted">2 DISPATCH RECOMMENDATIONS</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {/* Priority 01 */}
          <div className="p-3 rounded-xl bg-obsidian-900/90 border border-rose-500/30 space-y-2">
            <div className="flex items-center justify-between">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40">
                PRIORITY 01 // CRITICAL
              </span>
              <span className="text-[11px] font-mono text-text-faint">ZONE 04 GRID E-7</span>
            </div>
            <h3 className="text-xs font-bold text-text-primary font-panchang">
              Deploy Acoustic Deterrent & Ground Recon
            </h3>
            <p className="text-xs text-text-muted leading-relaxed">
              2.4kHz harmonic cluster matches chainsaw signature. Immediate drone sweep recommended to verify perimeter intrusion before canopy breach.
            </p>
            <button
              onClick={() => setPriority1Dispatched(!priority1Dispatched)}
              className={`w-full py-2 rounded-lg text-xs font-bold tracking-wider uppercase transition-all font-mono ${
                priority1Dispatched
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                  : "bg-emerald-500 hover:bg-emerald-400 text-obsidian-950 shadow-glow-emerald"
              }`}
            >
              {priority1Dispatched ? "✓ PATROL SQUAD 02 DISPATCHED" : "DISPATCH PATROL SQUAD 02"}
            </button>
          </div>

          {/* Priority 02 */}
          <div className="p-3 rounded-xl bg-obsidian-900/90 border border-amber-500/30 space-y-2">
            <div className="flex items-center justify-between">
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                PRIORITY 02 // URGENT
              </span>
              <span className="text-[11px] font-mono text-text-faint">ZONE Z-02 TIGER CORRIDOR</span>
            </div>
            <h3 className="text-xs font-bold text-text-primary font-panchang">
              Extend Buffer Zone Around Waterhole Traps
            </h3>
            <p className="text-xs text-text-muted leading-relaxed">
              Thermal sensors detect human foot traffic within 450m of active tiger nursery corridor. Reroute eco-tourist perimeter paths immediately.
            </p>
            <button
              onClick={() => setPriority2PatrolActive(!priority2PatrolActive)}
              className={`w-full py-2 rounded-lg text-xs font-bold tracking-wider uppercase transition-all font-mono ${
                priority2PatrolActive
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : "bg-amber-500 hover:bg-amber-400 text-obsidian-950"
              }`}
            >
              {priority2PatrolActive ? "✓ BUFFER EXTENSION ACTIVE" : "ACTIVATE BUFFER RESTRICTION"}
            </button>
          </div>
        </div>

        <button
          onClick={() => setShowActionPlanModal(true)}
          className="w-full py-2.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-bold tracking-wider uppercase transition-all flex items-center justify-center gap-2 font-mono"
        >
          <Plus size={14} />
          <span>Synthesize Comprehensive Action Plan via TinyLlama</span>
        </button>
      </GlassCard>

      {/* ── MODALS ── */}

      {/* 1. UAV Modal */}
      {showUavModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="w-full max-w-lg p-5 rounded-2xl bg-obsidian-900 border border-sky-500/40 shadow-2xl space-y-4 animate-fade-in">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div className="flex items-center gap-2">
                <Navigation size={18} className="text-sky-400" />
                <h3 className="font-panchang font-bold text-sm text-text-primary uppercase">
                  Autonomous UAV Dispatch
                </h3>
              </div>
              <button
                onClick={() => { setShowUavModal(false); setUavLaunched(false); }}
                className="text-text-muted hover:text-white"
              >
                <X size={18} />
              </button>
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div className="p-3 rounded-lg bg-obsidian-950 border border-border">
                <div className="flex justify-between text-text-muted mb-1">
                  <span>DRONE DESIGNATION:</span>
                  <span className="text-sky-400 font-bold">AERO-GUARD X4</span>
                </div>
                <div className="flex justify-between text-text-muted mb-1">
                  <span>TARGET VECTOR:</span>
                  <span className="text-white">Zone 04 (Chainsaw Anomaly)</span>
                </div>
                <div className="flex justify-between text-text-muted">
                  <span>BATTERY LEVEL:</span>
                  <span className="text-emerald-400 font-bold">94% (48 min aloft)</span>
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-text-muted">CRUISE FLIGHT SPEED</span>
                  <span className="text-sky-400 font-bold">{flightSpeed} m/s ({Math.round(flightSpeed * 3.6)} km/h)</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="60"
                  value={flightSpeed}
                  onChange={(e) => setFlightSpeed(Number(e.target.value))}
                  className="w-full accent-sky-400"
                />
              </div>

              <div className="p-3 rounded-lg border border-dashed border-border-subtle text-center text-text-faint">
                Waypoints: WP-01 (Canopy Tower) → WP-02 (Sector E-7) → WP-03 (Return)
              </div>

              {uavLaunched && (
                <div className="p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 flex items-center gap-2">
                  <CheckCircle size={16} />
                  <span>LAUNCH CONFIRMED. UAV EN ROUTE. ETA 4.2 MIN.</span>
                </div>
              )}
            </div>

            <button
              onClick={() => setUavLaunched(true)}
              className="w-full py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-obsidian-950 font-bold text-xs tracking-wider uppercase font-mono transition-all"
            >
              Confirm Launch Sequence
            </button>
          </div>
        </div>
      )}

      {/* 2. Climate Stress Simulator Modal */}
      {showClimateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="w-full max-w-lg p-5 rounded-2xl bg-obsidian-900 border border-rose-500/40 shadow-2xl space-y-4 animate-fade-in">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div className="flex items-center gap-2">
                <Zap size={18} className="text-rose-400" />
                <h3 className="font-panchang font-bold text-sm text-text-primary uppercase">
                  Climate Stress Simulator
                </h3>
              </div>
              <button onClick={() => setShowClimateModal(false)} className="text-text-muted hover:text-white">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-4 font-mono text-xs">
              <div className="space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-text-muted">TEMPERATURE ANOMALY</span>
                  <span className="text-rose-400 font-bold">+{tempAnomaly.toFixed(1)}°C</span>
                </div>
                <input
                  type="range"
                  min="0.5"
                  max="6.0"
                  step="0.1"
                  value={tempAnomaly}
                  onChange={(e) => setTempAnomaly(Number(e.target.value))}
                  className="w-full accent-rose-400"
                />
              </div>

              <div className="space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-text-muted">HUMIDITY DEFICIT</span>
                  <span className="text-amber-400 font-bold">-{humidityDeficit}%</span>
                </div>
                <input
                  type="range"
                  min="5"
                  max="70"
                  value={humidityDeficit}
                  onChange={(e) => setHumidityDeficit(Number(e.target.value))}
                  className="w-full accent-amber-400"
                />
              </div>

              {/* Monte Carlo Results */}
              <div className="p-3 rounded-lg bg-obsidian-950 border border-border space-y-2">
                <span className="text-text-faint text-[10px] uppercase font-bold tracking-wider block">
                  MONTE CARLO PROJECTION (1,000 RUNS)
                </span>
                <div className="flex justify-between">
                  <span className="text-text-muted">Species Loss Probability:</span>
                  <span className="text-rose-400 font-bold">{Math.round(tempAnomaly * 7.5 + humidityDeficit * 0.3)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Canopy Regression:</span>
                  <span className="text-amber-400 font-bold">{Math.round(humidityDeficit * 0.85)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-text-muted">Estimated Recovery Window:</span>
                  <span className="text-sky-400 font-bold">{Math.round(tempAnomaly * 4 + 8)} months</span>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowClimateModal(false)}
              className="w-full py-2.5 rounded-xl bg-rose-500 hover:bg-rose-400 text-obsidian-950 font-bold text-xs tracking-wider uppercase font-mono transition-all"
            >
              Close Simulator
            </button>
          </div>
        </div>
      )}

      {/* 3. Export PDF Modal */}
      {showExportModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="w-full max-w-lg p-5 rounded-2xl bg-obsidian-900 border border-amber-500/40 shadow-2xl space-y-4 animate-fade-in">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div className="flex items-center gap-2">
                <FileText size={18} className="text-amber-400" />
                <h3 className="font-panchang font-bold text-sm text-text-primary uppercase">
                  Export PDF Telemetry Briefing
                </h3>
              </div>
              <button onClick={() => setShowExportModal(false)} className="text-text-muted hover:text-white">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-3 font-mono text-xs text-text-secondary">
              <p>Select briefing sections to compile into tactical ecological report:</p>
              <div className="space-y-2 p-3 rounded-lg bg-obsidian-950 border border-border">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" defaultChecked className="accent-emerald-400" />
                  <span>Full Biodiversity Health Index (BHI) Breakdown</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" defaultChecked className="accent-emerald-400" />
                  <span>Ecosystem Risk SHAP Feature Attributions</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" defaultChecked className="accent-emerald-400" />
                  <span>Zone 04 Acoustic Threat Vector Waveform</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" defaultChecked className="accent-emerald-400" />
                  <span>Optical Camera Trap Infrared Imagery Logs</span>
                </label>
              </div>

              <div className="text-[10px] text-text-faint p-2 rounded bg-obsidian-950/50">
                SHA-256 SIGNATURE: a7f8c92b...e431 (Tamper-evident conservation registry)
              </div>
            </div>

            <button
              onClick={() => {
                alert("Briefing PDF downloaded with SHA-256 validation.");
                setShowExportModal(false);
              }}
              className="w-full py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-obsidian-950 font-bold text-xs tracking-wider uppercase font-mono transition-all flex items-center justify-center gap-2"
            >
              <Download size={14} />
              Generate & Download PDF
            </button>
          </div>
        </div>
      )}

      {/* 4. Action Plan Dispatcher Modal */}
      {showActionPlanModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="w-full max-w-lg p-5 rounded-2xl bg-obsidian-900 border border-emerald-500/40 shadow-2xl space-y-4 animate-fade-in">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div className="flex items-center gap-2">
                <Shield size={18} className="text-emerald-400" />
                <h3 className="font-panchang font-bold text-sm text-text-primary uppercase">
                  Conservation Action Plan
                </h3>
              </div>
              <button onClick={() => setShowActionPlanModal(false)} className="text-text-muted hover:text-white">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-3 font-mono text-xs text-slate-300">
              <div className="p-3 rounded-lg bg-obsidian-950 border border-emerald-500/30 space-y-2">
                <div className="text-emerald-400 font-bold uppercase tracking-wider text-[11px]">
                  STRATEGY SUMMARY // SECTOR-04
                </div>
                <p className="leading-relaxed">
                  1. Deploy UAV unit Aero-Guard X4 on continuous thermal perimeter at Grid E-7.
                </p>
                <p className="leading-relaxed">
                  2. Mobilize Ranger Squad 02 with directional acoustic hydrophones and trail cameras.
                </p>
                <p className="leading-relaxed">
                  3. Log telemetry to regional IUCN automated sentinel ledger.
                </p>
              </div>
            </div>

            <button
              onClick={() => {
                alert("Action plan committed to field ledger.");
                setShowActionPlanModal(false);
              }}
              className="w-full py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-obsidian-950 font-bold text-xs tracking-wider uppercase font-mono transition-all"
            >
              Execute Action Plan
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
