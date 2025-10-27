import axios, { AxiosError } from 'axios';
import type {
  SymmetryAnalysisResult,
  UploadResponse,
  GalleryResponse,
  ErrorResponse
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

// Create axios instance
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}${API_PREFIX}`,
  timeout: 60000, // 60 seconds for image processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ErrorResponse>) => {
    const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
    return Promise.reject(new Error(errorMessage));
  }
);

// API Functions

/**
 * Upload and analyze an image
 */
export const analyzeImage = async (
  file: File,
  onProgress?: (progress: number) => void
): Promise<SymmetryAnalysisResult> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<SymmetryAnalysisResult>('/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total && onProgress) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentCompleted);
      }
    },
  });

  return response.data;
};

/**
 * Upload image without analyzing
 */
export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<UploadResponse>('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Get analysis by ID
 */
export const getAnalysis = async (fileId: string): Promise<SymmetryAnalysisResult> => {
  const response = await apiClient.get<SymmetryAnalysisResult>(`/analyze/${fileId}`);
  return response.data;
};

/**
 * Get gallery of all analyses
 */
export const getGallery = async (
  limit: number = 20,
  offset: number = 0,
  sortBy: 'timestamp' | 'score' = 'timestamp'
): Promise<GalleryResponse> => {
  const response = await apiClient.get<GalleryResponse>('/gallery', {
    params: { limit, offset, sort_by: sortBy },
  });
  return response.data;
};

/**
 * Delete analysis
 */
export const deleteAnalysis = async (fileId: string): Promise<void> => {
  await apiClient.delete(`/gallery/${fileId}`);
};

/**
 * Get gallery statistics
 */
export const getGalleryStats = async (): Promise<{
  total_analyses: number;
  average_score: number;
  highest_score: number;
  lowest_score: number;
  storage_used_mb: number;
}> => {
  const response = await apiClient.get('/gallery/stats');
  return response.data;
};

/**
 * Get analysis summary
 */
export const getAnalysisSummary = async (fileId: string): Promise<{
  file_id: string;
  summary: {
    overall_assessment: string;
    dominant_symmetry: string;
    symmetry_count: number;
    confidence_level: string;
  };
  details: SymmetryAnalysisResult;
}> => {
  const response = await apiClient.get(`/analyze/summary/${fileId}`);
  return response.data;
};

/**
 * Build full image URL
 */
export const getImageUrl = (path: string): string => {
  if (path.startsWith('http')) return path;
  return `${API_BASE_URL}${path}`;
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await apiClient.get('/upload/health');
  return response.data;
};

export default apiClient;