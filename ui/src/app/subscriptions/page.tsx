import React from 'react';
import Navigation from '../navigation';
import VideoCard from '@components/VideoCard';
import YoutubeLink from '@components/YoutubeLink';

const Subscriptions: React.FC = () => {
  return (
    <Navigation>
      <VideoCard />
      <YoutubeLink />
    </Navigation>
  );
};

export default Subscriptions;
