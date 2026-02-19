import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '@api/client';

interface ProbeRequest {
  brand: string;
  keywords: string[];
  frequency: string;
  llm_engines: string[];
}

export const useProbes = () => {
  const queryClient = useQueryClient();

  const listProbes = useQuery({
    queryKey: ['probes'],
    queryFn: async () => {
      const response = await apiClient.get('/probes');
      return response.data;
    }
  });

  const createProbe = useMutation({
    mutationFn: async (data: ProbeRequest) => {
      const response = await apiClient.post('/probes/create', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['probes'] });
    }
  });

  const getProbeResults = (jobId: string, timeframe: string = '30d') => {
    return useQuery({
      queryKey: ['probe-results', jobId, timeframe],
      queryFn: async () => {
        const response = await apiClient.get(`/probes/${jobId}/results`, {
          params: { timeframe }
        });
        return response.data;
      },
      enabled: !!jobId
    });
  };

  const executeProbe = useMutation({
    mutationFn: async (jobId: string) => {
      const response = await apiClient.post(`/probes/${jobId}/execute`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['probe-results'] });
    }
  });

  return {
    listProbes,
    createProbe,
    getProbeResults,
    executeProbe
  };
};
