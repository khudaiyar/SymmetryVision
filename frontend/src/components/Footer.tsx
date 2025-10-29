import { Github, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              About SymmetryVision
            </h3>
            <p className="text-sm text-gray-600">
            A sophisticated AI web application for detecting and analyzing image symmetry with precision. 
            Powered by FastAPI and Next.js, it combines advanced deep learning and computer vision for seamless, high-performance image analysis.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Quick Links
            </h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>
                <a href="/upload" className="hover:text-primary-600 transition-colors">
                  Upload Image
                </a>
              </li>
              <li>
                <a href="/gallery" className="hover:text-primary-600 transition-colors">
                  View Gallery
                </a>
              </li>
              <li>
                <a href="http://localhost:8000/api/docs" target="_blank" rel="noopener noreferrer" className="hover:text-primary-600 transition-colors">
                  API Documentation
                </a>
              </li>
            </ul>
          </div>

          {/* Tech Stack */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Technology
            </h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• FastAPI (Python Backend)</li>
              <li>• Next.js (React Frontend)</li>
              <li>• TensorFlow / PyTorch</li>
              <li>• OpenCV</li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-sm text-gray-500 flex items-center">
              Made with <Heart className="w-4 h-4 mx-1 text-red-500" /> built with modern web technologies.
            </p>

            <div className="flex items-center space-x-4">
              <a
                href="https://github.com/khudaiyar"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-500 hover:text-gray-900 transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
            </div>

            <p className="text-sm text-gray-500">
              © {new Date().getFullYear()} SymmetryVision by Hudayyar. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}