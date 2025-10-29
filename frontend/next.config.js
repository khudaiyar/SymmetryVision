/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove this line: output: 'export',
  reactStrictMode: true,
  swcMinify: true,
  
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
  
  images: {
    formats: ['image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
    imageSizes: [16, 32, 48, 64, 96],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'symmetryvision-1.onrender.com',
        pathname: '/uploads/**',
      },
      {
        protocol: 'https',
        hostname: 'symmetryvision-1.onrender.com',
        pathname: '/results/**',
      },
    ],
  },
  
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://symmetryvision-1.onrender.com',
  },
}

module.exports = nextConfig