import { Directory } from '@/types/plexTypes';
import { Subscription } from '@/types/subscriptionTypes';
import { Video } from '@/types/videoTypes';

export const mockSubscription: Subscription = {
  error_state: null,
  id: 1,
  last_updated: '2024-10-08T14:01:37.745954',
  title: 'E;R - YouTube',
  url: 'https://www.youtube.com/@esemicolonr',
  description:
    'I shit where you eat.And stream (most) every Mon at 7 EST (always on time) FAQ:But THE VIDEOS, MANAre still being made. The streams do not--or rarely--eat in...',
  image: 'https://i.ytimg.com/vi/bilJ8RcS7Pc/maxresdefault.jpg',
  rss_feed_url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UCS67mNnpfnHsU3IQYNHLToA',
  type: 'Channel',
};

export const mockVideos: Video[] = [
  {
    description:
      'Hanging with my phasmobros. With a TTwiSt.  \n\nKool Kids: https://www.youtube.com/channel/UC4BZtFgtCuHUt0p8J-XENiA/join\n\nhttps://streamlabs.com/esemicolonr/tip\nSteamlabs TTS Commands:\n!phasmo (only one to be output thru my mic in-game; the rest output as normal) \nE;R = !e;r\nStrawnerd = !nerd\nTyrone = !ty \nUncle Ruckus = !ruckus \nShaniqua = !shaniqua\nKorra = !korra\nChloe = !chloe\nAmelie = !sis\nVel = !vel \nPamu = !pamu\nHerbie = !herb\nSenator Armstrong = !arm\nRakesh = !loo\nRinoa = !rin',
    id: 33,
    published: '2024-10-07T22:07:11',
    status: 'Failed',
    thumbnail_url: 'https://i4.ytimg.com/vi/sU_1XforOp0/hqdefault.jpg',
    video_id: 'sU_1XforOp0',
    duration: 600,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=sU_1XforOp0',
    subscription_id: 1,
    title: "Bustin' (G)hos(ts)",
  },
  {
    description:
      'Everybody do the dinosaur. \n\nKool Kids: https://www.youtube.com/channel/UC4BZtFgtCuHUt0p8J-XENiA/join\n\nhttps://streamlabs.com/esemicolonr/tip\n\nSteamlabs TTS Commands \n\nE;R = !e;r\nStrawnerd = !nerd\nTyrone = !ty \nUncle Ruckus = !ruckus \nShaniqua = !shaniqua\nKorra = !korra\nChloe = !chloe\nAmelie = !sis\nVel = !vel \nPamu = !pamu\nHerbie = !herb\nSenator Armstrong = !arm\nRakesh = !loo\nRinoa = !rin',
    id: 31,
    published: '2024-09-30T22:03:59',
    status: 'Filtered',
    thumbnail_url: 'https://i.ytimg.com/vi/bilJ8RcS7Pc/maxresdefault.jpg',
    video_id: 'bilJ8RcS7Pc',
    duration: 13489,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=bilJ8RcS7Pc',
    subscription_id: 1,
    title: 'Jurass Is Mine 3',
  },
  {
    description:
      'I love Netflix and the eerie, statuesque composure with which they can hold a thing against my temple. \n\nPurplE;R model by https://x.com/beams_n\n\nSocials: \nhttps://twitter.com/EsemicolonR\n\nSupport: \nKool Kids: https://www.youtube.com/channel/UC4BZtFgtCuHUt0p8J-XENiA/join\nhttps://www.patreon.com/esemicolonr\nhttps://paypal.me/esemicolonr?country...',
    id: 1,
    published: '2024-09-27T23:06:48',
    status: 'Filtered',
    thumbnail_url: 'https://i.ytimg.com/vi_webp/gxqTkgoRR-Y/maxresdefault.webp',
    video_id: 'gxqTkgoRR-Y',
    duration: 3565,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=gxqTkgoRR-Y',
    subscription_id: 1,
    title: 'Avatar: The Netflix Demake',
  },
  {
    description:
      '10 points from Brokenbuck.\n\nSocials: \nhttps://twitter.com/EsemicolonR\n\nSupport: \nMembE;R klub: https://bit.ly/48E2omy\nhttps://www.patreon.com/esemicolonr\nhttps://paypal.me/esemicolonr?country...\nETH: 0x6B63C144184B98BaEb3f11154d432e82FA558D50',
    id: 2,
    published: '2024-04-02T03:45:10',
    status: 'Filtered',
    thumbnail_url: 'https://i.ytimg.com/vi/zWv1JwAo48I/maxresdefault.jpg',
    video_id: 'zWv1JwAo48I',
    duration: 830,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=zWv1JwAo48I',
    subscription_id: 1,
    title: "The American Society of Magical N'augurs",
  },
  {
    description: "Sorry, hopeful Zutarians. She's taken.",
    id: 3,
    published: '2024-03-04T21:58:59',
    status: 'Filtered',
    thumbnail_url:
      'https://i.ytimg.com/vi/i5pwFcW-bOA/hqdefault.jpg?sqp=-oaymwEmCOADEOgC8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGHIgQyg7MA8=&rs=AOn4CLAuOHlYYu9uX7hjUmtK2RYZbaw6nQ',
    video_id: 'i5pwFcW-bOA',
    duration: 17,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=i5pwFcW-bOA',
    subscription_id: 1,
    title: 'Cave of Two Siblings',
  },
  {
    description:
      'Better late than nevE;R. \n\nSocials: \nhttps://twitter.com/EsemicolonR\n\nSupport: \nMembE;R klub: https://bit.ly/48E2omy\nhttps://www.patreon.com/esemicolonr\nhttps://paypal.me/esemicolonr?country...\nETH: 0x6B63C144184B98BaEb3f11154d432e82FA558D50',
    id: 4,
    published: '2024-01-31T17:36:02',
    status: 'Filtered',
    thumbnail_url: 'https://i.ytimg.com/vi_webp/q-8TkayFT34/maxresdefault.webp',
    video_id: 'q-8TkayFT34',
    duration: 898,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=q-8TkayFT34',
    subscription_id: 1,
    title: 'Avatar: The Last Airbender Trailer RE;daction',
  },
  {
    description:
      "It's a-here.  \n\nSocials: \nhttps://twitter.com/EsemicolonR\n\nSupport: \nMembE;R klub: https://bit.ly/48E2omy\nhttps://www.patreon.com/esemicolonr\nhttps://paypal.me/esemicolonr?country...\nETH: 0x6B63C144184B98BaEb3f11154d432e82FA558D50",
    id: 5,
    published: '2023-11-18T05:27:33',
    status: 'Filtered',
    thumbnail_url: 'https://i.ytimg.com/vi/Gy1PZkwxfkk/maxresdefault.jpg',
    video_id: 'Gy1PZkwxfkk',
    duration: 2128,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=Gy1PZkwxfkk',
    subscription_id: 1,
    title: 'TLoW: Book 3 - Well, I think Zaheer BLOWS (Part 5)',
  },
  {
    description:
      "I said vid drop. Not THE vid drop. I ain't doin nunna that.\n\nReal vid's like thirty minutes out, relax",
    id: 6,
    published: '2023-11-18T04:45:51',
    status: 'Pending Download',
    thumbnail_url: 'https://i.ytimg.com/vi/bGP0_-qI654/maxresdefault.jpg',
    video_id: 'bGP0_-qI654',
    duration: 17,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=bGP0_-qI654',
    subscription_id: 1,
    title: 'placeholdE;R meme',
  },
  {
    description: '"Uncle, that\'s what ALL live-action adaptations are."',
    id: 7,
    published: '2023-11-11T00:18:51',
    status: 'Pending Download',
    thumbnail_url:
      'https://i.ytimg.com/vi/XYKwiRPpsaI/sd2.jpg?sqp=-oaymwEoCIAFEOAD8quKqQMcGADwAQH4AbYIgAKAD4oCDAgAEAEYciBVKEMwDw==&rs=AOn4CLDCcAx2zvxvAXDbKl5P5CR24KQYQQ',
    video_id: 'XYKwiRPpsaI',
    duration: 31,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=XYKwiRPpsaI',
    subscription_id: 1,
    title: 'Iroh vs Netflix',
  },
  {
    description: "I didn't forget.",
    id: 8,
    published: '2023-09-11T18:55:27',
    status: 'Pending Download',
    thumbnail_url:
      'https://i.ytimg.com/vi/9mtdmdHgnkc/sd2.jpg?sqp=-oaymwEoCIAFEOAD8quKqQMcGADwAQH4AbYIgAKAD4oCDAgAEAEYZSBRKE4wDw==&rs=AOn4CLCXKJY7SbJs8m4noFwKQQLsUQFAeA',
    video_id: '9mtdmdHgnkc',
    duration: 18,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=9mtdmdHgnkc',
    subscription_id: 1,
    title: 'Leaf Me Alone',
  },
  {
    description:
      'You know what The Little Mermaid was always missing? Bird rap. \nAnd another 45 minutes.\n\nSocials: \nhttps://twitter.com/EsemicolonR\n\nSupport: \nLimited-time plush boi: https://www.makeship.com/products/shadower-plush\nhttps://www.patreon.com/esemicolonr\nhttps://paypal.me/esemicolonr?country...\nETH: 0x6B63C144184B98BaEb3f11154d432e82FA558D50\n\nTracks (by order of appearance): \nスプラッシュ・オーシャン - Amagi Brilliant Park OST\nチケットぜんぶ30円 - Amagi Brilliant Park OST',
    id: 9,
    published: '2023-06-04T19:57:40',
    status: 'Pending Download',
    thumbnail_url: 'https://i.ytimg.com/vi_webp/7tg8RkxOXeo/maxresdefault.webp',
    video_id: '7tg8RkxOXeo',
    duration: 695,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=7tg8RkxOXeo',
    subscription_id: 1,
    title: 'THE LATER ME;RMAID',
  },
];

