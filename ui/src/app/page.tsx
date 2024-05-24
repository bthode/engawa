import Image from 'next/image';
import YoutubeLink from './youtube/YoutubeLink';
import VideoCard from '@/app/youtube/VideoCard';
import Navigation from './navigation';

export default function Home() {
  return (
    <Navigation>
      <div>Hello Home Page</div>
    </Navigation>
  );
}
