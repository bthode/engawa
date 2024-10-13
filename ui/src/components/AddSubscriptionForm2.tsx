import { Directory, SaveToProps } from '@/types/plexTypes';
import { Video } from '@/types/videoTypes';
import { List, ListItem, ListItemText, Paper, Slider } from '@mui/material';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/Grid2';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import Typography from '@mui/material/Typography';
import React, { useEffect, useState } from 'react';
import LocationPicker from './DownloadToPicker';
import FilterStep, { Filter } from './FilterStep';
import SubscriptionVideos from './subvids';

interface Subscription {
  error_state: string | null;
  id: number;
  last_updated: string | null;
  title: string;
  url: string;
  description: string;
  image: string;
  rss_feed_url: string;
  type: 'Channel' | 'Playlist' | 'Video';
}

export type VideoStatus = 'Pending' | 'In Progress' | 'Failed' | 'Deleted' | 'Complete' | 'Excluded' | 'Filtered';

type RetentionPolicyType = 'RetainAll' | 'LastNEntities' | 'EntitiesSince';

interface RetentionPolicy {
  type: RetentionPolicyType;
  value?: number | Date | string;
}

enum FormStage {
  LinkInput = 1,
  SubscriptionInfo,
  PendingVideos,
  VideoDisplay,
  Filter,
  RetentionPolicy,
  Summary,
}

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

const mockVideos: Video[] = [
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

export const fetchPlexLocationData = (): Promise<Directory[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(directories);
    }, 200);
  });
};

export const obtainSubscription = (url: string): Promise<Subscription> => {
  console.log(url);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockSubscription);
    }, 500);
  });
};

export const fetchVideoData = (url: string): Promise<Video[]> => {
  console.log(url);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockVideos);
    }, 1 * 1000);
  });
};

export const transformLastNVideoHelperText = (value: number | Date | string): string => {
  switch (typeof value) {
    case 'number':
      return `Retain the last ${value} videos`;
    case 'object':
      if (value instanceof Date) {
        return `Retain videos until ${value.toDateString()}`;
      }
      return 'N/A';
    case 'string':
      return 'N/A';
  }
};

export const produceRetentionPolicySummaryText = (retentionPolicy: RetentionPolicy): string => {
  switch (retentionPolicy.type) {
    case 'RetainAll':
      return 'Retain all videos';
    case 'LastNEntities':
      return retentionPolicy.value !== undefined
        ? transformLastNVideoHelperText(retentionPolicy.value)
        : 'Invalid value';
    case 'EntitiesSince':
      return retentionPolicy.value !== undefined
        ? transformLastNVideoHelperText(retentionPolicy.value)
        : 'Invalid value';
    default:
      return 'N/A';
  }
};

