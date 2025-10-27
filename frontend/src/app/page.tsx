import Link from 'next/link';
import Image from 'next/image';
import { ArrowRight, Zap, Eye, BarChart3 } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <section className="text-center py-16 animate-fade-in">
        <div className="inline-block mb-4">
          <div className="relative w-32 h-32 mx-auto animate-pulse-slow">
            <Image
              src="/logo.png"
              alt="SymmetryVision Logo"
              fill
              className="object-contain"
              priority
            />
          </div>
        </div>
        <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-6">
          SymmetryVision
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
        AI that sees symmetry like never before. Instantly detect vertical, horizontal, diagonal, and radial patterns through advanced deep learning and computer vision.
        </p>
        <div className="flex justify-center space-x-4">
          <Link href="/upload" className="btn-primary inline-flex items-center space-x-2">
            <span>Get Started</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link href="/gallery" className="btn-secondary inline-flex items-center space-x-2">
            <span>View Gallery</span>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Key Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Feature 1 */}
          <div className="card text-center group hover:shadow-xl transition-all">
            <div className="inline-block p-4 bg-primary-100 rounded-full mb-4 group-hover:bg-primary-200 transition-colors">
              <div className="relative w-8 h-8">
                <Image
                  src="/logo.png"
                  alt="Multi-Axis Detection"
                  fill
                  className="object-contain"
                />
              </div>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Multi-Axis Detection
            </h3>
            <p className="text-sm text-gray-600">
              Detect vertical, horizontal, diagonal, and radial symmetry axes
            </p>
          </div>

          {/* Feature 2 */}
          <div className="card text-center group hover:shadow-xl transition-all">
            <div className="inline-block p-4 bg-secondary-100 rounded-full mb-4 group-hover:bg-secondary-200 transition-colors">
              <Zap className="w-8 h-8 text-secondary-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Fast Processing
            </h3>
            <p className="text-sm text-gray-600">
              Powered by TensorFlow and OpenCV for real-time analysis
            </p>
          </div>

          {/* Feature 3 */}
          <div className="card text-center group hover:shadow-xl transition-all">
            <div className="inline-block p-4 bg-green-100 rounded-full mb-4 group-hover:bg-green-200 transition-colors">
              <Eye className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Visual Results
            </h3>
            <p className="text-sm text-gray-600">
              Clear visualization with highlighted symmetry axes and regions
            </p>
          </div>

          {/* Feature 4 */}
          <div className="card text-center group hover:shadow-xl transition-all">
            <div className="inline-block p-4 bg-yellow-100 rounded-full mb-4 group-hover:bg-yellow-200 transition-colors">
              <BarChart3 className="w-8 h-8 text-yellow-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Symmetry Score
            </h3>
            <p className="text-sm text-gray-600">
              Quantitative scoring (0-100) for overall image symmetry
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gradient-to-br from-primary-50 to-secondary-50 rounded-3xl px-8">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              1
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Image</h3>
            <p className="text-sm text-gray-600">
              Upload any JPG, PNG, or BMP image up to 10MB
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              2
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Analysis</h3>
            <p className="text-sm text-gray-600">
              Our AI detects and analyzes all symmetry types
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-primary-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              3
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Get Results</h3>
            <p className="text-sm text-gray-600">
              View detailed analysis with visual symmetry axes
            </p>
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-16">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Built With Modern Technology
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
          <div className="card text-center">
            <p className="font-semibold text-gray-900">FastAPI</p>
            <p className="text-xs text-gray-500">Python Backend</p>
          </div>
          <div className="card text-center">
            <p className="font-semibold text-gray-900">Next.js</p>
            <p className="text-xs text-gray-500">React Framework</p>
          </div>
          <div className="card text-center">
            <p className="font-semibold text-gray-900">TensorFlow</p>
            <p className="text-xs text-gray-500">Deep Learning</p>
          </div>
          <div className="card text-center">
            <p className="font-semibold text-gray-900">OpenCV</p>
            <p className="text-xs text-gray-500">Computer Vision</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="text-center py-16">
        <div className="card max-w-2xl mx-auto bg-gradient-to-br from-primary-600 to-secondary-600 text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Analyze?</h2>
          <p className="text-lg mb-6 opacity-90">
            Start detecting symmetry in your images with AI-powered precision
          </p>
          <Link href="/upload" className="inline-flex items-center space-x-2 bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
            <span>Upload Image Now</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
}