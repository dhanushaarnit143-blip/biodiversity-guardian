/**
 * useOverviewMetrics
 * ------------------
 * React Query hook that fetches the full Overview page dataset from
 * GET /api/v1/overview/metrics.
 *
 * Features:
 * - 30s stale time → only refetches after 30 s of inactivity
 * - 5 min cache time → data stays in cache for background tabs
 * - refetchInterval: 60 s → live dashboard auto-refresh
 * - Typed return value: UseQueryResult<OverviewMetrics, Error>
 *
 * Usage:
 *   const { data, isLoading, isError, error } = useOverviewMetrics();
 */

import { useQuery, type UseQueryResult } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";
import type { OverviewMetrics } from "@/types/api";

// ── Query key factory (use this pattern for all hooks) ───────────────────────
export const overviewKeys = {
  all:     ["overview"]              as const,
  metrics: ["overview", "metrics"]   as const,
} as const;

// ── Fetcher ───────────────────────────────────────────────────────────────────
async function fetchOverviewMetrics(): Promise<OverviewMetrics> {
  const { data } = await apiClient.get<OverviewMetrics>("/overview/metrics");
  return data;
}

// ── Hook ─────────────────────────────────────────────────────────────────────
export function useOverviewMetrics(): UseQueryResult<OverviewMetrics, Error> {
  return useQuery({
    queryKey:       overviewKeys.metrics,
    queryFn:        fetchOverviewMetrics,
    staleTime:      30_000,   // 30 s
    gcTime:         300_000,  // 5 min
    refetchInterval:60_000,   // auto-refresh every 60 s
    retry:          2,
    retryDelay:     (attempt) => Math.min(1000 * 2 ** attempt, 10_000),
  });
}
