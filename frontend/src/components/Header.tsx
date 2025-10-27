import Link from 'next/link';
import Image from 'next/image';
import { LayoutGrid } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="relative w-20 h-20">
              <Image
                src="/logo.png"
                alt="SymmetryVision Logo"
                fill
                className="object-contain"
                priority
              />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">
                SymmetryVision
              </h1>
              <p className="text-xs text-gray-500">AI-Powered Detection</p>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-1">
            <Link
              href="/upload"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors group"
            >
              <Image
                src="/logo.png"
                alt="Upload"
                width={50}
                height={20}
                className="opacity-60 group-hover:opacity-100"
              />
              <span className="font-medium text-gray-700 group-hover:text-primary-600">
                Upload
              </span>
            </Link>

            <Link
              href="/gallery"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors group"
            >
              <LayoutGrid className="w-5 h-5 text-gray-600 group-hover:text-primary-600" />
              <span className="font-medium text-gray-700 group-hover:text-primary-600">
                Gallery
              </span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}