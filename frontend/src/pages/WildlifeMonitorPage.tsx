import { useState } from "react";
import { Camera, Eye, AlertTriangle, Crosshair, Download, RefreshCw, Shield, Sliders } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";

const JAGUAR_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuBLzADIm0FTKdvvGKvL1L-PWqiiK1OOnEKtvad8UBoe90PM-Zvvu1ei6uxIhQSi8Pq9k4LSSKAl1bmBZVQZ16OzrPKQdbm9haKt7j8dwaFx9oVii3TdWkcWMlOWoW1SezhEQCU3olvhbaCh1rVIpJrTaSeuttIila4iR82Zi1aJ2ERD3FMBxPbGhK_W2w_u8cSgymxbtfBQ6QrP27PwvXYP3TgY-HEGQmDobIiprEU_y1ZEUY-U0yhxnw";
const CANOPY_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuCJ8L-HmDUv7A82WjHj79aQBuHaI6soubxVBptfJzTubGzo42M8LWL17h88WhjI6E1DuuMZukoR0Exv4Tp0CYbU-J2i-ZQu_OsFUffrICFFzCbjJsEwbp1pkXN_d58srRXtWMmeDBv-5gCNn-C-sT3MfOflTkRB5TtNhoNuEqPkCWxEUsRW8tkjSiKoBwNyf74Vmonhh1ItdT3HlUeFERvP9KKqA7ep7MCp9Zmquy3U8y_dQXjyXYlFUw";

