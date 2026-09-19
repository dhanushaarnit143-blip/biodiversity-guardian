export interface Species {
  id: string;
  name: string;
  scientificName: string;
  confidence: number;
  category: 'Mammalia' | 'Aves' | 'Amphibia' | 'Reptilia';
  zone: string;
  imageUrl?: string;
  riskLevel: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
}

export interface Zone {
  id: string;
  name: string;
  lat: number;
  lon: number;
  riskLevel: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  speciesCount: number;
}

export interface TelemetryMetrics {
  speciesMonitored: number;
  biodiversityScore: number;
  observations24h: number;
  threatsDetected: { moderate: number; critical: number };
  bhi: number;
}
