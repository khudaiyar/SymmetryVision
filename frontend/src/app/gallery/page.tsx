'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import GalleryCard from '@/components/GalleryCard';
import LoadingSpinner from '@/components/LoadingSpinner';
import { getGallery, deleteAnalysis } from '@/lib/api';
import { LayoutGrid, AlertCircle, Filter } from 'lucide-react';
import type { GalleryItem } from '@/types';

export default function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<'timestamp' | 'score'>('timestamp');
  const router = useRouter();

  useEffect(() => {
    loadGallery();
  }, [sortBy]);

  const loadGallery = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getGallery(50, 0, sortBy);
      setItems(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load gallery');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteAnalysis(id);
      setItems(items.filter(item => item.analysis_id !== id));
    } catch (err) {
      alert('Failed to delete analysis');
    }
  };

  const handleClick = (id: string) => {
    router.push(`/results/${id}`);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-12">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <LayoutGrid className="w-10 h-10 text-primary-600" />
              <h1 className="text-4xl font-bold text-gray-900">Gallery</h1>
            </div>
            <p className="text-lg text-gray-600">
              Browse your symmetry analysis history
            </p>
          </div>

          {/* Sort Controls */}
          <div className="flex items-center space-x-2">
            <Filter className="w-5 h-5 text-gray-500" />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'timestamp' | 'score')}
              className="input-field py-2"
            >
              <option value="timestamp">Recent First</option>
              <option value="score">Highest Score</option>
            </select>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading gallery..." />
        </div>
      )}

      {/* Error State */}
      {error && !loading && (
        <div className="card bg-red-50 border-red-200 border">
          <div className="flex items-center space-x-3">
            <AlertCircle className="w-6 h-6 text-red-600" />
            <div>
              <p className="font-semibold text-red-800">Error Loading Gallery</p>
              <p className="text-sm text-red-600">{error}</p>
            </div>
          </div>
          <button onClick={loadGallery} className="btn-primary mt-4">
            Try Again
          </button>
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && items.length === 0 && (
        <div className="text-center py-20">
          <LayoutGrid className="w-20 h-20 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-700 mb-2">
            No Analyses Yet
          </h2>
          <p className="text-gray-500 mb-6">
            Upload your first image to start building your gallery
          </p>
          <button
            onClick={() => router.push('/upload')}
            className="btn-primary"
          >
            Upload Image
          </button>
        </div>
      )}

      {/* Gallery Grid */}
      {!loading && !error && items.length > 0 && (
        <>
          <div className="mb-6 text-sm text-gray-600">
            Showing {items.length} {items.length === 1 ? 'analysis' : 'analyses'}
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-fade-in">
            {items.map((item) => (
              <GalleryCard
                key={item.analysis_id}
                item={item}
                onDelete={handleDelete}
                onClick={handleClick}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}