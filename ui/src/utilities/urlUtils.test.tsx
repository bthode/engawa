import { isValidYoutubeUrl } from './urlUtils';
type TestDataItem = { [key: string]: string };
const testData: TestDataItem[] = [
  { 'Channel Id Url': 'https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw' },
  { 'Custom Url': 'https://www.youtube.com/c/YouTubeCreators' },
  { 'Legacy Username Url': 'https://www.youtube.com/user/YouTube' },
  { 'Channel Shortened Url': 'https://youtu.be/UC_x5XG1OV2P6uZZ5FSM9Ttw' },
  { 'Playlist Url': 'https://www.youtube.com/playlist?list=PL9tY0BWXOZFt8jZdf3GWBVtrhT4y7Y4Hb' },
  { 'Vanity Url': 'https://www.youtube.com/YouTubeCreators' },
  { 'Legacy Shortened Url': 'https://youtu.be/YouTube' },
  { 'At Channel URL': 'https://www.youtube.com/@channelname' },
  { 'Live Stream Url': 'https://www.youtube.com/watch?v=live_stream_id' },
  { 'Shortened Video Url': 'https://youtu.be/dQw4w9WgXcQ' },
];

describe('isValidYoutubeUrl', () => {
  testData.forEach((testItem) => {
    const urlDescription = Object.keys(testItem)[0];
    const url = Object.values(testItem)[0];
    it(`should validate the URL: ${urlDescription}`, () => {
      expect(isValidYoutubeUrl(url)).toBe(true);
    });
  });
});
