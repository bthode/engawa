import dynamic from 'next/dynamic';

const App = dynamic(() => import('./YoutubeCardFetcher'), { ssr: false });

export default App;
