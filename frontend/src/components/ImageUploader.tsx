'use client';

import { useState, useRef, useCallback } from 'react';
import { Upload, X, Image as ImageIcon, AlertCircle } from 'lucide-react';
import { analyzeImage } from '@/lib/api';
import { validateImageFile, formatFileSize } from '@/lib/utils';
import LoadingSpinner from './LoadingSpinner';
import type { ImageUploaderProps } from '@/types';

export default function ImageUploader({ onUploadComplete, onUploadError }: ImageUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = useCallback((selectedFile: File) => {
    // Validate file
    const validation = validateImageFile(selectedFile);
    if (!validation.valid) {
      setError(validation.error || 'Invalid file');
      return;
    }

    // Set file and create preview
    setFile(selectedFile);
    setError(null);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(selectedFile);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setProgress(0);
    setError(null);

    try {
      const result = await analyzeImage(file, (progress) => {
        setProgress(progress);
      });

      onUploadComplete(result);
      setUploading(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed';
      setError(errorMessage);
      onUploadError(errorMessage);
      setUploading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setProgress(0);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Upload Area */}
      {!file && (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-primary-500 transition-colors cursor-pointer bg-white"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            Upload an Image
          </h3>
          <p className="text-gray-500 mb-4">
            Drag and drop or click to select
          </p>
          <p className="text-sm text-gray-400">
            Supported: JPG, PNG, BMP (Max 10MB)
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/jpg,image/png,image/bmp"
            onChange={handleInputChange}
            className="hidden"
          />
        </div>
      )}

      {/* Preview and Upload */}
      {file && preview && !uploading && (
        <div className="card animate-slide-up">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center space-x-3">
              <ImageIcon className="w-5 h-5 text-primary-600" />
              <div>
                <p className="font-semibold text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
              </div>
            </div>
            <button
              onClick={handleReset}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Image Preview */}
          <div className="relative w-full h-64 bg-gray-100 rounded-lg overflow-hidden mb-4">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-full object-contain"
            />
          </div>

          {/* Actions */}
          <div className="flex space-x-3">
            <button onClick={handleUpload} className="btn-primary flex-1">
              Analyze Symmetry
            </button>
            <button onClick={handleReset} className="btn-secondary">
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Uploading State */}
      {uploading && (
        <div className="card animate-slide-up">
          <LoadingSpinner size="lg" text="Analyzing symmetry..." />
          <div className="mt-6">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="text-center text-sm text-gray-600 mt-2">
              {progress}% complete
            </p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-semibold text-red-800">Upload Error</p>
            <p className="text-sm text-red-600">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
}