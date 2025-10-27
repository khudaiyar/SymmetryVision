'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import SymmetryVisualizer from '@/components/SymmetryVisualizer';
import LoadingSpinner from '@/components/LoadingSpinner';
import { getAnalysis } from '@/lib/api';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import type { SymmetryAnalysisResult } from '@/types';

export default function ResultsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [result, setResult] = useState<SymmetryAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadAnalysis();
    }
  }, [id]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAnalysis(id);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Back Button */}
      <button
        onClick={() => router.push('/gallery')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Gallery</span>
      </button>

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading analysis..." />
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="card bg-red-50 border-red-200 border">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-6 h-6 text-red-600" />
            <div>
              <p className="font-semibold text-red-800">Error Loading Analysis</p>
              <p className="text-sm text-red-600">{error}</p>
            </div>
          </div>
          <div className="mt-4 flex space-x-3">
            <button onClick={loadAnalysis} className="btn-primary">
              Try Again
            </button>
            <button onClick={() => router.push('/gallery')} className="btn-secondary">
              Back to Gallery
            </button>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !loading && !error && (
        <div className="animate-fade-in">
          <SymmetryVisualizer result={result} />
        </div>
      )}
    </div>
  );
}