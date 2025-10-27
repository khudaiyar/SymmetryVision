'use client';

import { Trash2, ExternalLink } from 'lucide-react';
import { getImageUrl, formatScore, getScoreBadgeClass, formatRelativeTime } from '@/lib/utils';
import type { GalleryCardProps } from '@/types';

export default function GalleryCard({ item, onDelete, onClick }: GalleryCardProps) {
  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onDelete && confirm('Are you sure you want to delete this analysis?')) {
      onDelete(item.analysis_id);
    }
  };

  const handleClick = () => {
    if (onClick) {
      onClick(item.analysis_id);
    }
  };

  return (
    <div
      className="card group cursor-pointer hover:shadow-xl transition-all duration-300 overflow-hidden"
      onClick={handleClick}
    >
      {/* Thumbnail */}
      <div className="relative w-full h-48 bg-gray-100 rounded-lg overflow-hidden mb-4">
        <img
          src={getImageUrl(item.thumbnail_url)}
          alt={`Analysis ${item.analysis_id}`}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
        />

        {/* Score Overlay */}
        <div className="absolute top-3 right-3">
          <div className={`px-3 py-1 rounded-full text-sm font-bold backdrop-blur-sm ${getScoreBadgeClass(item.symmetry_score)}`}>
            {formatScore(item.symmetry_score)}
          </div>
        </div>

        {/* Hover Overlay */}
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
          <ExternalLink className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        </div>
      </div>

      {/* Info */}
      <div className="space-y-3">
        {/* Symmetry Badges */}
        <div className="flex flex-wrap gap-2">
          {item.has_vertical_symmetry && (
            <span className="badge badge-info text-xs">Vertical</span>
          )}
          {item.has_horizontal_symmetry && (
            <span className="badge badge-success text-xs">Horizontal</span>
          )}
          {!item.has_vertical_symmetry && !item.has_horizontal_symmetry && (
            <span className="badge bg-gray-100 text-gray-600 text-xs">No axes</span>
          )}
        </div>

        {/* Timestamp and Actions */}
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">
            {formatRelativeTime(item.timestamp)}
          </span>

          {onDelete && (
            <button
              onClick={handleDelete}
              className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}