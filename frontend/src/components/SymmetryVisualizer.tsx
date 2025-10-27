'use client';

import { useState } from 'react';
import { Download, Eye, EyeOff, Clock, Target } from 'lucide-react';
import { getImageUrl, getAxisColor, formatScore, formatProcessingTime, getScoreBadgeClass, getAssessmentText } from '@/lib/utils';
import type { SymmetryVisualizerProps } from '@/types';

export default function SymmetryVisualizer({ result, showAxes = true, showRegions = true }: SymmetryVisualizerProps) {
  const [viewMode, setViewMode] = useState<'original' | 'processed'>('processed');
  const [axesVisible, setAxesVisible] = useState(showAxes);

  const imageUrl = viewMode === 'original'
    ? getImageUrl(result.original_image_url)
    : getImageUrl(result.processed_image_url);

  const downloadImage = () => {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `symmetry_analysis_${result.analysis_id}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Image Display */}
        <div className="lg:col-span-2">
          <div className="card">
            {/* Controls */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex space-x-2">
                <button
                  onClick={() => setViewMode('processed')}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    viewMode === 'processed'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Analyzed
                </button>
                <button
                  onClick={() => setViewMode('original')}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    viewMode === 'original'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Original
                </button>
              </div>

              <div className="flex space-x-2">
                {viewMode === 'processed' && (
                  <button
                    onClick={() => setAxesVisible(!axesVisible)}
                    className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center space-x-2 transition-colors"
                  >
                    {axesVisible ? (
                      <Eye className="w-4 h-4" />
                    ) : (
                      <EyeOff className="w-4 h-4" />
                    )}
                    <span className="text-sm font-medium">Axes</span>
                  </button>
                )}
                <button
                  onClick={downloadImage}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg flex items-center space-x-2 transition-colors"
                >
                  <Download className="w-4 h-4" />
                  <span className="text-sm font-medium">Download</span>
                </button>
              </div>
            </div>

            {/* Image */}
            <div className="relative w-full bg-gray-100 rounded-lg overflow-hidden" style={{ minHeight: '400px' }}>
              <img
                src={imageUrl}
                alt="Symmetry Analysis"
                className="w-full h-full object-contain"
              />
            </div>
          </div>
        </div>

        {/* Analysis Details */}
        <div className="space-y-6">
          {/* Symmetry Score */}
          <div className="card">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-gray-900">Symmetry Score</h3>
              <Target className="w-5 h-5 text-primary-600" />
            </div>
            <div className="text-center py-4">
              <div className="text-5xl font-bold gradient-text mb-2">
                {formatScore(result.symmetry_score)}
              </div>
              <div className={`inline-block px-4 py-1 rounded-full text-sm font-medium ${getScoreBadgeClass(result.symmetry_score)}`}>
                {getAssessmentText(result.symmetry_score)}
              </div>
            </div>
          </div>

          {/* Detected Symmetries */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Detected Symmetries</h3>
            <div className="space-y-3">
              {result.detected_axes.length === 0 ? (
                <p className="text-sm text-gray-500 text-center py-4">
                  No symmetry axes detected
                </p>
              ) : (
                result.detected_axes.map((axis, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex items-center space-x-3">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: getAxisColor(axis.type) }}
                      />
                      <div>
                        <p className="text-sm font-medium text-gray-900 capitalize">
                          {axis.type.replace('_', ' ')}
                        </p>
                        <p className="text-xs text-gray-500">
                          {axis.angle}°
                        </p>
                      </div>
                    </div>
                    <span className="text-sm font-semibold text-gray-700">
                      {(axis.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Symmetry Types */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Symmetry Types</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-2 rounded">
                <span className="text-sm text-gray-700">Vertical</span>
                <span className={`badge ${result.has_vertical_symmetry ? 'badge-success' : 'bg-gray-100 text-gray-500'}`}>
                  {result.has_vertical_symmetry ? 'Detected' : 'None'}
                </span>
              </div>
              <div className="flex items-center justify-between p-2 rounded">
                <span className="text-sm text-gray-700">Horizontal</span>
                <span className={`badge ${result.has_horizontal_symmetry ? 'badge-success' : 'bg-gray-100 text-gray-500'}`}>
                  {result.has_horizontal_symmetry ? 'Detected' : 'None'}
                </span>
              </div>
              <div className="flex items-center justify-between p-2 rounded">
                <span className="text-sm text-gray-700">Radial</span>
                <span className={`badge ${result.has_radial_symmetry ? 'badge-success' : 'bg-gray-100 text-gray-500'}`}>
                  {result.has_radial_symmetry ? 'Detected' : 'None'}
                </span>
              </div>
            </div>
          </div>

          {/* Processing Info */}
          <div className="card">
            <div className="flex items-center space-x-2 mb-3">
              <Clock className="w-5 h-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">Processing Info</h3>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Processing Time:</span>
                <span className="font-medium text-gray-900">
                  {formatProcessingTime(result.processing_time)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Analysis ID:</span>
                <span className="font-mono text-xs text-gray-700">
                  {result.analysis_id.substring(0, 8)}...
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Regions Found:</span>
                <span className="font-medium text-gray-900">
                  {result.detected_regions.length}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}