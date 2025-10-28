#!/bin/bash
set -e  # Exit on error

echo "🏗️  Building SymmetryVision..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm ci  # Use ci for cleaner installs
npm run build
cd ..

echo "✅ Build complete!"