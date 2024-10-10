import { Video } from '@/types/videoTypes';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/Typography';
import React, { useEffect, useState } from 'react';
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
    duration: 5489,
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
    duration: 1489,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=bilJ8RcS7Pc',
    subscription_id: 1,
    title: 'Jurass Is Mine 3',
  },
];

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
    }, 6 * 1000);
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

export const transformRetentionPolicy = (retentionPolicy: RetentionPolicy): string => {
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
        }),
      });
      if (!response.ok) throw new Error('Failed to save subscription');
      handleCancel(); // Close the form after saving
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
        className="w-full max-w-md p-2 mb-4 border rounded"
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
        Loading video data...
      </Typography>
    </Box>
  );

  const videoDisplayStep = (videos: Video[], subscriptionTitle: string) => (
    <div>
      <SubscriptionVideos videos={videos} subscriptionTitle={subscriptionTitle} />
      <div className="flex-col items-center"></div>
    </div>
  );

  // const filterStep = () => (
  //   <div className="flex flex-col items-center">
  //     <h2 className="text-xl font-bold mb-4">Filters</h2>
  //     {filters.map((filter, index) => (
  //       <div key={index} className="flex mb-2 rounded">
  //         <select
  //           value={filter.criteria}
  //           onChange={(e) => {
  //             const newFilters = [...filters];
  //             newFilters[index].criteria = e.target.value as 'Duration' | 'Title' | 'Published' | 'Description';
  //             setFilters(newFilters);
  //           }}
  //           className="mr-2 p-2 border rounded bg-white text-gray-800"
  //         >
  //           <option value="Duration">Duration</option>
  //           <option value="Title">Title</option>
  //           <option value="Published">Published</option>
  //           <option value="Description">Description</option>
  //         </select>
  //         <select
  //           value={filter.operand}
  //           onChange={(e) => {
  //             const newFilters = [...filters];
  //             newFilters[index].operand = e.target.value as Operand;
  //             setFilters(newFilters);
  //           }}
  //           className="mr-2 p-2 border rounded bg-white text-gray-800"
  //         >
  //           {filter.criteria === 'Title' || filter.criteria === 'Description' ? (
  //             <>
  //               <option value="contains">contains</option>
  //               <option value="!contains">does not contain</option>
  //             </>
  //           ) : (
  //             <>
  //               <option value=">">{'>'}</option>
  //               <option value="<">{'<'}</option>
  //               <option value=">=">{'≥'}</option>
  //               <option value="<=">{'≤'}</option>
  //               <option value="==">{'='}</option>
  //               <option value="!=">{'≠'}</option>
  //             </>
  //           )}
  //         </select>
  //         <input
  //           type={filter.criteria === 'Published' ? 'date' : 'text'}
  //           value={filter.value as string}
  //           onChange={(e) => {
  //             const newFilters = [...filters];
  //             newFilters[index].value = e.target.value;
  //             setFilters(newFilters);
  //           }}
  //           className="mr-2 p-2 border rounded text-gray-800 bg-white"
  //         />
  //         <button
  //           onClick={() => setFilters(filters.filter((_, i) => i !== index))}
  //           className="px-2 py-1 bg-red-500 text-white rounded"
  //         >
  //           Remove
  //         </button>
  //       </div>
  //     ))}
  //     <button
  //       onClick={() => setFilters([...filters, { criteria: 'Title', operand: 'contains', value: '' }])}
  //       className="mb-4 px-4 py-2 bg-green-500 text-white rounded"
  //     >
  //       Add Filter
  //     </button>
  //   </div>
  // );

  const retentionPolicyStep = () => (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4">Retention Policy</h2>
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
        <input
          type="number"
          value={retentionPolicy.value as number}
          onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: parseInt(e.target.value) })}
          placeholder="Enter number of entities"
          className="mb-4 p-2 border rounded text-gray-800 bg-white"
        />
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

  const renderSummary = () => (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4 text-white">Summary</h2>
      <p className="text-white">
        <strong>Channel:</strong> {subscription?.title}
      </p>
      <p className="text-white">
        <strong>URL:</strong> {youtubeLink}
      </p>
      <h3 className="text-lg font-bold mt-4 mb-2 text-white">Filters:</h3>
      <ul className="list-disc pl-5 text-white">
        {filters.map((filter, index) => (
          <li key={index}>{`${filter.criteria} ${filter.operand} ${filter.value}`}</li>
        ))}
      </ul>
      <h3 className="text-lg font-bold mt-4 mb-2 text-white">Retention Policy:</h3>
      <p className="text-white">{`${retentionPolicy.type}${retentionPolicy.value ? `: ${transformLastNVideoHelperText(retentionPolicy.value)}` : ''}`}</p>
    </div>
  );

  return (
    <div className="container mx-auto p-4 snap-center">
      <h1 className="text-3xl font-bold mb-8 text-center">Add Subscription</h1>
      {currentStage === FormStage.LinkInput && linkInputStep()}
      {currentStage === FormStage.SubscriptionInfo && subscriptionInfoStep()}
      {currentStage === FormStage.PendingVideos && loadingStep()}
      {currentStage === FormStage.VideoDisplay && videoDisplayStep(videos, subscription?.title || '')}
      {currentStage === FormStage.Filter && <FilterStep filters={filters} setFilters={setFilters} />}{' '}
      {currentStage === FormStage.RetentionPolicy && retentionPolicyStep()}
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
