import { useState } from "react";
import {
  Map as MapIcon,
  Filter,
  Layers,
  AlertTriangle,
  Navigation,
  Radio,
  Wifi,
  ChevronDown,
  Crosshair,
  Compass,
  Plus,
  Minus,
  Eye,
  Shield,
  Clock,
  Activity,
  Zap,
} from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";

const TIGER_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuB3IzFFdbJfoM2w5JeSHMcwyMDll-9Nxx3rIQDs6T2pVi0qN1UtY48LJ5v1c3jXIlqvOkTtwO0N7a6feEJ8F2MI6KLX6dlNfriFkHZaneBIPpA9bwG2Y07Fz1LAqNehTpyi_ylwfwpAbhJSm3071LQRDF07mhq1gaXfKFnHkIOmh0oQ5zYqfBzpxQ6RDGWm4D9XNbl47UMnr_Qosq-2bjZ5SQVRFisPJNnFZenzU3uyByitCpt9M_lkzA";
const PEAFOWL_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuBNlWD1q90O26W_NFakub53EOli5QV96PKiPUrtYWNnlvL-AHlvKhRQn8Mwea_DtA4x_dIf7cht5ddZGC4b3xPgtqztVYj8sxltU9PGLY1GX2AutCTUhkcJF0EFIRtLeUk-dPXVFy_cZAez7S8ib0sslIGeGxmkr_Z-ky18XDG3dbtnwX7KJ-BC67pLydFAEYyMe2WM-fHTrjiGVkxTztxAFbh7gVcc_N92wgYY3E2KmT8e40Gj3CA09Q";
const ELEPHANT_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuDsbMRE2-9tmkGSymqcpVRCAN-kfcszBCpICqNcFD1WUjm0wnghb8ase-AAJzKEXOBDJ58X-SpkdeGoM3CYo0LnTyYK6nt9E811lLAenyPbt5cV7gjT9e7_ZYhXzlUvkWApVeCYBbs8pIOAiogoZMMSD542DgDfdQU2w5gDqodfBRALB2IMrHSPfCx2n-Sq7KEQxrnEhSCw9u3yxacbH-sHyJnhMGcI4rNToiLXJpGrN_wdplaW1duLqw";
const HORNBILL_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuCsVpCuyc5OK9xpFe46rrxXniRiRTg0bOgKFvw9wA2cSo5jfWh_736Xm44to5LtCBtZ7Rx_FRY_31tuywn3XH8WMrtvzIWcFOXKMfyd4WxXlVoMuZfVOrvJz8fIL_u93oNlPtyZ8Efk5ZDgnajifl9M1Nr40EW9THkQ6rLTGsb95VM9nFbx91x8DmUDOh7A5KYtbX5wX2PaV5mpKlYNCdH63b27NZ3d4mAPXoLDZXjNn3N5RgC2MXVuDw";

interface MapNode {
  id: string;
  name: string;
  species: string;
  category: "Mammalia" | "Aves" | "Amphibia";
  x: number; // SVG coordinates 0-1000
  y: number; // SVG coordinates 0-600
  status: "CRITICAL" | "MODERATE" | "LOW";
  color: string;
  description: string;
  time: string;
  freq?: string;
}

const MAP_NODES: MapNode[] = [
  {
    id: "zone-04",
    name: "Zone 04 Threat Vector",
    species: "Chainsaw / Vehicle Anomaly",
    category: "Mammalia",
    x: 520,
    y: 280,
    status: "CRITICAL",
    color: "#EF4444",
    description: "2.4kHz acoustic chainsaw cluster. Cross-referenced with IR vehicle intrusion at Grid E-7.",
    time: "14:32 UTC",
    freq: "2.4kHz Pulse",
  },
  {
    id: "node-z02",
    name: "Node Z-02 (Tiger Territory)",
    species: "Panthera tigris (Bengal Tiger)",
    category: "Mammalia",
    x: 290,
    y: 190,
    status: "CRITICAL",
    color: "#10B981",
    description: "Adult male tiger scent marking along Northern Ridge transect.",
    time: "14:34 UTC",
  },
  {
    id: "node-z07",
    name: "Node Z-07 (Peafowl Sanctuary)",
    species: "Pavo cristatus (Indian Peafowl)",
    category: "Aves",
    x: 760,
    y: 170,
    status: "LOW",
    color: "#38BDF8",
    description: "Courtship call cluster logged across 4 acoustic hydrophones.",
    time: "14:31 UTC",
  },
  {
    id: "node-z01",
    name: "Node Z-01 (Elephant Corridor)",
    species: "Elephas maximus (Asian Elephant)",
    category: "Mammalia",
    x: 340,
    y: 440,
    status: "MODERATE",
    color: "#A855F7",
    description: "Herd of 6 traversing bamboo crossing heading south toward river basin.",
    time: "14:28 UTC",
  },
  {
    id: "node-z09",
    name: "Node Z-09 (Canopy Hornbill)",
    species: "Buceros bicornis (Great Pied Hornbill)",
    category: "Aves",
    x: 680,
    y: 390,
    status: "LOW",
    color: "#34D399",
    description: "Nesting pair active in emergent dipterocarp crown.",
    time: "14:25 UTC",
  },
];

