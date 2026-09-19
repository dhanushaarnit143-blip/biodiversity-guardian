/**
 * Additional React Query hooks for all API domains.
 * One hook file per domain keeps imports clean and avoids circular deps.
 */

// ── Audio hooks ───────────────────────────────────────────────────────────────

import { useMutation, useQuery, type UseQueryResult } from "@tanstack/react-query";
import { apiClient } from "@/lib/apiClient";
import type {
  AudioClassificationResult,
  ConservationQueryRequest,
  ConservationQueryResult,
  MapData,
  MultiSpeciesAudioResult,
  RiskFeatureInput,
  RiskPredictionResult,
  WildlifeDetectionResult,
} from "@/types/api";

// ── Audio ─────────────────────────────────────────────────────────────────────

/**
 * useclassifyAudio
 * Upload a single clip and get the top species.
 * Uses `useMutation` because it's a user-triggered POST with a file.
 *
 * const { mutate, data, isPending } = useClassifyAudio();
 * mutate(formData);  // formData contains the audio file
 */
export function useClassifyAudio() {
  return useMutation<AudioClassificationResult, Error, FormData>({
    mutationFn: async (formData) => {
      const { data } = await apiClient.post<AudioClassificationResult>(
        "/audio/classify",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } },
      );
      return data;
    },
  });
}

/**
 * useIdentifyAllSpecies
 * Upload a longer recording and get an aggregated species count.
 */
export function useIdentifyAllSpecies() {
  return useMutation<MultiSpeciesAudioResult, Error, FormData>({
    mutationFn: async (formData) => {
      const { data } = await apiClient.post<MultiSpeciesAudioResult>(
        "/audio/identify-all",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } },
      );
      return data;
    },
  });
}

// ── Vision ────────────────────────────────────────────────────────────────────

/**
 * useDetectWildlife
 * Upload a camera-trap image and receive bounding boxes.
 */
export function useDetectWildlife() {
  return useMutation<WildlifeDetectionResult, Error, FormData>({
    mutationFn: async (formData) => {
      const { data } = await apiClient.post<WildlifeDetectionResult>(
        "/vision/detect",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } },
      );
      return data;
    },
  });
}

// ── Risk ──────────────────────────────────────────────────────────────────────

/**
 * usePredictRisk
 * Submit 12 ecosystem features → risk level + SHAP factors.
 */
export function usePredictRisk() {
  return useMutation<RiskPredictionResult, Error, RiskFeatureInput>({
    mutationFn: async (features) => {
      const { data } = await apiClient.post<RiskPredictionResult>(
        "/risk/predict",
        features,
      );
      return data;
    },
  });
}

// ── Conservation ──────────────────────────────────────────────────────────────

/**
 * useConservationRecommendation
 * Natural language or structured scenario → LLM recommendation.
 * Note: May take 10–30 s on LLM cold start.
 */
export function useConservationRecommendation() {
  return useMutation<ConservationQueryResult, Error, ConservationQueryRequest>({
    mutationFn: async (body) => {
      const { data } = await apiClient.post<ConservationQueryResult>(
        "/conservation/recommend",
        body,
      );
      return data;
    },
  });
}

// ── Map ───────────────────────────────────────────────────────────────────────

const MAP_KEYS = {
  data: ["map", "data"] as const,
};

async function fetchMapData(): Promise<MapData> {
  const { data } = await apiClient.get<MapData>("/map/data");
  return data;
}

/**
 * useMapData
 * Sensor markers + zone polygons for React-Leaflet.
 * 5-minute stale time — map data doesn't change that often.
 */
export function useMapData(): UseQueryResult<MapData, Error> {
  return useQuery({
    queryKey:  MAP_KEYS.data,
    queryFn:   fetchMapData,
    staleTime: 300_000,   // 5 min
    gcTime:    600_000,   // 10 min
  });
}
