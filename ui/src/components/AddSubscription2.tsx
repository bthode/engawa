import dynamic from 'next/dynamic';

const YoutubeCardFetcher = dynamic(() => import('./AddSubscriptionForm2'), { ssr: false });

const Card2 = () => {
  return <YoutubeCardFetcher />;
};

export default Card2;