export default function BiodiversityMapPage() {
  const [selectedTaxa, setSelectedTaxa] = useState<string>("All");
  const [riskFilter, setRiskFilter] = useState<string>("All");
  const [activeLayers, setActiveLayers] = useState({
    canopyRadar: true,
    acousticArray: true,
    irTraps: true,
    humanFootprint: true,
  });

  const [selectedNode, setSelectedNode] = useState<MapNode>(MAP_NODES[0]);
  const [zoomLevel, setZoomLevel] = useState<number>(1);

  const toggleLayer = (key: keyof typeof activeLayers) => {
    setActiveLayers((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const filteredNodes = MAP_NODES.filter((node) => {
    if (selectedTaxa !== "All" && node.category !== selectedTaxa) return false;
    if (riskFilter === "Critical Only" && node.status !== "CRITICAL") return false;
    if (riskFilter === "Moderate+" && node.status === "LOW") return false;
    return true;
  });

  return (
    <div className="space-y-4 pb-12">
      {/* ── 1. Tactical Filter Bar ── */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3 p-3 rounded-xl bg-obsidian-850/80 border border-emerald-500/20 backdrop-blur-md">
        {/* Taxa tabs */}
        <div className="flex items-center gap-1 bg-obsidian-950/60 p-1 rounded-lg border border-border-subtle">
          {["All", "Mammalia", "Aves", "Amphibia"].map((taxa) => (
            <button
              key={taxa}
              onClick={() => setSelectedTaxa(taxa)}
              className={`px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-md transition-all font-mono ${
                selectedTaxa === taxa
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-glow-sm"
                  : "text-text-muted hover:text-text-primary hover:bg-white/5"
              }`}
            >
              {taxa}
            </button>
          ))}
        </div>

        {/* Dropdowns & Layer Toggles */}
        <div className="flex items-center gap-2 flex-wrap text-xs font-mono">
          {/* Risk Filter */}
          <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-obsidian-900 border border-border text-text-secondary">
            <Filter size={12} className="text-emerald-400" />
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="bg-transparent text-text-primary focus:outline-none cursor-pointer"
            >
              <option value="All" className="bg-obsidian-900">Risk: All Tiers</option>
              <option value="Critical Only" className="bg-obsidian-900">Risk: Critical Only</option>
              <option value="Moderate+" className="bg-obsidian-900">Risk: Moderate+</option>
            </select>
          </div>

          {/* Layer toggles */}
          <div className="flex items-center gap-1 bg-obsidian-950/60 p-1 rounded-lg border border-border-subtle">
            <button
              onClick={() => toggleLayer("canopyRadar")}
              className={`px-2 py-1 rounded text-[11px] font-semibold transition-all ${
                activeLayers.canopyRadar
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                  : "text-text-faint hover:text-text-muted"
              }`}
            >
              Radar
            </button>
            <button
              onClick={() => toggleLayer("acousticArray")}
              className={`px-2 py-1 rounded text-[11px] font-semibold transition-all ${
                activeLayers.acousticArray
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40"
                  : "text-text-faint hover:text-text-muted"
              }`}
            >
              Acoustics
            </button>
            <button
              onClick={() => toggleLayer("irTraps")}
              className={`px-2 py-1 rounded text-[11px] font-semibold transition-all ${
                activeLayers.irTraps
                  ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                  : "text-text-faint hover:text-text-muted"
              }`}
            >
              IR Traps
            </button>
            <button
              onClick={() => toggleLayer("humanFootprint")}
              className={`px-2 py-1 rounded text-[11px] font-semibold transition-all ${
                activeLayers.humanFootprint
                  ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                  : "text-text-faint hover:text-text-muted"
              }`}
            >
              Human Pressure
            </button>
          </div>

          {/* Node sync counter */}
          <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-bold">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
            <span>48 NODES • 100% SYNC</span>
          </div>
        </div>
      </div>

      {/* ── 2. Vector Map + Side Panels (2 Columns) ── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Map Column (8/12 on large screens) */}
        <div className="lg:col-span-8 relative">
          <GlassCard padded={false} className="relative h-[640px] overflow-hidden border-emerald-500/30 bg-[#080d12]">
            {/* SVG Tactical Vector Map */}
            <svg
              className="w-full h-full cursor-crosshair select-none"
              viewBox="0 0 1000 600"
              style={{ transform: `scale(${zoomLevel})`, transformOrigin: "center center", transition: "transform 0.3s ease-out" }}
            >
              <defs>
                {/* Radial Gradient for Radar Sweep */}
                <linearGradient id="radarSweep" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#10B981" stopOpacity="0.3" />
                  <stop offset="50%" stopColor="#10B981" stopOpacity="0.08" />
                  <stop offset="100%" stopColor="#10B981" stopOpacity="0" />
                </linearGradient>

                {/* Tactical Grid Pattern */}
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#152140" strokeWidth="0.8" strokeOpacity="0.6" />
                </pattern>
              </defs>

              {/* Background Grid */}
              <rect width="1000" height="600" fill="url(#grid)" />

              {/* Topographic Isolines (curved elevation contours) */}
              <g stroke="#0e2a22" strokeWidth="1.2" fill="none" opacity="0.65">
                <path d="M 50,300 Q 200,180 400,220 T 750,190 T 950,280" />
                <path d="M 80,350 Q 250,260 450,290 T 780,260 T 980,360" />
                <path d="M 30,220 Q 220,110 420,140 T 720,120 T 920,180" />
                <path d="M 120,420 Q 300,340 520,380 T 820,360 T 960,460" />
                <path d="M 160,500 Q 380,440 600,470 T 880,460 T 980,540" />
              </g>

              {/* Concentric Radar Survey Rings */}
              {activeLayers.canopyRadar && (
                <g stroke="#10B981" strokeOpacity="0.18" fill="none">
                  <circle cx="500" cy="300" r="100" strokeDasharray="4 4" />
                  <circle cx="500" cy="300" r="200" strokeWidth="1" />
                  <circle cx="500" cy="300" r="300" strokeDasharray="8 6" />
                  <circle cx="500" cy="300" r="400" strokeWidth="1" />

                  {/* Crosshairs zero-axis */}
                  <line x1="100" y1="300" x2="900" y2="300" stroke="#10B981" strokeOpacity="0.12" />
                  <line x1="500" y1="50" x2="500" y2="550" stroke="#10B981" strokeOpacity="0.12" />
                </g>
              )}

              {/* Animated 2.4kHz Acoustic Chainsaw Soundwave Pulses at Zone 04 (x=520, y=280) */}
              {activeLayers.acousticArray && (
                <g>
                  {/* Outer pulsing ring */}
                  <circle cx="520" cy="280" r="48" fill="none" stroke="#EF4444" strokeWidth="1.5" opacity="0.6">
                    <animate attributeName="r" values="18;65;18" dur="2.4s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.8;0.1;0.8" dur="2.4s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="520" cy="280" r="32" fill="none" stroke="#F59E0B" strokeWidth="1.2" opacity="0.8">
                    <animate attributeName="r" values="10;45;10" dur="2.4s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="520" cy="280" r="8" fill="#EF4444" className="animate-ping" opacity="0.75" />
                </g>
              )}

              {/* Map Nodes / Pins */}
              {filteredNodes.map((node) => {
                const isSelected = selectedNode.id === node.id;
                return (
                  <g
                    key={node.id}
                    className="cursor-pointer group"
                    onClick={() => setSelectedNode(node)}
                  >
                    {/* Pulsing ring on selected */}
                    {isSelected && (
                      <circle
                        cx={node.x}
                        cy={node.y}
                        r="24"
                        fill="none"
                        stroke={node.color}
                        strokeWidth="2"
                        strokeDasharray="3 3"
                      >
                        <animateTransform
                          attributeName="transform"
                          type="rotate"
                          from={`0 ${node.x} ${node.y}`}
                          to={`360 ${node.x} ${node.y}`}
                          dur="8s"
                          repeatCount="indefinite"
                        />
                      </circle>
                    )}

                    {/* Outer marker pin */}
                    <circle
                      cx={node.x}
                      cy={node.y}
                      r={isSelected ? "11" : "8"}
                      fill="#0B1120"
                      stroke={node.color}
                      strokeWidth="2.5"
                    />

                    {/* Inner core */}
                    <circle cx={node.x} cy={node.y} r={isSelected ? "5" : "3.5"} fill={node.color} />

                    {/* Node Tag Label */}
                    <rect
                      x={node.x + 14}
                      y={node.y - 12}
                      width={node.id === "zone-04" ? "145" : "110"}
                      height="22"
                      rx="4"
                      fill="rgba(11,17,32,0.85)"
                      stroke={isSelected ? node.color : "rgba(51,65,85,0.6)"}
                      strokeWidth="1"
                    />
                    <text
                      x={node.x + 20}
                      y={node.y + 3}
                      fill={isSelected ? "#F8FAFC" : "#94A3B8"}
                      fontSize="10"
                      fontFamily="monospace"
                      fontWeight="bold"
                    >
                      {node.name.split(" ")[0]} // {node.status}
                    </text>
                  </g>
                );
              })}
            </svg>

            {/* HUD Overlays (Top-left coordinates + Scale) */}
            <div className="absolute top-3 left-3 flex flex-col gap-1 p-2 rounded-lg bg-obsidian-950/85 border border-border-subtle font-mono text-[10px] text-text-muted backdrop-blur-sm pointer-events-none">
              <span className="text-emerald-400 font-bold flex items-center gap-1">
                <Crosshair size={12} />
                TAC-RADAR // SEC-04 GRID
              </span>
              <span>COORDS: -03.4653°N, -62.2159°W</span>
              <span>SCALE: 1:50,000 CONTOUR (10m ISOLINES)</span>
              <span>PROJECTION: WGS84 / UTM ZONE 20S</span>
            </div>

            {/* HUD Top-right: Compass Rose */}
            <div className="absolute top-3 right-3 p-2 rounded-xl bg-obsidian-950/85 border border-border-subtle font-mono text-[10px] flex flex-col items-center backdrop-blur-sm">
              <Compass size={24} className="text-emerald-400 animate-spin-slow" />
              <span className="text-emerald-300 font-bold mt-1">N 000°</span>
            </div>

            {/* HUD Bottom-left: Minimap Radar Widget */}
            <div className="absolute bottom-3 left-3 w-28 h-28 rounded-xl bg-obsidian-950/90 border border-emerald-500/30 overflow-hidden flex flex-col items-center justify-center p-1.5 backdrop-blur-md">
              <div className="relative w-20 h-20 rounded-full border border-emerald-500/40 flex items-center justify-center">
                <div className="w-12 h-12 rounded-full border border-emerald-500/20" />
                <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping absolute" />
                <div className="absolute top-1 text-[8px] font-mono text-emerald-400 font-bold">1:50k</div>
              </div>
              <span className="text-[9px] font-mono text-text-faint uppercase mt-1">RADAR WIDGET</span>
            </div>

            {/* HUD Bottom-right: Zoom Controls */}
            <div className="absolute bottom-3 right-3 flex flex-col gap-1.5">
              <button
                onClick={() => setZoomLevel((z) => Math.min(z + 0.2, 1.8))}
                className="p-2 rounded-lg bg-obsidian-950/85 hover:bg-obsidian-900 border border-border text-slate-300 hover:text-emerald-400 transition-colors shadow-lg"
                title="Zoom In"
              >
                <Plus size={16} />
              </button>
              <button
                onClick={() => setZoomLevel((z) => Math.max(z - 0.2, 0.8))}
                className="p-2 rounded-lg bg-obsidian-950/85 hover:bg-obsidian-900 border border-border text-slate-300 hover:text-emerald-400 transition-colors shadow-lg"
                title="Zoom Out"
              >
                <Minus size={16} />
              </button>
            </div>

            {/* Floating Threat Vector Inspector Card (Zone 04 Summary) */}
            {selectedNode && (
              <div className="absolute bottom-16 right-3 sm:right-6 w-80 sm:w-96 p-4 rounded-xl bg-obsidian-950/95 border border-emerald-500/40 shadow-2xl backdrop-blur-xl animate-fade-in font-mono text-xs space-y-2.5">
                <div className="flex items-center justify-between border-b border-border-subtle pb-2">
                  <div className="flex items-center gap-2">
                    <AlertTriangle
                      size={15}
                      className={selectedNode.status === "CRITICAL" ? "text-rose-400" : "text-amber-400"}
                    />
                    <span className="font-panchang font-bold text-text-primary text-[11px] uppercase">
                      {selectedNode.name}
                    </span>
                  </div>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      selectedNode.status === "CRITICAL"
                        ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                        : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                    }`}
                  >
                    {selectedNode.status}
                  </span>
                </div>

                <div className="space-y-1 text-slate-300">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-text-muted">Target Species / Event:</span>
                    <span className="text-emerald-400 font-semibold">{selectedNode.species}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-text-muted">Classification:</span>
                    <span>{selectedNode.category}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-text-muted">Timestamp:</span>
                    <span>{selectedNode.time}</span>
                  </div>
                  {selectedNode.freq && (
                    <div className="flex justify-between text-[11px]">
                      <span className="text-text-muted">Acoustic Signature:</span>
                      <span className="text-amber-400 font-bold">{selectedNode.freq}</span>
                    </div>
                  )}
                </div>

                <p className="text-[11px] text-text-muted leading-relaxed border-t border-border-subtle pt-2">
                  {selectedNode.description}
                </p>

                <button
                  onClick={() => alert(`Drone dispatched to coordinates for ${selectedNode.name}`)}
                  className="w-full py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-obsidian-950 font-bold text-xs tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 shadow-glow-emerald"
                >
                  <Navigation size={13} />
                  <span>View Zone Analysis & Dispatch Drone</span>
                </button>
              </div>
            )}
          </GlassCard>
        </div>

        {/* Side Panel: Live Observations Stream (4/12 on large screens) */}
        <div className="lg:col-span-4 space-y-4">
          <GlassCard className="space-y-3">
            <div className="flex items-center justify-between border-b border-border-subtle pb-2">
              <div className="flex items-center gap-2">
                <Eye size={16} className="text-emerald-400" />
                <h3 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
                  Live Observations Stream
                </h3>
              </div>
              <span className="text-[10px] font-mono text-emerald-400 font-bold">4 TAXA LOGGED</span>
            </div>

            {/* Scrollable list of observation cards */}
            <div className="space-y-2.5 max-h-[520px] overflow-y-auto pr-1">
              {/* Card 1: Bengal Tiger */}
              <div
                onClick={() => setSelectedNode(MAP_NODES[1])}
                className={`p-2.5 rounded-xl border transition-all cursor-pointer flex gap-3 ${
                  selectedNode.id === "node-z02"
                    ? "bg-emerald-500/15 border-emerald-500/50 shadow-glow-sm"
                    : "bg-obsidian-900/80 border-border hover:border-emerald-500/30"
                }`}
              >
                <img
                  src={TIGER_IMAGE}
                  alt="Bengal Tiger"
                  className="w-16 h-16 rounded-lg object-cover shrink-0 border border-emerald-500/20"
                />
                <div className="flex flex-col justify-between min-w-0 flex-1 font-mono text-xs">
                  <div>
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-text-primary truncate">Bengal Tiger</h4>
                      <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-rose-500/20 text-rose-300">
                        CRITICAL
                      </span>
                    </div>
                    <span className="text-[10px] text-text-muted italic block">Panthera tigris</span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-text-faint mt-1">
                    <span>Zone Z-02</span>
                    <span className="text-emerald-400">14:34:22 UTC</span>
                  </div>
                </div>
              </div>

              {/* Card 2: Indian Peafowl */}
              <div
                onClick={() => setSelectedNode(MAP_NODES[2])}
                className={`p-2.5 rounded-xl border transition-all cursor-pointer flex gap-3 ${
                  selectedNode.id === "node-z07"
                    ? "bg-emerald-500/15 border-emerald-500/50 shadow-glow-sm"
                    : "bg-obsidian-900/80 border-border hover:border-emerald-500/30"
                }`}
              >
                <img
                  src={PEAFOWL_IMAGE}
                  alt="Indian Peafowl"
                  className="w-16 h-16 rounded-lg object-cover shrink-0 border border-emerald-500/20"
                />
                <div className="flex flex-col justify-between min-w-0 flex-1 font-mono text-xs">
                  <div>
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-text-primary truncate">Indian Peafowl</h4>
                      <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300">
                        LOW
                      </span>
                    </div>
                    <span className="text-[10px] text-text-muted italic block">Pavo cristatus</span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-text-faint mt-1">
                    <span>Zone Z-07</span>
                    <span className="text-emerald-400">14:31:55 UTC</span>
                  </div>
                </div>
              </div>

              {/* Card 3: Asian Elephant */}
              <div
                onClick={() => setSelectedNode(MAP_NODES[3])}
                className={`p-2.5 rounded-xl border transition-all cursor-pointer flex gap-3 ${
                  selectedNode.id === "node-z01"
                    ? "bg-emerald-500/15 border-emerald-500/50 shadow-glow-sm"
                    : "bg-obsidian-900/80 border-border hover:border-emerald-500/30"
                }`}
              >
                <img
                  src={ELEPHANT_IMAGE}
                  alt="Asian Elephant"
                  className="w-16 h-16 rounded-lg object-cover shrink-0 border border-emerald-500/20"
                />
                <div className="flex flex-col justify-between min-w-0 flex-1 font-mono text-xs">
                  <div>
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-text-primary truncate">Asian Elephant</h4>
                      <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-500/20 text-amber-300">
                        MODERATE
                      </span>
                    </div>
                    <span className="text-[10px] text-text-muted italic block">Elephas maximus</span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-text-faint mt-1">
                    <span>Zone Z-01</span>
                    <span className="text-emerald-400">14:28:10 UTC</span>
                  </div>
                </div>
              </div>

              {/* Card 4: Great Pied Hornbill */}
              <div
                onClick={() => setSelectedNode(MAP_NODES[4])}
                className={`p-2.5 rounded-xl border transition-all cursor-pointer flex gap-3 ${
                  selectedNode.id === "node-z09"
                    ? "bg-emerald-500/15 border-emerald-500/50 shadow-glow-sm"
                    : "bg-obsidian-900/80 border-border hover:border-emerald-500/30"
                }`}
              >
                <img
                  src={HORNBILL_IMAGE}
                  alt="Great Pied Hornbill"
                  className="w-16 h-16 rounded-lg object-cover shrink-0 border border-emerald-500/20"
                />
                <div className="flex flex-col justify-between min-w-0 flex-1 font-mono text-xs">
                  <div>
                    <div className="flex items-center justify-between">
                      <h4 className="font-bold text-text-primary truncate">Great Pied Hornbill</h4>
                      <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300">
                        LOW
                      </span>
                    </div>
                    <span className="text-[10px] text-text-muted italic block">Buceros bicornis</span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-text-faint mt-1">
                    <span>Zone Z-09</span>
                    <span className="text-emerald-400">14:25:40 UTC</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Zone Telemetry Summary */}
            <div className="pt-2 border-t border-border-subtle grid grid-cols-2 gap-2 font-mono text-xs">
              <div className="p-2 rounded bg-obsidian-950 border border-border">
                <span className="text-text-faint text-[10px] block">ACTIVE NODES</span>
                <span className="text-emerald-400 font-bold">48 / 48 (100%)</span>
              </div>
              <div className="p-2 rounded bg-obsidian-950 border border-border">
                <span className="text-text-faint text-[10px] block">CRITICAL ZONES</span>
                <span className="text-rose-400 font-bold">2 VECTORS</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
