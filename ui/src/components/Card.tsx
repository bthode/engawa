import dynamic from 'next/dynamic';

const YoutubeCardFetcher = dynamic(() => import('./YoutubeCardFetcher'), { ssr: false });

const Card = () => {
  return <YoutubeCardFetcher />;
};

export default Card;