export default function WildlifeMonitorPage() {
  const [selectedFeed, setSelectedFeed] = useState<"cam-04" | "ir-09">("ir-09");
  const [pirSensitivity, setPirSensitivity] = useState(85);

  return (
    <div className="space-y-4 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 rounded-xl bg-obsidian-850/80 border border-emerald-500/20 backdrop-blur-md">
        <div>
          <h1 className="text-base sm:text-lg font-panchang font-bold text-gradient-eco uppercase tracking-wider">
            Wildlife Camera Trap Vision Array
          </h1>
          <p className="text-xs font-mono text-text-muted">
            High-Resolution Optical & Thermal Wildlife Reconnaissance
          </p>
        </div>
        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-bold">
            48 CAMERA TRAPS ONLINE (96% SYNC)
          </span>
        </div>
      </div>

      {/* Main Stream View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Large Viewport (8 cols) */}
        <div className="lg:col-span-8 space-y-3">
          <GlassCard padded={false} className="relative h-[520px] rounded-2xl overflow-hidden border-emerald-500/30 bg-black">
            <img
              src={selectedFeed === "ir-09" ? JAGUAR_IMAGE : CANOPY_IMAGE}
              alt="Live Wildlife Camera Stream"
              className="w-full h-full object-cover filter contrast-125"
            />

            {/* Camera Overlay Badges */}
            <div className="absolute top-4 left-4 flex items-center gap-2">
              <span className="px-2.5 py-1 rounded bg-red-600 font-mono text-[10px] font-bold text-white tracking-widest uppercase flex items-center gap-1.5 shadow-lg">
                <span className="h-2 w-2 rounded-full bg-white animate-pulse" />
                LIVE REC // {selectedFeed === "ir-09" ? "IR-09B" : "CAM-04A"}
              </span>
              <span className="px-2.5 py-1 rounded bg-black/70 backdrop-blur-md border border-white/20 font-mono text-[10px] text-emerald-300">
                {selectedFeed === "ir-09" ? "THERMAL 850nm" : "OPTICAL 4K HDR"}
              </span>
            </div>

            {/* Bounding Box Overlay */}
            {selectedFeed === "ir-09" ? (
              <div className="absolute top-[22%] left-[26%] w-[48%] h-[56%] border-2 border-amber-400 bg-amber-400/10 rounded-sm flex flex-col justify-between p-2 pointer-events-none animate-pulse">
                <div className="flex justify-between items-center">
                  <span className="px-2 py-0.5 bg-amber-500 text-obsidian-950 font-mono text-xs font-bold">
                    Panthera onca [87.2%]
                  </span>
                  <span className="text-amber-300 font-mono text-[10px] font-bold">CONF: HIGH</span>
                </div>
                <div className="flex justify-between font-mono text-[10px] text-amber-200 bg-black/70 px-2 py-1 rounded">
                  <span>GAIT: PROWLING (2.4 km/h)</span>
                  <span>EST. MASS: 78kg</span>
                </div>
              </div>
            ) : (
              <div className="absolute top-[20%] left-[30%] w-[42%] h-[46%] border-2 border-emerald-400 bg-emerald-400/10 rounded-sm flex flex-col justify-between p-2 pointer-events-none animate-pulse">
                <span className="px-2 py-0.5 bg-emerald-500 text-obsidian-950 font-mono text-xs font-bold inline-block self-start">
                  Harpyhaliaetus solitarius [98.4%]
                </span>
                <span className="text-emerald-200 font-mono text-[10px] bg-black/70 px-2 py-1 rounded inline-block self-end">
                  PERCHED ELEVATION: 38m
                </span>
              </div>
            )}

            {/* Bottom Controls Bar */}
            <div className="absolute bottom-4 inset-x-4 p-3 rounded-xl bg-black/85 backdrop-blur-md border border-white/10 flex items-center justify-between font-mono text-xs text-slate-300">
              <span>LAT -03.4653° / LON -62.2159°</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => alert("High-res keyframe snapshot saved")}
                  className="px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-obsidian-950 font-bold tracking-wider text-[11px] uppercase transition-all"
                >
                  Capture Keyframe
                </button>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Side Feeds & Controls (4 cols) */}
        <div className="lg:col-span-4 space-y-3 font-mono text-xs">
          <GlassCard className="space-y-3">
            <h3 className="font-panchang font-bold text-xs uppercase tracking-wider text-text-primary">
              Active Optical Traps
            </h3>

            {/* Feed Selector 1 */}
            <div
              onClick={() => setSelectedFeed("ir-09")}
              className={`p-2.5 rounded-xl border transition-all cursor-pointer flex gap-3 ${
                selectedFeed === "ir-09"
                  ? "bg-emerald-500/15 border-emerald-500/50 shadow-glow-sm"
                  : "bg-obsidian-900 border-border hover:border-emerald-500/30"
              }`}
            >
              <img src={JAGUAR_IMAGE} alt="IR-09B" className="w-16 h-16 rounded-lg object-cover" />
              <div className="flex flex-col justify-between flex-1">
                <div>
                  <span className="font-bold text-text-primary block">IR-09B // Understory</span>
                  <span className="text-[10px] text-text-muted">Target: Panthera onca</span>
                </div>
                <span className="text-[10px] text-emerald-400 font-semibold">SIGNAL: 99% 14:32:10 UTC</span>
              </div>
            </div>

            {/* Feed Selector 2 */}
            <div
              onClick={() => setSelectedFeed("cam-04")}
              className={`p-2.5 rounded-xl border transition-all cursor-pointer flex gap-3 ${
                selectedFeed === "cam-04"
                  ? "bg-emerald-500/15 border-emerald-500/50 shadow-glow-sm"
                  : "bg-obsidian-900 border-border hover:border-emerald-500/30"
              }`}
            >
              <img src={CANOPY_IMAGE} alt="CAM-04A" className="w-16 h-16 rounded-lg object-cover" />
              <div className="flex flex-col justify-between flex-1">
                <div>
                  <span className="font-bold text-text-primary block">CAM-04A // Canopy Alpha</span>
                  <span className="text-[10px] text-text-muted">Target: Harpyhaliaetus</span>
                </div>
                <span className="text-[10px] text-emerald-400 font-semibold">SIGNAL: 96% 14:30:45 UTC</span>
              </div>
            </div>

            {/* Sensor Calibration Sliders */}
            <div className="pt-2 border-t border-border-subtle space-y-2">
              <div className="flex justify-between text-[11px]">
                <span className="text-text-muted">PIR TRIGGER SENSITIVITY</span>
                <span className="text-emerald-400 font-bold">{pirSensitivity}%</span>
              </div>
              <input
                type="range"
                min="20"
                max="100"
                value={pirSensitivity}
                onChange={(e) => setPirSensitivity(Number(e.target.value))}
                className="w-full accent-emerald-400 cursor-pointer"
              />
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
