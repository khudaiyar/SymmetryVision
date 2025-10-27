'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ImageUploader from '@/components/ImageUploader';
import SymmetryVisualizer from '@/components/SymmetryVisualizer';
import { CheckCircle, Upload } from 'lucide-react';
import type { SymmetryAnalysisResult } from '@/types';

export default function UploadPage() {
  const [result, setResult] = useState<SymmetryAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleUploadComplete = (analysisResult: SymmetryAnalysisResult) => {
    setResult(analysisResult);
    setError(null);
  };

  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
    setResult(null);
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-block p-4 bg-primary-100 rounded-full mb-4">
          <Upload className="w-12 h-12 text-primary-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Upload & Analyze
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Upload your image to detect symmetry axes and calculate symmetry scores using AI
        </p>
      </div>

      {/* Upload Section */}
      {!result && (
        <div className="animate-fade-in">
          <ImageUploader
            onUploadComplete={handleUploadComplete}
            onUploadError={handleUploadError}
          />
        </div>
      )}

      {/* Success Message */}
      {result && !error && (
        <div className="mb-8 animate-slide-up">
          <div className="card bg-green-50 border-green-200 border">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-6 h-6 text-green-600" />
              <div>
                <p className="font-semibold text-green-800">Analysis Complete!</p>
                <p className="text-sm text-green-600">
                  Your image has been successfully analyzed
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="animate-fade-in">
          <SymmetryVisualizer result={result} />

          {/* Actions */}
          <div className="mt-8 flex justify-center space-x-4">
            <button
              onClick={handleReset}
              className="btn-secondary"
            >
              Analyze Another Image
            </button>
            <button
              onClick={() => router.push('/gallery')}
              className="btn-primary"
            >
              View Gallery
            </button>
          </div>
        </div>
      )}
    </div>
  );
}