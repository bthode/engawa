import dynamic from 'next/dynamic';

const App = dynamic(() => import('./AddSubscriptionForm'), { ssr: false });

export default App;
