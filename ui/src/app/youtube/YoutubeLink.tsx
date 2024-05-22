import dynamic from 'next/dynamic';

const App = dynamic(() => import('./YoutubeLinkFetcher'), { ssr: false });

export default App;
