/** @type {import('next').NextConfig} */
const nextConfig = {
  // env: {
  //   PLEX_HOST: process.env.NEXT_PUBLIC_PLEX_HOST || '192.168.1.10',
  // },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