export const directories: Directory[] = [
  {
    id: 2,
    title: 'Movies',
    uuid: '364f2ba8-254e-492d-a8d5-8658cfc90161',
    key: 3,
    locations: [
      {
        id: 9,
        path: '/media/Media/Video/Movies',
      },
    ],
  },
  {
    id: 4,
    title: 'Youtube',
    uuid: '0c717b05-2deb-419c-a2d0-e68cceddea04',
    key: 7,
    locations: [
      {
        id: 9,
        path: '/index/YouTube',
      },
      {
        id: 10,
        path: '/index/media',
      },
    ],
  },
  {
    id: 7,
    title: 'TV Shows',
    uuid: '50b6e1e0-e274-41e4-ade8-1e71e95c9330',
    key: 2,
    locations: [
      {
        id: 9,
        path: '/media/Media/Video/TV',
      },
    ],
  },
  {
    id: 9,
    title: 'Fitness',
    uuid: 'e32e9e32-b24c-4867-b113-95fc3914e37e',
    key: 16,
    locations: [
      {
        id: 9,
        path: '/index/YouTube/reference',
      },
    ],
  },
  {
    id: 10,
    title: 'Misc',
    uuid: '2c507cdc-36d7-43cc-beee-efbee3644bbd',
    key: 1,
    locations: [
      {
        id: 9,
        path: '/media/Media/Video/Video',
      },
    ],
  },
  {
    id: 11,
    title: 'Personal',
    uuid: '3df269f4-004e-4c00-b522-4acb6c8dfe54',
    key: 14,
    locations: [
      {
        id: 9,
        path: '/media/Media/Video/Personal',
      },
    ],
  },
];
