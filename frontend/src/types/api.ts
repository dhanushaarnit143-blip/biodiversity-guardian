/**
 * TypeScript interfaces that mirror the FastAPI Pydantic schemas in api/core/schemas.py.
 *
 * Keep these in sync with the backend schemas. When the backend changes,
 * update these types and TypeScript's compiler will surface any mismatches.
 */

// ── Common ───────────────────────────────────────────────────────────────────

export type RiskLevel = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";
export type SpeciesStatus = "Stable" | "Declining" | "Critical";
export type SensorType = "audio" | "camera" | "environmental";
export type SensorStatus = "online" | "offline" | "warning";

// ── Overview ─────────────────────────────────────────────────────────────────

export interface ShannonDataPoint {
  label:    string;
  observed: number;
  baseline: number;
}

export interface TaxaBreakdown {
  taxa:          string;
  species_count: number;
  abundance:     number;
  trend_90d:     string;
}

export interface SpeciesTrendRow {
  species:    string;
  taxon:      string;
  status:     SpeciesStatus;
  obs_count:  number;
  change_90d: string;
}

export interface OverviewMetrics {
  biodiversity_score:     number;
  shannon_index:          number;
  species_detected:       number;
  declining_species_count:number;
  risk_level:             RiskLevel;
  risk_confidence:        number;
  sensors_online:         string;
  satellite_status:       string;
  alert_message:          string | null;
  shannon_trajectory:     ShannonDataPoint[];
  taxa_breakdown:         TaxaBreakdown[];
  priority_species:       SpeciesTrendRow[];
  radar_current:          number[];
  radar_baseline:         number[];
  radar_categories:       string[];
}

// ── Audio ────────────────────────────────────────────────────────────────────

export interface AudioClassificationResult {
  species:           string;
  confidence:        number;
  all_probabilities: Record<string, number>;
  processing_time_ms:number;
}

export interface MultiSpeciesAudioResult {
  detected_species:  Record<string, number>;
  total_segments:    number;
  unique_species:    number;
  processing_time_ms:number;
}

// ── Vision ───────────────────────────────────────────────────────────────────

export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface DetectionResult {
  species:       string;
  confidence:    number;
  bbox:          BoundingBox;
  species_class: string;
}

export interface WildlifeDetectionResult {
  detections:        DetectionResult[];
  detection_count:   number;
  image_url:         string;
  processing_time_ms:number;
}

// ── Risk ─────────────────────────────────────────────────────────────────────

export interface RiskFeatureInput {
  shannon_index:           number;
  species_richness:        number;
  evenness:                number;
  temperature:             number;
  humidity:                number;
  rainfall:                number;
  vegetation_index:        number;
  soil_moisture:           number;
  shannon_trend:           number;
  species_trend:           number;
  human_activity:          number;
  habitat_fragmentation:   number;
}

export interface ShapFactor {
  feature:    string;
  shap_value: number;
}

export interface RiskPredictionResult {
  risk_level:        RiskLevel;
  confidence:        number;
  probabilities:     Record<string, number>;
  top_shap_factors:  ShapFactor[];
  processing_time_ms:number;
}

// ── Conservation ─────────────────────────────────────────────────────────────

export interface ConservationQueryRequest {
  question:          string;
  zone?:             string;
  intervention_type?:string;
  budget_usd?:       number;
  timeline?:         string;
}

export interface ConservationQueryResult {
  recommendation:    string;
  priority:          "HIGH" | "MEDIUM" | "LOW";
  confidence:        number | null;
  processing_time_ms:number;
  used_llm:          boolean;
}

// ── Map ──────────────────────────────────────────────────────────────────────

export interface SensorMarker {
  id:                 string;
  lat:                number;
  lon:                number;
  sensor_type:        SensorType;
  zone:               string;
  status:             SensorStatus;
  last_reading:       string | null;  // ISO datetime string
  biodiversity_score: number | null;
}

export interface ZonePolygon {
  zone_id:       string;
  name:          string;
  risk_level:    RiskLevel;
  coordinates:   [number, number][];
  shannon_index: number;
  species_count: number;
}

export interface MapData {
  sensors: SensorMarker[];
  zones:   ZonePolygon[];
  center:  [number, number];
  zoom:    number;
}
