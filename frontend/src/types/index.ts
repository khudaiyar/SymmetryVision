// API Types matching backend schemas

export interface SymmetryAxis {
  type: 'vertical' | 'horizontal' | 'main_diagonal' | 'anti_diagonal';
  angle: number;
  confidence: number;
  coordinates: {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

export interface SymmetryRegion {
  region_id: number;
  symmetry_type: 'radial' | 'reflective' | 'rotational';
  center_x: number;
  center_y: number;
  confidence: number;
}

export interface SymmetryAnalysisResult {
  analysis_id: string;
  original_image_url: string;
  processed_image_url: string;
  symmetry_score: number;
  detected_axes: SymmetryAxis[];
  detected_regions: SymmetryRegion[];
  has_vertical_symmetry: boolean;
  has_horizontal_symmetry: boolean;
  has_radial_symmetry: boolean;
  processing_time: number;
  timestamp: string;
}

export interface UploadResponse {
  message: string;
  file_id: string;
  filename: string;
  file_path: string;
}

export interface GalleryItem {
  analysis_id: string;
  thumbnail_url: string;
  symmetry_score: number;
  timestamp: string;
  has_vertical_symmetry: boolean;
  has_horizontal_symmetry: boolean;
}

export interface GalleryResponse {
  total: number;
  items: GalleryItem[];
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

// UI State Types
export interface UploadState {
  uploading: boolean;
  progress: number;
  error: string | null;
  success: boolean;
}

export interface AnalysisState {
  analyzing: boolean;
  result: SymmetryAnalysisResult | null;
  error: string | null;
}

// Component Props Types
export interface ImageUploaderProps {
  onUploadComplete: (result: SymmetryAnalysisResult) => void;
  onUploadError: (error: string) => void;
}

export interface SymmetryVisualizerProps {
  result: SymmetryAnalysisResult;
  showAxes?: boolean;
  showRegions?: boolean;
}

export interface GalleryCardProps {
  item: GalleryItem;
  onDelete?: (id: string) => void;
  onClick?: (id: string) => void;
}