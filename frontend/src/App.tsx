import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import TopNav from "@/components/layout/TopNav";

// ── Lazy-load pages — each page is a separate chunk ──────────────────────────
// Phase 5: React Router → Streamlit page mapping
//
//   Streamlit page          →   React Route
//   ─────────────────────────────────────────────────────
//   "🏠 Overview"           →   /
//   "🗺️ Biodiversity Map"   →   /map
//   "🎙️ Sound Monitor"      →   /sound-monitor
//   "📷 Wildlife Monitor"   →   /wildlife-monitor
//   "🤖 Conservation AI"    →   /conservation-ai

const OverviewPage       = lazy(() => import("@/pages/OverviewPage"));
const BiodiversityMapPage= lazy(() => import("@/pages/BiodiversityMapPage"));
const SoundMonitorPage   = lazy(() => import("@/pages/SoundMonitorPage"));
const WildlifeMonitorPage= lazy(() => import("@/pages/WildlifeMonitorPage"));
const ConservationAIPage = lazy(() => import("@/pages/ConservationAIPage"));

// ── Loading skeleton (matches glassmorphism style) ────────────────────────────
function PageSkeleton() {
  return (
    <div className="flex flex-col gap-3 animate-pulse p-4">
      <div className="h-6 w-64 rounded-lg bg-obsidian-700/60" />
      <div className="grid grid-cols-4 gap-3">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-28 rounded-xl bg-obsidian-700/40" />
        ))}
      </div>
      <div className="h-64 rounded-xl bg-obsidian-700/40 mt-2" />
    </div>
  );
}

// ── App ───────────────────────────────────────────────────────────────────────
export default function App() {
  return (
    <>
      <TopNav />
      <main style={{ paddingTop: "60px" }} className="min-h-screen bg-obsidian-900">
        <div className="max-w-[1600px] mx-auto p-4">
          <Suspense fallback={<PageSkeleton />}>
            <Routes>
              <Route path="/"                 element={<OverviewPage />}        />
              <Route path="/map"              element={<BiodiversityMapPage />} />
              <Route path="/sound-monitor"    element={<SoundMonitorPage />}    />
              <Route path="/wildlife-monitor" element={<WildlifeMonitorPage />} />
              <Route path="/conservation-ai"  element={<ConservationAIPage />}  />
              {/* 404 — redirect to overview */}
              <Route path="*"                 element={<OverviewPage />}        />
            </Routes>
          </Suspense>
        </div>
      </main>
    </>
  );
}
