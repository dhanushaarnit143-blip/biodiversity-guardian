import { useQuery } from '@tanstack/react-query';

// Mock static metrics — wire to real API later
export function useMetrics() {
  return useQuery({
    queryKey: ['metrics'],
    queryFn: async () => ({
      speciesMonitored: 24,
      biodiversityScore: 82.4,
      observations24h: 1248,
      threatsDetected: { moderate: 27, critical: 4 },
      bhi: 82,
    }),
    staleTime: 30_000,
  });
}
