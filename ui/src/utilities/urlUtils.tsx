export const isValidYoutubeUrl = (url: string): boolean => {
  let urlPattern =
    /^(https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:c\/|user\/|playlist\?list=|@([\w-]+)|channel\/|)?|youtu\.be\/)([\w-]+)/i;
  return urlPattern.test(url);
};
