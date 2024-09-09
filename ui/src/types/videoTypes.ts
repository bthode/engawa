export type Video = {
  id: number;
  title: string;
  published: string;
  video_id: string;
  link: string;
  author: string;
  subscription_id: number;
  thumbnail_url: string;
  status: 'Pending' | 'In Progress' | 'Failed' | 'Deleted' | 'Complete' | 'Excluded';
};

export type VideoStatus = 'Pending' | 'In Progress' | 'Failed' | 'Deleted' | 'Complete' | 'Excluded';