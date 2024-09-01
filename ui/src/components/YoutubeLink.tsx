import dynamic from 'next/dynamic';

const App = dynamic(() => import('./YouTubeLinkFetcher'), { ssr: false });

export default App;
