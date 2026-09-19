import { useState, useEffect } from "react";
import {
  Brain,
  Activity,
  Leaf,
  TrendingDown,
  TrendingUp,
  Mic,
  AlertTriangle,
  Shield,
  Navigation,
  Sparkles,
  RefreshCw,
  CheckCircle,
  ChevronRight,
  Zap,
} from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";

const JAGUAR_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuBLzADIm0FTKdvvGKvL1L-PWqiiK1OOnEKtvad8UBoe90PM-Zvvu1ei6uxIhQSi8Pq9k4LSSKAl1bmBZVQZ16OzrPKQdbm9haKt7j8dwaFx9oVii3TdWkcWMlOWoW1SezhEQCU3olvhbaCh1rVIpJrTaSeuttIila4iR82Zi1aJ2ERD3FMBxPbGhK_W2w_u8cSgymxbtfBQ6QrP27PwvXYP3TgY-HEGQmDobIiprEU_y1ZEUY-U0yhxnw";

export default function ConservationAIPage() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [strategyIndex, setStrategyIndex] = useState(0);

  const STRATEGIES = [
    {
      title: "TACTICAL PATROL RECOMMENDATION — SQUAD 02",
      squad: "Squad 02 (Delta Unit)",
      route: "Alpha-3 Ridge Path",
      eta: "18 minutes",
      coords: "-3.4821°S, -62.1847°W (Grid E-7)",
      assessment:
        "Acoustic anomaly in Zone 04 consistent with illegal chainsaw activity. IR camera trap (CAM-09B) confirms vehicle intrusion at 14:32 UTC. Threat confidence: 87.3%. Recommend immediate interception sweep.",
      steps: [
        {
          num: "01",
          name: "Acoustic Triangulation",
          detail: "Deploy parabolic directional microphones across M10-M12 coordinates to isolate chainsaw motor RPM.",
        },
        {
          num: "02",
          name: "Physical Ground Intercept",
          detail: "Advance Squad 02 along Ridge Cut to secure vehicle egress trail at Bamboo Bridge.",
        },
        {
          num: "03",
          name: "Evidence Preservation",
          detail: "Log telemetry and thermal keyframes directly to immutable blockchain conservation ledger.",
        },
      ],
    },
    {
      title: "AIR-SURVEILLANCE & RECON PROTOCOL — UAV ECHO-1",
      squad: "Drone Wing Alpha",
      route: "Direct Canopy Overflight",
      eta: "4 minutes",
      coords: "-3.4790°S, -62.1812°W (Sector 04 Perimeter)",
      assessment:
        "High-altitude FLIR thermal sweep detects 3 heat signatures adjacent to logging track. Automatic geofencing alert broadcasted to regional forest ranger command.",
      steps: [
        {
          num: "01",
          name: "Thermal Overhead Sweep",
          detail: "Maintain 120m altitude with 4K FLIR camera; illuminate target coordinates with IR strobe.",
        },
        {
          num: "02",
          name: "Auditory Deterrent Broadcast",
          detail: "Activate 130dB automated wildlife-safe acoustic deterrent tone to halt illegal clearing.",
        },
        {
          num: "03",
          name: "Ranger Rendezvous",
          detail: "Provide continuous live telemetry feed to approaching ground intercept vehicles.",
        },
      ],
    },
  ];

  const handleSynthesizeStrategy = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setStrategyIndex((prev) => (prev === 0 ? 1 : 0));
      setIsGenerating(false);
    }, 1800);
  };

  const currentStrategy = STRATEGIES[strategyIndex];

  return (
    <div className="space-y-4 pb-12">
      {/* ── 1. Page Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 rounded-xl bg-obsidian-850/80 border border-emerald-500/20 backdrop-blur-md">
        <div>
          <h1 className="text-base sm:text-lg font-panchang font-bold text-gradient-eco uppercase tracking-wider">
            Analytics & Conservation AI
          </h1>
          <p className="text-xs font-mono text-text-muted">
            Multi-Metric Biodiversity Intelligence & Predictive Decision Support
          </p>
        </div>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="px-2 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-bold">
            TINYLAMA LOCAL INFERENCE • OFFLINE READY
          </span>
        </div>
      </div>

      {/* ── 2. Micro-Metrics Strip (4 Inline KPI Tiles) ── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 font-mono">
        <GlassCard className="space-y-1 border-t-2 border-t-sky-400">
          <span className="text-[10px] text-text-faint uppercase font-bold tracking-wider block">
            Shannon Diversity (H')
          </span>
          <div className="text-2xl font-panchang font-bold text-sky-400">3.42</div>
          <span className="text-[10px] text-text-muted">Target Ref: 3.80 | High Diversity</span>
        </GlassCard>

        <GlassCard className="space-y-1 border-t-2 border-t-emerald-400">
          <span className="text-[10px] text-text-faint uppercase font-bold tracking-wider block">
            Simpson Index (1-D)
          </span>
          <div className="text-2xl font-panchang font-bold text-emerald-400">0.89</div>
          <span className="text-[10px] text-text-muted">High species evenness probability</span>
        </GlassCard>

        <GlassCard className="space-y-1 border-t-2 border-t-emerald-400">
          <span className="text-[10px] text-text-faint uppercase font-bold tracking-wider block">
            Pielou Evenness (J')
          </span>
          <div className="text-2xl font-panchang font-bold text-emerald-400">0.78</div>
          <span className="text-[10px] text-text-muted">Equitable distribution across taxa</span>
        </GlassCard>

        <GlassCard className="space-y-1 border-t-2 border-t-amber-400">
          <span className="text-[10px] text-text-faint uppercase font-bold tracking-wider block">
            Bio Health Deficit
          </span>
          <div className="text-2xl font-panchang font-bold text-amber-400">-8.4% <span className="text-xs font-normal">/ 90D</span></div>
          <span className="text-[10px] text-rose-400">Deviation from 10Y historical average</span>
        </GlassCard>
      </div>

      {/* ── 3. Biodiversity Health Trajectory Chart vs 10Y Baseline ── */}
      <GlassCard className="space-y-3 border-emerald-500/30">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border-subtle pb-2">
          <div>
            <h2 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
              Biodiversity Health Trajectory vs. 10Y Baseline
            </h2>
            <p className="text-[11px] font-mono text-text-faint">
              90-day observed trajectory compared to historical decadal mean (2014-2024)
            </p>
          </div>
          {/* Legend */}
          <div className="flex items-center gap-4 text-xs font-mono">
            <div className="flex items-center gap-1.5">
              <span className="w-4 h-0.5 border-t-2 border-dashed border-sky-400" />
              <span className="text-text-muted">10Y Baseline Mean (88-92)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-4 h-1 bg-emerald-400 rounded-full" />
              <span className="text-emerald-400 font-bold">Observed 90D Trend</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 bg-rose-500/25 border border-rose-500/40 rounded-sm" />
              <span className="text-rose-400 font-bold">Deficit Zone</span>
            </div>
          </div>
        </div>

        {/* Pure SVG Curve Chart */}
        <div className="relative w-full h-64 sm:h-72 bg-obsidian-950/70 rounded-xl overflow-hidden p-2">
          <svg className="w-full h-full" viewBox="0 0 900 280">
            <defs>
              <linearGradient id="deficitFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#EF4444" stopOpacity="0.35" />
                <stop offset="100%" stopColor="#EF4444" stopOpacity="0.05" />
              </linearGradient>
            </defs>

            {/* Subtle horizontal grid lines */}
            <g stroke="#1e293b" strokeWidth="1" strokeDasharray="4 4">
              <line x1="60" y1="40" x2="860" y2="40" />
              <line x1="60" y1="90" x2="860" y2="90" />
              <line x1="60" y1="140" x2="860" y2="140" />
              <line x1="60" y1="190" x2="860" y2="190" />
              <line x1="60" y1="240" x2="860" y2="240" />
            </g>

            {/* Y Axis Labels */}
            <g fill="#64748b" fontSize="10" fontFamily="monospace" textAnchor="end">
              <text x="50" y="44">100</text>
              <text x="50" y="94">90</text>
              <text x="50" y="144">80</text>
              <text x="50" y="194">70</text>
              <text x="50" y="244">60</text>
            </g>

            {/* X Axis Months */}
            <g fill="#94a3b8" fontSize="10" fontFamily="monospace" textAnchor="middle">
              <text x="100" y="265">JAN</text>
              <text x="190" y="265">FEB</text>
              <text x="280" y="265">MAR</text>
              <text x="370" y="265">APR</text>
              <text x="460" y="265">MAY</text>
              <text x="550" y="265">JUN</text>
              <text x="640" y="265">JUL</text>
              <text x="730" y="265">AUG</text>
              <text x="820" y="265">SEP</text>
            </g>

            {/* Red Deficit Shaded Polygon Area (between baseline and observed curve starting ~May) */}
            <polygon
              points="
                460,90
                550,88
                640,92
                730,86
                820,90
                820,135
                730,128
                640,118
                550,102
                460,90
              "
              fill="url(#deficitFill)"
            />

            {/* 10Y Baseline Curve (Sky Blue Dashed Line around y=88-92) */}
            <path
              d="M 100,92 Q 280,86 460,90 T 640,92 T 820,90"
              fill="none"
              stroke="#38BDF8"
              strokeWidth="2.5"
              strokeDasharray="6 4"
            />

            {/* Observed Trajectory Curve (Emerald Solid Line, declines past June) */}
            <path
              d="M 100,94 C 200,92 320,90 460,90 C 550,102 640,118 730,128 C 780,132 820,135 820,135"
              fill="none"
              stroke="#10B981"
              strokeWidth="3.5"
            />

            {/* Deficit Annotation Callout Arrow */}
            <g>
              <circle cx="730" cy="107" r="4" fill="#EF4444" className="animate-ping" />
              <line x1="730" y1="107" x2="700" y2="50" stroke="#EF4444" strokeWidth="1.5" />
              <rect x="635" y="30" width="130" height="22" rx="4" fill="#0B1120" stroke="#EF4444" strokeWidth="1" />
              <text x="700" y="45" fill="#EF4444" fontSize="10" fontFamily="monospace" fontWeight="bold" textAnchor="middle">
                DEFICIT -8.4%
              </text>
            </g>
          </svg>
        </div>
      </GlassCard>

      {/* ── 4. Zone 04 Acoustic Array Panel (14 Mic Array) ── */}
      <GlassCard className="space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border-subtle pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Mic size={16} className="text-emerald-400" />
              <h2 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
                Zone 04 // Acoustic Array — Signal Matrix
              </h2>
            </div>
            <p className="text-[11px] font-mono text-text-faint">
              14-channel microphone array • Real-time FFT processing
            </p>
          </div>
          <div className="flex items-center gap-3 font-mono text-xs">
            <span className="text-emerald-400 font-bold">Active: 11/14</span>
            <span className="text-amber-400 font-bold">Suppressed: 3/14</span>
            <span className="text-text-muted">Coverage: 78.6%</span>
          </div>
        </div>

        {/* 14 Microphone status tiles */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 font-mono text-xs">
          {Array.from({ length: 14 }).map((_, idx) => {
            const nodeNum = idx + 1;
            const nodeId = `M${nodeNum < 10 ? "0" + nodeNum : nodeNum}`;
            const isSuppressed = nodeNum >= 10 && nodeNum <= 12;

            return (
              <div
                key={nodeId}
                className={`p-2.5 rounded-xl border flex flex-col justify-between h-28 ${
                  isSuppressed
                    ? "bg-amber-500/10 border-amber-500/40 text-amber-300"
                    : "bg-obsidian-900 border-border text-slate-300"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sm text-text-primary">{nodeId}</span>
                  <span
                    className={`h-2 w-2 rounded-full ${
                      isSuppressed ? "bg-amber-400 animate-pulse" : "bg-emerald-400"
                    }`}
                  />
                </div>

                <div className="space-y-1">
                  <span className="text-[10px] text-text-faint block">
                    {isSuppressed ? "NOISE FLOOR SUPPRESSED" : "SIGNAL: NOMINAL"}
                  </span>
                  {/* Signal bars */}
                  <div className="flex items-end gap-0.5 h-4">
                    {Array.from({ length: 5 }).map((_, bIdx) => (
                      <div
                        key={bIdx}
                        className={`w-1 rounded-sm ${
                          isSuppressed
                            ? bIdx < 2 ? "bg-amber-400 h-2" : "bg-obsidian-700 h-1"
                            : "bg-emerald-400"
                        }`}
                        style={{ height: isSuppressed ? undefined : `${(bIdx + 1) * 3}px` }}
                      />
                    ))}
                  </div>
                </div>

                <div className="flex justify-between text-[9px] text-text-faint">
                  <span>{isSuppressed ? "0.8-2.4kHz" : "0-16kHz"}</span>
                  <span>14:34:10</span>
                </div>
              </div>
            );
          })}
        </div>
      </GlassCard>

      {/* ── 5. Ecosystem Risk Engine & SHAP (2 Cols) ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Left: Risk Score */}
        <GlassCard className="space-y-3 font-mono">
          <div className="flex items-center justify-between border-b border-border-subtle pb-2">
            <div className="flex items-center gap-2">
              <Activity size={16} className="text-amber-400" />
              <h3 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
                Ecosystem Risk Engine
              </h3>
            </div>
            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">
              MODERATE RISK TIER
            </span>
          </div>

          <div className="flex items-center gap-4">
            <div className="p-4 rounded-xl bg-obsidian-950 border border-amber-500/30 text-center shrink-0">
              <span className="text-3xl font-panchang font-bold text-amber-400 block">63</span>
              <span className="text-[10px] text-text-faint uppercase">OUT OF 100</span>
            </div>

            <p className="text-xs text-text-muted leading-relaxed">
              XGBoost ensemble model integrates biophony spectral entropy, thermal deficit vectors, and acoustic chainsaw detection rates across Zone 04.
            </p>
          </div>
        </GlassCard>

        {/* Right: SHAP Attributions */}
        <GlassCard className="space-y-3 font-mono">
          <div className="flex items-center justify-between border-b border-border-subtle pb-2">
            <h3 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
              SHAP Feature Attributions
            </h3>
            <span className="text-[10px] text-text-faint">TreeSHAP Explainer</span>
          </div>

          <div className="space-y-2 text-xs">
            {/* Positive Bars (Risk Elevators - Teal) */}
            <div className="flex items-center gap-2">
              <span className="w-36 text-text-secondary text-[11px] truncate">Biophony Drop</span>
              <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                <div className="h-full bg-teal-400 rounded" style={{ width: "62%" }} />
              </div>
              <span className="w-12 text-right font-bold text-teal-300">+0.31</span>
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
                <div className="h-full bg-teal-400 rounded" style={{ width: "38%" }} />
              </div>
              <span className="w-12 text-right font-bold text-teal-300">+0.19</span>
            </div>

            <div className="flex items-center gap-2">
              <span className="w-36 text-text-secondary text-[11px] truncate">Temp Shift</span>
              <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                <div className="h-full bg-teal-400 rounded" style={{ width: "24%" }} />
              </div>
              <span className="w-12 text-right font-bold text-teal-300">+0.12</span>
            </div>

            {/* Negative Bars (Protective Factors - Blue) */}
            <div className="flex items-center gap-2">
              <span className="w-36 text-text-secondary text-[11px] truncate">Canopy Integrity</span>
              <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                <div className="h-full bg-sky-400 rounded" style={{ width: "16%" }} />
              </div>
              <span className="w-12 text-right font-bold text-sky-300">-0.08</span>
            </div>

            <div className="flex items-center gap-2">
              <span className="w-36 text-text-secondary text-[11px] truncate">Seasonal Correction</span>
              <div className="flex-1 h-3 rounded bg-obsidian-700 overflow-hidden">
                <div className="h-full bg-sky-400 rounded" style={{ width: "28%" }} />
              </div>
              <span className="w-12 text-right font-bold text-sky-300">-0.14</span>
            </div>
          </div>
        </GlassCard>
      </div>

      {/* ── 6. Conservation AI Decision Assistant ── */}
      <GlassCard className="space-y-4 border-emerald-500/40">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border-subtle pb-2">
          <div className="flex items-center gap-2">
            <Brain size={18} className="text-emerald-400" />
            <div>
              <h2 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
                Conservation AI Decision Assistant
              </h2>
              <span className="text-[10px] font-mono text-text-faint">
                TinyLlama • Local Edge Inference • Offline Protocol Active
              </span>
            </div>
          </div>
          <button
            onClick={handleSynthesizeStrategy}
            disabled={isGenerating}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-obsidian-950 font-bold text-xs font-mono uppercase tracking-wider transition-all shadow-glow-emerald disabled:opacity-50"
          >
            {isGenerating ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
            <span>{isGenerating ? "Synthesizing Strategy..." : "Synthesize New Strategy"}</span>
          </button>
        </div>

        {/* Content Box */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 font-mono text-xs">
          {/* Situation Assessment (7 cols) */}
          <div className="lg:col-span-7 space-y-3">
            <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 space-y-1.5">
              <span className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider block">
                SITUATION ASSESSMENT & MODEL REASONING
              </span>
              <p className="text-slate-200 leading-relaxed">
                {currentStrategy.assessment}
              </p>
            </div>

            {/* Tactical Steps */}
            <div className="space-y-2">
              <span className="text-[10px] text-text-faint uppercase font-bold tracking-wider block">
                RECOMMENDED EXECUTION STEPS:
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                {currentStrategy.steps.map((step) => (
                  <div key={step.num} className="p-2.5 rounded-lg bg-obsidian-900 border border-border space-y-1">
                    <span className="text-emerald-400 font-bold text-[11px] block">{step.num} // {step.name}</span>
                    <p className="text-[10px] text-text-muted leading-relaxed">{step.detail}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Infrared Intrusion Photo & Telemetry (5 cols) */}
          <div className="lg:col-span-5 space-y-2">
            <div className="relative h-48 rounded-xl overflow-hidden bg-obsidian-950 border border-rose-500/40">
              <img
                src={JAGUAR_IMAGE}
                alt="Infrared Vehicle Intrusion"
                className="w-full h-full object-cover filter contrast-125"
              />
              <div className="absolute top-2 left-2 px-2 py-0.5 rounded bg-rose-600/90 text-white font-bold text-[9px] tracking-wider uppercase flex items-center gap-1">
                <AlertTriangle size={11} />
                INTRUSION DETECTED // 14:32 UTC
              </div>
              <div className="absolute bottom-2 inset-x-2 p-2 rounded bg-black/85 backdrop-blur-sm text-[10px] text-slate-300 flex justify-between">
                <span>SECTOR 04 GRID E-7</span>
                <span className="text-rose-400 font-bold">CHAINSIGNAL: MATCH</span>
              </div>
            </div>

            {/* Tactical Deployment Meta */}
            <div className="p-2.5 rounded-lg bg-obsidian-950 border border-border-subtle text-[11px] space-y-1 text-slate-300">
              <div className="flex justify-between">
                <span className="text-text-muted">Target Squadron:</span>
                <span className="text-emerald-400 font-bold">{currentStrategy.squad}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-muted">Transit Route:</span>
                <span>{currentStrategy.route}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-muted">Estimated Intercept:</span>
                <span className="text-amber-400 font-bold">{currentStrategy.eta}</span>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
}
