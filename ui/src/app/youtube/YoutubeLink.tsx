import dynamic from 'next/dynamic';

const App = dynamic(
  () => import('./YoutubeLinkFetcher'), // replace with the path to your component
  { ssr: false }, // This will disable server-side rendering (SSR)
);

export default App;
