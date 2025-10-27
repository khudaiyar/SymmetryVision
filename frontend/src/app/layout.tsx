import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import dynamic from 'next/dynamic';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

// Lazy load animated background
const AnimatedBackground = dynamic(() => import('@/components/AnimatedBackground'), {
  ssr: false,
});

export const metadata: Metadata = {
  title: 'SymmetryVision - AI Image Symmetry Detection',
  description: 'AI-powered web application for detecting and analyzing image symmetry using deep learning and computer vision',
  keywords: 'symmetry detection, image analysis, AI, computer vision, deep learning',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        <AnimatedBackground />
        <Header />
        <main className="flex-1 py-8 px-4 relative z-10">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}