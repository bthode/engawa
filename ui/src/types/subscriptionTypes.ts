export type Subscription = {
  id: number;
  title: string;
  url: string;
  description?: string;
  rss_feed_url?: string;
  image?: string;
};

// export enum VideoStatus {
//   PENDING = 'Pending',
//   IN_PROGRESS = 'In Progress',
//   FAILED = 'Failed',
//   DELETED = 'Deleted',
//   COMPLETE = 'Complete',
//   EXCLUDED = 'Excluded',
// }

// export enum Retention {
//   DATE_BASED = 'Date Based',
//   COUNT_BASED = 'Count Based',
// }

// export type Policy = {
//   id: number | null;
//   subscription_id: number | null;
//   type: Retention;
//   days_to_retain: number;
//   subscription: Subscription;
// };

// export type Video = {
//   id: number | null;
//   subscription_id: number | null;
//   url: string | null;
//   title: string | null;
//   status: VideoStatus | null;
//   subscription: Subscription;
//   created_at: Date | null;
//   download_attempts: number | null;
//   saved_path: string | null;
// };
