import { type ClassValue, clsx } from 'clsx';

/**
 * Merge class names with Tailwind
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

/**
 * Format file size
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

/**
 * Format date relative to now
 */
export function formatRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  if (diffInSeconds < 60) return 'just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
  
  return date.toLocaleDateString();
}

/**
 * Format symmetry score
 */
export function formatScore(score: number): string {
  return score.toFixed(1);
}

/**
 * Get score color class
 */
export function getScoreColor(score: number): string {
  if (score >= 90) return 'text-green-600';
  if (score >= 75) return 'text-blue-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
}

/**
 * Get score badge class
 */
export function getScoreBadgeClass(score: number): string {
  if (score >= 90) return 'bg-green-100 text-green-800';
  if (score >= 75) return 'bg-blue-100 text-blue-800';
  if (score >= 60) return 'bg-yellow-100 text-yellow-800';
  if (score >= 40) return 'bg-orange-100 text-orange-800';
  return 'bg-red-100 text-red-800';
}

/**
 * Get assessment text
 */
export function getAssessmentText(score: number): string {
  if (score >= 90) return 'Highly Symmetric';
  if (score >= 75) return 'Strongly Symmetric';
  if (score >= 60) return 'Moderately Symmetric';
  if (score >= 40) return 'Somewhat Symmetric';
  return 'Low Symmetry';
}

/**
 * Validate image file
 */
export function validateImageFile(file: File): { valid: boolean; error?: string } {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
  const maxSize = 10 * 1024 * 1024; // 10MB
  
  if (!allowedTypes.includes(file.type)) {
    return {
      valid: false,
      error: 'Invalid file type. Please upload a JPG, PNG, or BMP image.',
    };
  }
  
  if (file.size > maxSize) {
    return {
      valid: false,
      error: `File too large. Maximum size is ${formatFileSize(maxSize)}.`,
    };
  }
  
  return { valid: true };
}

/**
 * Download file
 */
export function downloadFile(url: string, filename: string): void {
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Copy to clipboard
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error('Failed to copy:', error);
    return false;
  }
}

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  
  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Format processing time
 */
export function formatProcessingTime(seconds: number): string {
  if (seconds < 1) return `${(seconds * 1000).toFixed(0)}ms`;
  return `${seconds.toFixed(2)}s`;
}

/**
 * Generate random color for symmetry axis
 */
export function getAxisColor(type: string): string {
  const colors: Record<string, string> = {
    vertical: '#ef4444',
    horizontal: '#3b82f6',
    main_diagonal: '#10b981',
    anti_diagonal: '#f59e0b',
  };
  return colors[type] || '#8b5cf6';
}

/**
 * Build full image URL from path
 */
export function getImageUrl(path: string): string {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  if (!path) return '';
  
  // If path already includes http/https, return as is
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  
  // If path starts with /, use it directly
  if (path.startsWith('/')) {
    return `${API_BASE_URL}${path}`;
  }
  
  // Otherwise, add leading slash
  return `${API_BASE_URL}/${path}`;
}