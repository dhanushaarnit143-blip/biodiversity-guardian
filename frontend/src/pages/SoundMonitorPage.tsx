import { useState, useEffect, useRef } from "react";
import {
  Mic,
  Camera,
  Radio,
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  Volume2,
  Download,
  AlertTriangle,
  RefreshCw,
  Activity,
  CheckCircle,
  Sliders,
  Crosshair,
  Wifi,
  WifiOff,
} from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";

const JAGUAR_IMAGE = "https://lh3.googleusercontent.com/aida-public/AB6AXuBLzADIm0FTKdvvGKvL1L-PWqiiK1OOnEKtvad8UBoe90PM-Zvvu1ei6uxIhQSi8Pq9k4LSSKAl1bmBZVQZ16OzrPKQdbm9haKt7j8dwaFx9oVii3TdWkcWMlOWoW1SezhEQCU3olvhbaCh1rVIpJrTaSeuttIila4iR82Zi1aJ2ERD3FMBxPbGhK_W2w_u8cSgymxbtfBQ6QrP27PwvXYP3TgY-HEGQmDobIiprEU_y1ZEUY-U0yhxnw";

export default function SoundMonitorPage() {
  const [activeTab, setActiveTab] = useState<"audio" | "vision" | "telemetry">("audio");
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [scrubberPosition, setScrubberPosition] = useState<number>(34); // percentage 0-100
  const [volume, setVolume] = useState<number>(80);
  const [isLooping, setIsLooping] = useState<boolean>(true);

  const [activeFilters, setActiveFilters] = useState({
    lowCut: true,
    notchHum: true,
    hiCut: false,
  });

  // Audio Context ref for Web Audio API synthesis
  const audioCtxRef = useRef<AudioContext | null>(null);
  const synthIntervalRef = useRef<number | null>(null);

  // 48-bar visualizer heights state
  const [barHeights, setBarHeights] = useState<number[]>(
    Array.from({ length: 48 }, () => Math.floor(Math.random() * 40) + 10)
  );

  // Animate bars and progress playhead when playing
  useEffect(() => {
    let timerId: number | null = null;

    if (isPlaying) {
      timerId = window.setInterval(() => {
        setBarHeights(
          Array.from({ length: 48 }, (_, i) => {
            // Harmonic clusters around center
            const peak = Math.sin((i / 48) * Math.PI * 3);
            const base = Math.max(10, Math.floor(Math.abs(peak) * 60 + Math.random() * 25));
            return base;
          })
        );
        setScrubberPosition((prev) => (prev >= 100 ? (isLooping ? 0 : 100) : prev + 0.5));
      }, 100);
    } else {
      // Quiet resting state
      setBarHeights(Array.from({ length: 48 }, () => Math.floor(Math.random() * 15) + 6));
    }

    return () => {
      if (timerId !== null) clearInterval(timerId);
    };
  }, [isPlaying, isLooping]);

  // Web Audio Bioacoustic Synthesizer
  const togglePlayAudio = () => {
    if (isPlaying) {
      // Stop synthesis
      setIsPlaying(false);
      if (synthIntervalRef.current) {
        clearInterval(synthIntervalRef.current);
        synthIntervalRef.current = null;
      }
      if (audioCtxRef.current && audioCtxRef.current.state !== "closed") {
        audioCtxRef.current.suspend();
      }
    } else {
      // Start synthesis
      setIsPlaying(true);
      try {
        const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        if (!audioCtxRef.current) {
          audioCtxRef.current = new AudioCtx();
        }
        if (audioCtxRef.current.state === "suspended") {
          audioCtxRef.current.resume();
        }

        const ctx = audioCtxRef.current;

        // Function to create a short natural bird chirp
        const playChirp = () => {
          if (!ctx || ctx.state === "closed") return;
          const now = ctx.currentTime;
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();

          // Randomized natural avian frequency sweep (e.g. 2100Hz -> 3400Hz -> 1800Hz)
          const baseFreq = 1800 + Math.random() * 1600;
          osc.type = "sine";
          osc.frequency.setValueAtTime(baseFreq, now);
          osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.4, now + 0.08);
          osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.9, now + 0.18);

          // Gentle gain envelope
          gain.gain.setValueAtTime(0, now);
          gain.gain.linearRampToValueAtTime((volume / 100) * 0.08, now + 0.03);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);

          osc.connect(gain);
          gain.connect(ctx.destination);

          osc.start(now);
          osc.stop(now + 0.25);
        };

        // Play immediate chirp and recurring harmonic rhythm
        playChirp();
        synthIntervalRef.current = window.setInterval(() => {
          if (Math.random() > 0.3) {
            playChirp();
          }
        }, 320);
      } catch (err) {
        console.warn("Web Audio not supported or blocked by policy:", err);
      }
    }
  };

  // Clean up AudioContext on unmount
  useEffect(() => {
    return () => {
      if (synthIntervalRef.current) clearInterval(synthIntervalRef.current);
      if (audioCtxRef.current && audioCtxRef.current.state !== "closed") {
        audioCtxRef.current.close();
      }
    };
  }, []);

  return (
    <div className="space-y-4 pb-12">
      {/* ── Tab Switcher Bar ── */}
      <div className="flex items-center justify-between gap-3 p-2 rounded-xl bg-obsidian-850/80 border border-emerald-500/20 backdrop-blur-md">
        <div className="flex items-center gap-1.5 font-mono text-xs">
          <button
            onClick={() => setActiveTab("audio")}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg font-bold tracking-wider uppercase transition-all ${
              activeTab === "audio"
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-glow-sm"
                : "text-text-muted hover:text-text-primary hover:bg-white/5"
            }`}
          >
            <Mic size={15} />
            <span>Bioacoustic Engine v2.4</span>
          </button>

          <button
            onClick={() => setActiveTab("vision")}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg font-bold tracking-wider uppercase transition-all ${
              activeTab === "vision"
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-glow-sm"
                : "text-text-muted hover:text-text-primary hover:bg-white/5"
            }`}
          >
            <Camera size={15} />
            <span>Wildlife Camera Trap Vision</span>
          </button>

          <button
            onClick={() => setActiveTab("telemetry")}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg font-bold tracking-wider uppercase transition-all ${
              activeTab === "telemetry"
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-glow-sm"
                : "text-text-muted hover:text-text-primary hover:bg-white/5"
            }`}
          >
            <Radio size={15} />
            <span>Edge Sensor Telemetry</span>
          </button>
        </div>

        <div className="hidden sm:flex items-center gap-2 font-mono text-xs text-text-muted">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>BUFFER: 96kHz / 24-BIT LOSSLESS</span>
        </div>
      </div>

      {/* ── TAB 1: BIOACOUSTIC ENGINE ── */}
      {activeTab === "audio" && (
        <div className="space-y-4">
          {/* Mel Spectrogram Matrix */}
          <GlassCard padded={false} className="relative overflow-hidden border-emerald-500/30">
            {/* Header row */}
            <div className="p-3 bg-obsidian-950/80 border-b border-border-subtle flex items-center justify-between font-mono text-xs">
              <div className="flex items-center gap-2">
                <Activity size={15} className="text-emerald-400 animate-pulse" />
                <span className="font-bold text-text-primary">
                  MEL SPECTROGRAM — ZONE 04 / MIC ARRAY (M01-M09)
                </span>
              </div>
              <span className="text-text-faint text-[11px]">
                96kHz • 16-BIT • FFT: 2048pt • HOP: 512 • HANNING WINDOW
              </span>
            </div>

            {/* Spectrogram Grid Container */}
            <div className="relative h-72 sm:h-80 w-full bg-[#070b12] flex">
              {/* Y-Axis Frequency scale */}
              <div className="w-16 h-full border-r border-border-subtle flex flex-col justify-between py-2 px-1 text-[10px] font-mono text-text-faint select-none shrink-0 bg-obsidian-950/60">
                <span>16.0 kHz</span>
                <span>14.0 kHz</span>
                <span>12.0 kHz</span>
                <span>10.0 kHz</span>
                <span>8.0 kHz</span>
                <span>6.0 kHz</span>
                <span>4.0 kHz</span>
                <span>2.0 kHz</span>
                <span>0.0 Hz</span>
              </div>

              {/* Heatmap Matrix Surface */}
              <div className="relative flex-1 h-full overflow-hidden bg-gradient-to-b from-[#0a121e] via-[#081f18] to-[#040e0b]">
                {/* Horizontal frequency reference guide lines */}
                <div className="absolute inset-0 flex flex-col justify-between pointer-events-none opacity-20">
                  {Array.from({ length: 9 }).map((_, i) => (
                    <div key={i} className="border-b border-emerald-500/30 w-full" />
                  ))}
                </div>

                {/* Simulated Energy Patterns (CSS Frequency bands) */}
                <div className="absolute top-[52%] left-[10%] w-[38%] h-[26%] bg-gradient-to-r from-emerald-500/20 via-emerald-400/45 to-teal-400/20 rounded-full blur-md" />
                <div className="absolute top-[24%] left-[48%] w-[32%] h-[28%] bg-gradient-to-r from-sky-500/25 via-blue-400/40 to-emerald-400/25 rounded-full blur-md" />
                <div className="absolute top-[75%] left-[2%] w-[96%] h-[18%] bg-gradient-to-r from-amber-500/15 via-red-500/20 to-amber-500/15 blur-sm" />

                {/* Bounding Box 1: Asian Koel (2.1 - 4.5kHz) */}
                <div
                  className="absolute top-[48%] left-[12%] w-[28%] h-[28%] border-2 border-emerald-400 bg-emerald-400/15 rounded-sm flex flex-col justify-between p-1 select-none animate-pulse"
                  style={{ backdropFilter: "blur(1px)" }}
                >
                  <div className="flex items-center justify-between">
                    <span className="px-1.5 py-0.5 bg-emerald-500 text-obsidian-950 font-mono text-[9px] font-bold">
                      ASIAN KOEL // 81%
                    </span>
                    <span className="text-[9px] font-mono text-emerald-300 font-semibold">2.1 - 4.5 kHz</span>
                  </div>
                  <span className="text-[8px] font-mono text-emerald-200">CALL: ASCENDING FLUTE</span>
                </div>

                {/* Bounding Box 2: Indian Peafowl (4.8 - 8.2kHz) */}
                <div
                  className="absolute top-[22%] left-[52%] w-[26%] h-[32%] border-2 border-sky-400 bg-sky-400/15 rounded-sm flex flex-col justify-between p-1 select-none animate-pulse"
                  style={{ backdropFilter: "blur(1px)" }}
                >
                  <div className="flex items-center justify-between">
                    <span className="px-1.5 py-0.5 bg-sky-500 text-obsidian-950 font-mono text-[9px] font-bold">
                      INDIAN PEAFOWL // 87%
                    </span>
                    <span className="text-[9px] font-mono text-sky-300 font-semibold">4.8 - 8.2 kHz</span>
                  </div>
                  <span className="text-[8px] font-mono text-sky-200">CALL: TRUMPETING HARMONIC</span>
                </div>

                {/* Dynamic Scrubbing Playhead Line */}
                <div
                  className="absolute top-0 bottom-0 w-[2px] bg-emerald-400 pointer-events-none shadow-glow-emerald transition-all duration-75"
                  style={{ left: `${scrubberPosition}%` }}
                >
                  <div className="w-2.5 h-2.5 -ml-1 bg-emerald-400 rounded-full" />
                </div>
              </div>
            </div>

            {/* X-Axis Time Labels */}
            <div className="flex justify-between pl-16 pr-4 py-1.5 bg-obsidian-950 text-[10px] font-mono text-text-faint border-t border-border-subtle">
              <span>00:00</span>
              <span>00:30</span>
              <span>01:00</span>
              <span>01:30</span>
              <span>02:00</span>
              <span>02:30</span>
              <span>02:45 UTC</span>
            </div>

            {/* 48-Bar RMS Visualizer Strip */}
            <div className="p-3 bg-obsidian-900 border-t border-border-subtle flex items-center gap-1 h-16">
              {barHeights.map((h, i) => (
                <div
                  key={i}
                  className="flex-1 bg-obsidian-950 rounded-t-sm overflow-hidden flex items-end h-full"
                >
                  <div
                    className={`w-full transition-all duration-100 ${
                      i > 15 && i < 28
                        ? "bg-emerald-400"
                        : i >= 28 && i < 38
                        ? "bg-sky-400"
                        : "bg-emerald-600/70"
                    }`}
                    style={{ height: `${h}%` }}
                  />
                </div>
              ))}
            </div>

            {/* Interactive Timeline Scrubber + Transport Controls */}
            <div className="p-4 bg-obsidian-950/90 border-t border-border-subtle space-y-3">
              {/* Range input scrubber */}
              <input
                type="range"
                min="0"
                max="100"
                value={scrubberPosition}
                onChange={(e) => setScrubberPosition(Number(e.target.value))}
                className="w-full accent-emerald-400 cursor-pointer h-1.5 bg-obsidian-700 rounded-lg"
              />

              {/* Transport Buttons row */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-3 font-mono text-xs">
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setScrubberPosition(0)}
                    className="p-2 rounded-lg bg-obsidian-800 hover:bg-obsidian-700 text-text-muted hover:text-emerald-400 transition-colors"
                    title="Rewind to start"
                  >
                    <SkipBack size={15} />
                  </button>

                  <button
                    onClick={togglePlayAudio}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-obsidian-950 font-bold tracking-wider uppercase transition-all shadow-glow-emerald"
                  >
                    {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                    <span>{isPlaying ? "PAUSE AUDIO" : "PLAY 96kHz BUFFER"}</span>
                  </button>

                  <button
                    onClick={() => setScrubberPosition((p) => Math.min(p + 10, 100))}
                    className="p-2 rounded-lg bg-obsidian-800 hover:bg-obsidian-700 text-text-muted hover:text-emerald-400 transition-colors"
                    title="Skip 10s"
                  >
                    <SkipForward size={15} />
                  </button>

                  <button
                    onClick={() => setIsLooping(!isLooping)}
                    className={`p-2 rounded-lg transition-colors ${
                      isLooping
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                        : "bg-obsidian-800 text-text-faint hover:text-text-muted"
                    }`}
                    title="Toggle Loop"
                  >
                    <RotateCcw size={15} />
                  </button>
                </div>

                {/* Volume slider */}
                <div className="flex items-center gap-2">
                  <Volume2 size={15} className="text-text-muted" />
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={volume}
                    onChange={(e) => setVolume(Number(e.target.value))}
                    className="w-24 accent-emerald-400 cursor-pointer"
                  />
                  <span className="w-8 text-text-faint text-[11px]">{volume}%</span>
                </div>

                {/* Audio filter pills */}
                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setActiveFilters((f) => ({ ...f, lowCut: !f.lowCut }))}
                    className={`px-2 py-1 rounded text-[10px] font-bold ${
                      activeFilters.lowCut
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                        : "bg-obsidian-800 text-text-faint"
                    }`}
                  >
                    Low-cut 500Hz
                  </button>
                  <button
                    onClick={() => setActiveFilters((f) => ({ ...f, notchHum: !f.notchHum }))}
                    className={`px-2 py-1 rounded text-[10px] font-bold ${
                      activeFilters.notchHum
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                        : "bg-obsidian-800 text-text-faint"
                    }`}
                  >
                    Notch Hum
                  </button>
                  <button
                    onClick={() => setActiveFilters((f) => ({ ...f, hiCut: !f.hiCut }))}
                    className={`px-2 py-1 rounded text-[10px] font-bold ${
                      activeFilters.hiCut
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                        : "bg-obsidian-800 text-text-faint"
                    }`}
                  >
                    Hi-cut 14k
                  </button>
                </div>
              </div>
            </div>
          </GlassCard>

          {/* Multi-Label Species Classification + Synced Optical Verification */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Multi-Label Classification */}
            <GlassCard className="space-y-3">
              <div className="flex items-center justify-between border-b border-border-subtle pb-2 font-mono">
                <span className="font-bold text-xs uppercase tracking-wider text-text-primary">
                  Multi-Label CNN Bioacoustic Classification
                </span>
                <span className="text-[10px] text-emerald-400 font-semibold">96kHz INFERENCE</span>
              </div>

              <div className="space-y-3 font-mono text-xs">
                {/* Species 1 */}
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="font-semibold text-text-primary">Indian Peafowl (Pavo cristatus)</span>
                    <span className="text-emerald-400 font-bold">87%</span>
                  </div>
                  <div className="w-full h-2 rounded bg-obsidian-800 overflow-hidden">
                    <div className="h-full bg-emerald-400 rounded" style={{ width: "87%" }} />
                  </div>
                  <div className="flex justify-between text-[10px] text-text-faint">
                    <span>Harmonic: 4.8 - 8.2 kHz</span>
                    <span>Confidence Tier: HIGH</span>
                  </div>
                </div>

                {/* Species 2 */}
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="font-semibold text-text-primary">Asian Koel (Eudynamys scolopaceus)</span>
                    <span className="text-teal-400 font-bold">81%</span>
                  </div>
                  <div className="w-full h-2 rounded bg-obsidian-800 overflow-hidden">
                    <div className="h-full bg-teal-400 rounded" style={{ width: "81%" }} />
                  </div>
                  <div className="flex justify-between text-[10px] text-text-faint">
                    <span>Harmonic: 2.1 - 4.5 kHz</span>
                    <span>Confidence Tier: HIGH</span>
                  </div>
                </div>

                {/* Species 3 */}
                <div className="space-y-1">
                  <div className="flex justify-between">
                    <span className="font-semibold text-text-primary">Amphibian Chorus (Anura spp.)</span>
                    <span className="text-sky-400 font-bold">76%</span>
                  </div>
                  <div className="w-full h-2 rounded bg-obsidian-800 overflow-hidden">
                    <div className="h-full bg-sky-400 rounded" style={{ width: "76%" }} />
                  </div>
                  <div className="flex justify-between text-[10px] text-text-faint">
                    <span>Harmonic: 800 - 1.6 kHz</span>
                    <span>Confidence Tier: MODERATE</span>
                  </div>
                </div>
              </div>
            </GlassCard>

            {/* Synced Optical Verification */}
            <GlassCard className="space-y-3 border-emerald-500/30">
              <div className="flex items-center justify-between border-b border-border-subtle pb-2 font-mono">
                <span className="font-bold text-xs uppercase tracking-wider text-text-primary">
                  Synced Optical Verification — CAM-04
                </span>
                <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300">
                  MATCH CONFIRMED
                </span>
              </div>

              <div className="relative h-44 rounded-lg overflow-hidden bg-obsidian-950 border border-border">
                <img
                  src={JAGUAR_IMAGE}
                  alt="Optical Verification Jaguar"
                  className="w-full h-full object-cover filter contrast-125"
                />
                <div className="absolute top-2 left-2 px-2 py-0.5 rounded bg-black/70 font-mono text-[9px] text-emerald-400 border border-emerald-500/30">
                  CAM-04 // 02:14:18 UTC
                </div>
                <div className="absolute bottom-2 inset-x-2 p-2 rounded bg-black/80 font-mono text-xs flex items-center justify-between text-slate-200">
                  <span>Panthera onca (Visual Keyframe)</span>
                  <span className="text-emerald-400 font-bold">94.1% CROSS-MATCH</span>
                </div>
              </div>

              <p className="text-xs font-mono text-text-muted leading-relaxed">
                Bioacoustic footprint coincides within 0.4s of motion-triggered infrared capture. Acoustic-visual triangulation confirmed.
              </p>
            </GlassCard>
          </div>

          {/* Action Buttons Row */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() => alert("Spectrogram matrix exported (CSV / FLAC / GeoTIFF)")}
              className="flex-1 py-2.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 text-amber-300 font-bold text-xs uppercase tracking-wider font-mono transition-all flex items-center justify-center gap-2"
            >
              <Download size={15} />
              <span>Export Spectrogram</span>
            </button>

            <button
              onClick={() => alert("Anomaly flagged and committed to incident dispatch register")}
              className="flex-1 py-2.5 rounded-xl bg-rose-500/15 hover:bg-rose-500/25 border border-rose-500/40 text-rose-300 font-bold text-xs uppercase tracking-wider font-mono transition-all flex items-center justify-center gap-2"
            >
              <AlertTriangle size={15} />
              <span>Flag Anomaly</span>
            </button>

            <button
              onClick={() => alert("Edge weights synchronized with CNN inference engine")}
              className="flex-1 py-2.5 rounded-xl bg-sky-500/15 hover:bg-sky-500/25 border border-sky-500/40 text-sky-300 font-bold text-xs uppercase tracking-wider font-mono transition-all flex items-center justify-center gap-2"
            >
              <RefreshCw size={15} />
              <span>Update Edge Weights</span>
            </button>
          </div>
        </div>
      )}

      {/* ── TAB 2: WILDLIFE CAMERA TRAP VISION ── */}
      {activeTab === "vision" && (
        <div className="space-y-4 font-mono">
          <GlassCard className="space-y-4">
            <div className="flex items-center justify-between border-b border-border-subtle pb-2">
              <div className="flex items-center gap-2">
                <Camera size={16} className="text-emerald-400" />
                <h3 className="font-panchang font-bold text-sm text-text-primary uppercase">
                  Wildlife Camera Trap Vision — IR Array
                </h3>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">
                CAM-09B ACTIVE
              </span>
            </div>

            <div className="relative h-96 w-full rounded-xl overflow-hidden bg-obsidian-950 border border-emerald-500/30">
              <img
                src={JAGUAR_IMAGE}
                alt="Wildlife Camera Trap Large View"
                className="w-full h-full object-cover filter contrast-125"
              />

              {/* Bounding Box overlay */}
              <div className="absolute top-[20%] left-[25%] w-[45%] h-[55%] border-2 border-amber-400 bg-amber-400/10 rounded-sm flex flex-col justify-between p-2">
                <span className="px-2 py-0.5 bg-amber-500 text-obsidian-950 font-bold text-xs inline-block self-start">
                  Panthera onca [87.2%]
                </span>
                <div className="flex justify-between text-[10px] text-amber-300 font-bold">
                  <span>GAIT: PROWLING</span>
                  <span>EST. WEIGHT: 78kg</span>
                </div>
              </div>

              {/* Bottom metadata */}
              <div className="absolute bottom-3 inset-x-3 p-3 rounded-lg bg-black/80 backdrop-blur-md flex items-center justify-between text-xs text-slate-300">
                <span>SENSOR: IR-09B // GRID E-7 CORRIDOR</span>
                <span>PIR SENSITIVITY: HIGH</span>
                <span className="text-emerald-400 font-bold">TIME: 14:32:10 UTC</span>
              </div>
            </div>
          </GlassCard>
        </div>
      )}

      {/* ── TAB 3: EDGE SENSOR TELEMETRY ── */}
      {activeTab === "telemetry" && (
        <div className="space-y-4 font-mono">
          <GlassCard className="space-y-3">
            <div className="flex items-center justify-between border-b border-border-subtle pb-2">
              <div className="flex items-center gap-2">
                <Radio size={16} className="text-emerald-400" />
                <h3 className="font-panchang font-bold text-sm text-text-primary uppercase">
                  14-Microphone Array Node Telemetry (M01 - M14)
                </h3>
              </div>
              <span className="text-xs text-text-muted">11 ONLINE • 3 SUPPRESSED</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5">
              {Array.from({ length: 14 }).map((_, idx) => {
                const nodeNum = idx + 1;
                const nodeId = `M${nodeNum < 10 ? "0" + nodeNum : nodeNum}`;
                const isSuppressed = nodeNum >= 10 && nodeNum <= 12;

                return (
                  <div
                    key={nodeId}
                    className={`p-3 rounded-xl border flex flex-col justify-between h-28 ${
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
                      <div className="text-[10px] text-text-faint">
                        {isSuppressed ? "SUPPRESSED" : "SIGNAL: 98%"}
                      </div>
                      <div className="w-full h-1.5 rounded-full bg-obsidian-950 overflow-hidden">
                        <div
                          className={`h-full rounded-full ${isSuppressed ? "bg-amber-400" : "bg-emerald-400"}`}
                          style={{ width: isSuppressed ? "25%" : "88%" }}
                        />
                      </div>
                    </div>

                    <div className="text-[9px] text-text-faint">Ping: 12ms</div>
                  </div>
                );
              })}
            </div>
          </GlassCard>
        </div>
      )}
    </div>
  );
}
