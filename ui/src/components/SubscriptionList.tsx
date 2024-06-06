import dynamic from 'next/dynamic';

const App = dynamic(() => import('./SubscriptionListFetcher'), { ssr: false });

export default App;