const MultiStepForm: React.FC = () => {
  const [currentStage, setCurrentStage] = useState<number>(1);
  const [youtubeLink, setYoutubeLink] = useState<string>('');
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [videos, setVideos] = useState<Video[]>([]);
  const [filters, setFilters] = useState<Filter[]>([]);
  const [retentionPolicy, setRetentionPolicy] = useState<RetentionPolicy>({ type: 'RetainAll' });
  const [directories, setDirectories] = React.useState<Directory[]>([]);
  const [saveToProps, setSaveToProps] = useState<SaveToProps>({
    directoryId: -1,
    locationId: -1,
  });

  useEffect(() => {
    if (currentStage === FormStage.SubscriptionInfo && subscription) {
      fetchVideoData(subscription.url)
        .then((fetchedVideos) => {
          setVideos(fetchedVideos);
        })
        .catch((error) => {
          console.error('Error fetching videos:', error);
          // Handle error (e.g., show error message to user)
        });
      fetchPlexLocationData().then((fetchedDirectories) => {
        setDirectories(fetchedDirectories);
      });
    } else if (currentStage === FormStage.PendingVideos && videos.length > 0) {
      setCurrentStage(FormStage.VideoDisplay);
    }
  }, [currentStage, subscription, videos]);

  const handleNext = () => {
    if (currentStage === FormStage.LinkInput) {
      obtainSubscription(youtubeLink).then((fetchedSubscription) => {
        setSubscription(fetchedSubscription);
        setCurrentStage(FormStage.SubscriptionInfo);
      });
    } else if (currentStage === FormStage.SubscriptionInfo) {
      if (videos.length > 0) {
        setCurrentStage(FormStage.VideoDisplay);
      } else {
        setCurrentStage(FormStage.PendingVideos);
      }
    } else {
      setCurrentStage((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    setCurrentStage((prev) => prev - 1);
  };

  const handleCancel = () => {
    setCurrentStage(FormStage.LinkInput);
    setYoutubeLink('');
    setSubscription(null);
    setVideos([]);
    setFilters([]);
    setRetentionPolicy({ type: 'RetainAll' });
    // Here you would typically call a function to close the form
  };

  const handleSave = async () => {
    try {
      const response = await fetch('/api/subscription', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: youtubeLink,
          filters,
          retentionPolicy,
          saveToProps,
        }),
      });
      if (!response.ok) throw new Error('Failed to save subscription');
      handleCancel();
    } catch (error) {
      console.error('Error saving subscription:', error);
      // Handle error (e.g., show error message to user)
    }
  };

  const linkInputStep = () => (
    <div className="flex flex-col items-center">
      <input
        type="text"
        value={youtubeLink}
        onChange={(e) => setYoutubeLink(e.target.value)}
        placeholder="Enter YouTube channel link"
        className="w-full max-w-md p-2 mb-4 border rounded text-black bg-white"
      />
    </div>
  );

  const subscriptionInfoStep = () => (
    <div className="flex flex-col items-center">
      {subscription && (
        <>
          <h1 className="text-2xl font-bold mb-4">{subscription.title}</h1>
          <img src={subscription.image} alt={subscription.title} className="w-64 h-64 object-cover mb-4" />
          <p className="max-w-[50%] min-w-[300px]">{subscription.description}</p>
          <a href={subscription.url} target="_blank" rel="noopener noreferrer" className="mb-4 text-blue-500">
            Visit Channel
          </a>
        </>
      )}
    </div>
  );

  const loadingStep = () => (
    <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="50vh">
      <CircularProgress size={60} />
      <Typography variant="h6" style={{ marginTop: '20px' }}>
        Fetching video metadata...
      </Typography>
    </Box>
  );

  const videoDisplayStep = (videos: Video[], subscriptionTitle: string) => (
    <div>
      <SubscriptionVideos videos={videos} subscriptionTitle={subscriptionTitle} />
      <div className="flex-col items-center"></div>
    </div>
  );

  const retentionPolicyStep = () => (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4">Retention Policy</h2>
      <FormControl>
        <FormLabel id="retention-policy-step-label">Retention Policy Step</FormLabel>
        <RadioGroup row aria-labelledby="retention-policy-step-label" name="retention-policy-step-group">
          <FormControlLabel value="step1" control={<Radio />} label="All Videos" />
          <FormControlLabel value="step2" control={<Radio />} label="Last N Videos" />
          <FormControlLabel value="step3" control={<Radio />} label="Since Date" />
          <FormControlLabel value="step4" control={<Radio />} label="Relative Date Offset" />
        </RadioGroup>
      </FormControl>
      <select
        value={retentionPolicy.type}
        onChange={(e) => setRetentionPolicy({ type: e.target.value as RetentionPolicyType, value: undefined })}
        className="mb-4 p-2 border rounded text-gray-800 bg-white"
      >
        <option value="RetainAll">Keep All Videos</option>
        <option value="LastNEntities">Keep Last N Videos</option>
        <option value="EntitiesSince">Keep Videos Since...</option>
      </select>
      {retentionPolicy.type === 'LastNEntities' && (
        <Slider
          value={retentionPolicy.value as number}
          onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: parseInt(e.target.value) })}
          aria-labelledby="input-slider"
          valueLabelDisplay="on"
        />
        // <input
        //   type="number"
        //   value={retentionPolicy.value as number}
        //   onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: parseInt(e.target.value) })}
        //   placeholder="Enter number of entities"
        //   className="mb-4 p-2 border rounded text-gray-800 bg-white"
        // />
      )}
      {retentionPolicy.type === 'EntitiesSince' && (
        <div className="flex flex-col items-center">
          <input
            type="date"
            value={retentionPolicy.value as string}
            onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: e.target.value })}
            className="mb-2 p-2 border rounded text-gray-800 bg-white"
          />
          <input
            type="text"
            value={retentionPolicy.value as string}
            onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: e.target.value })}
            placeholder="Or enter relative time (e.g., '2 weeks ago')"
            className="mb-4 p-2 border rounded text-gray-800 bg-white"
          />
        </div>
      )}
    </div>
  );

  const renderSummary = () => {
    const selectedDirectory = directories.find((dir) => dir.key === saveToProps.directoryId);
    const selectedLocation = selectedDirectory?.locations.find((loc) => loc.id === saveToProps.locationId);

    const SummarySection = ({ title, content }: { title: string; content: React.ReactNode }) => (
      <>
        <Grid>
          <Typography variant="h6" gutterBottom>
            {title}
          </Typography>
        </Grid>
        <Grid>{content}</Grid>
      </>
    );

    return (
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h4" gutterBottom align="center">
          Subscription Summary
        </Typography>
        <Grid container spacing={2}>
          <SummarySection
            title="Channel"
            content={
              <>
                <Typography variant="body1">{subscription?.title}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {youtubeLink}
                </Typography>
              </>
            }
          />
          <SummarySection
            title="Filters"
            content={
              <List dense>
                {filters.map((filter, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={`${filter.criteria} ${filter.operand} ${filter.value}`} />
                  </ListItem>
                ))}
              </List>
            }
          />
          <SummarySection
            title="Retention Policy"
            content={<Typography variant="body1">{produceRetentionPolicySummaryText(retentionPolicy)}</Typography>}
          />
          <SummarySection
            title="Plex Location"
            content={
              selectedDirectory && selectedLocation ? (
                <>
                  <Typography variant="body1">
                    <strong>Library:</strong> {selectedDirectory.title}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    <strong>Path:</strong> {selectedLocation.path}
                  </Typography>
                </>
              ) : (
                <Typography variant="body1" color="error">
                  No Plex location selected
                </Typography>
              )
            }
          />
        </Grid>
      </Paper>
    );
  };

  return (
    <div className="container mx-auto p-4 snap-center">
      <h1 className="text-3xl font-bold mb-8 text-center">Add Subscription</h1>
      {currentStage === FormStage.LinkInput && linkInputStep()}
      {currentStage === FormStage.SubscriptionInfo && subscriptionInfoStep()}
      {currentStage === FormStage.PendingVideos && loadingStep()}
      {currentStage === FormStage.VideoDisplay && videoDisplayStep(videos, subscription?.title || '')}
      {currentStage === FormStage.Filter && <FilterStep filters={filters} setFilters={setFilters} />}{' '}
      {currentStage === FormStage.RetentionPolicy && retentionPolicyStep()}
      {currentStage === FormStage.RetentionPolicy && (
        <LocationPicker saveToProps={saveToProps} setSaveToProps={setSaveToProps} directories={directories} />
      )}
      {currentStage === FormStage.Summary && renderSummary()}
      {currentStage !== FormStage.PendingVideos && (
        <div className="flex justify-center space-x-4 mt-10">
          <button onClick={handleBack} className="bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-blue-600">
            Back
          </button>
          <button onClick={handleCancel} className="bg-red-500 text-white py-2 px-4 rounded-full hover:bg-red-600">
            Cancel
          </button>
          {currentStage === FormStage.Summary ? (
            <button onClick={handleSave} className="bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-blue-600">
              Save
            </button>
          ) : (
            <button onClick={handleNext} className="bg-green-500 text-white py-2 px-4 rounded-full hover:bg-green-600">
              Next
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default MultiStepForm;
