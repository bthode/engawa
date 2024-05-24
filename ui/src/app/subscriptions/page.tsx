import React from 'react';
import Navigation from '../navigation';
import VideoCard from '../youtube/VideoCard';
import YoutubeLink from '../youtube/YoutubeLink';

const Subscriptions: React.FC = () => {
  return (
    <Navigation>
      <VideoCard />
      <YoutubeLink />
    </Navigation>
  );
};

export default Subscriptions;
