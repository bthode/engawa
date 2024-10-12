export type VideoStatus =
  | 'Pending'
  | 'In Progress'
  | 'Failed'
  | 'Deleted'
  | 'Complete'
  | 'Excluded'
  | 'Filtered'
  | 'Pending Download';

export interface Video {
  description: string;
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
