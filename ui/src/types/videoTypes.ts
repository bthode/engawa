export type VideoStatus = 'Pending' | 'In Progress' | 'Failed' | 'Deleted' | 'Complete' | 'Excluded' | 'Filtered';

export interface Video {
  id: number;
  duration: number;
  title: string;
  published: string;
  video_id: string;
  link: string;
  author: string;
  subscription_id: number;
  thumbnail_url: string;
  status: VideoStatus;
}
