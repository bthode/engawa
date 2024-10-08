import { Margin } from '@mui/icons-material';
import React, { useState } from 'react';

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

interface Video {
  description: string;
  id: number;
  published: string;
  status: VideoStatus;
  thumbnail_url: string;
  video_id: string;
  duration: number | null;
  author: string;
  link: string;
  retry_count: number;
  subscription_id: number;
  title: string;
}

type Operand = '>' | '<' | '>=' | '<=' | '==' | '!=' | 'contains' | '!contains';

interface Filter {
  criteria: 'Duration' | 'Title' | 'Published' | 'Description';
  operand: Operand;
  value: string | number | Date;
}

type RetentionPolicyType = 'NoPolicy' | 'LastNEntities' | 'EntitiesSince';

interface RetentionPolicy {
  type: RetentionPolicyType;
  value?: number | Date | string;
}

const mockSubscription: Subscription = {
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
    duration: 13489,
    author: 'E;R',
    link: 'https://www.youtube.com/watch?v=sU_1XforOp0',
    retry_count: 1,
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
    retry_count: 1,
    subscription_id: 1,
    title: 'Jurass Is Mine 3',
  },
];

const formatDuration = (seconds: number | null): string => {
  if (seconds === null) return 'N/A';
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  return `${hours}h ${minutes}m ${remainingSeconds}s`;
};

const MultiStepForm: React.FC = () => {
  const [currentStage, setCurrentStage] = useState<number>(1);
  const [youtubeLink, setYoutubeLink] = useState<string>('');
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [videos, setVideos] = useState<Video[]>([]);
  const [filters, setFilters] = useState<Filter[]>([]);
  const [retentionPolicy, setRetentionPolicy] = useState<RetentionPolicy>({ type: 'NoPolicy' });

  const handleNext = () => {
    if (currentStage === 1) {
      setSubscription(mockSubscription);
    } else if (currentStage === 2) {
      setVideos(mockVideos);
    }
    setCurrentStage((prev) => prev + 1);
  };

  const handleBack = () => {
    setCurrentStage((prev) => prev - 1);
  };

  const handleCancel = () => {
    setCurrentStage(1);
    setYoutubeLink('');
    setSubscription(null);
    setVideos([]);
    setFilters([]);
    setRetentionPolicy({ type: 'NoPolicy' });
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
      <div className="flex justify-between w-full max-w-md">
        <button onClick={handleCancel} className="px-4 py-2 bg-red-500 text-gray-800 rounded">
          Cancel
        </button>
        <button onClick={handleNext} className="px-4 py-2 bg-blue-500 text-gray-800 rounded">
          Next
        </button>
      </div>
    </div>
  );

  const subscriptioinInfoStep = () => (
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
      <div className="flex justify-between w-full max-w-md">
        <button onClick={handleBack} className="px-4 py-2 bg-gray-500 text-gray-800 rounded">
          Back
        </button>
        <button onClick={handleCancel} className="px-4 py-2 bg-red-500 text-gray-800 rounded">
          Cancel
        </button>
        <button onClick={handleNext} className="px-4 py-2 bg-blue-500 text-gray-800 rounded">
          Next
        </button>
      </div>
    </div>
  );

  const videoDisplayStep = () => (
    <div className="flex flex-col items-center">
      <table className="w-full max-w-4xl mb-4">
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Published</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {videos.map((video) => (
            <tr key={video.id}>
              <td>{video.title}</td>
              <td>{video.author}</td>
              <td>{new Date(video.published).toLocaleDateString()}</td>
              <td>{formatDuration(video.duration)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-between w-full max-w-md">
        <button onClick={handleBack} className="px-4 py-2 bg-gray-500 text-gray-800 rounded">
          Back
        </button>
        <button onClick={handleCancel} className="px-4 py-2 bg-red-500 text-gray-800 rounded">
          Cancel
        </button>
        <button onClick={handleNext} className="px-4 py-2 bg-blue-500 text-gray-800 rounded">
          Next
        </button>
      </div>
    </div>
  );
  const filterStep = () => (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4">Filters</h2>
      {filters.map((filter, index) => (
        <div key={index} className="flex mb-2">
          <select
            value={filter.criteria}
            onChange={(e) => {
              const newFilters = [...filters];
              newFilters[index].criteria = e.target.value as 'Duration' | 'Title' | 'Published' | 'Description';
              setFilters(newFilters);
            }}
            className="mr-2 p-2 border rounded bg-white text-gray-800"
          >
            <option value="Duration">Duration</option>
            <option value="Title">Title</option>
            <option value="Published">Published</option>
            <option value="Description">Description</option>
          </select>
          <select
            value={filter.operand}
            onChange={(e) => {
              const newFilters = [...filters];
              newFilters[index].operand = e.target.value as Operand;
              setFilters(newFilters);
            }}
            className="mr-2 p-2 border rounded bg-white text-gray-800"
          >
            {filter.criteria === 'Title' || filter.criteria === 'Description' ? (
              <>
                <option value="contains">contains</option>
                <option value="!contains">does not contain</option>
              </>
            ) : (
              <>
                <option value=">">{'>'}</option>
                <option value="<">{'<'}</option>
                <option value=">=">{'≥'}</option>
                <option value="<=">{'≤'}</option>
                <option value="==">{'='}</option>
                <option value="!=">{'≠'}</option>
              </>
            )}
          </select>
          <input
            type={filter.criteria === 'Published' ? 'date' : 'text'}
            value={filter.value as string}
            onChange={(e) => {
              const newFilters = [...filters];
              newFilters[index].value = e.target.value;
              setFilters(newFilters);
            }}
            className="mr-2 p-2 border rounded text-gray-800 bg-white"
          />
          <button
            onClick={() => setFilters(filters.filter((_, i) => i !== index))}
            className="px-2 py-1 bg-red-500 text-white rounded"
          >
            Remove
          </button>
        </div>
      ))}
      <button
        onClick={() => setFilters([...filters, { criteria: 'Title', operand: 'contains', value: '' }])}
        className="mb-4 px-4 py-2 bg-green-500 text-white rounded"
      >
        Add Filter
      </button>
      <div className="flex justify-between w-full max-w-md">
        <button onClick={handleBack} className="px-4 py-2 bg-gray-500 text-white rounded">
          Back
        </button>
        <button onClick={handleCancel} className="px-4 py-2 bg-red-500 text-white rounded">
          Cancel
        </button>
        <button onClick={handleNext} className="px-4 py-2 bg-blue-500 text-white rounded">
          Next
        </button>
      </div>
    </div>
  );

  const retentionPolicyStep = () => (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4">Retention Policy</h2>
      <select
        value={retentionPolicy.type}
        onChange={(e) => setRetentionPolicy({ type: e.target.value as RetentionPolicyType, value: undefined })}
        className="mb-4 p-2 border rounded text-gray-800 bg-white"
      >
        <option value="NoPolicy">No Policy</option>
        <option value="LastNEntities">Last N Entities</option>
        <option value="EntitiesSince">Entities Since</option>
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
      <div className="flex justify-between w-full max-w-md">
        <button onClick={handleBack} className="px-4 py-2 bg-gray-500 text-gray-800 rounded">
          Back
        </button>
        <button onClick={handleCancel} className="px-4 py-2 bg-red-500 text-gray-800 rounded">
          Cancel
        </button>
        <button onClick={handleNext} className="px-4 py-2 bg-blue-500 text-white rounded">
          Next
        </button>
      </div>
    </div>
  );

  const renderSummary = () => (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Summary</h2>
      <p className="text-gray-800">
        <strong>Channel:</strong> {subscription?.title}
      </p>
      <p className="text-gray-800">
        <strong>URL:</strong> {youtubeLink}
      </p>
      <h3 className="text-lg font-bold mt-4 mb-2 text-gray-800">Filters:</h3>
      <ul className="list-disc pl-5 text-gray-800">
        {filters.map((filter, index) => (
          <li key={index}>{`${filter.criteria} ${filter.operand} ${filter.value}`}</li>
        ))}
      </ul>
      <h3 className="text-lg font-bold mt-4 mb-2 text-gray-800">Retention Policy:</h3>
      <p className="text-gray-800">{`${retentionPolicy.type}${retentionPolicy.value ? `: ${retentionPolicy.value}` : ''}`}</p>
      <div className="flex justify-between w-full max-w-md mt-4">
        <button onClick={handleBack} className="px-4 py-2 bg-gray-500 text-gray-800 rounded">
          Back
        </button>
        <button onClick={handleCancel} className="px-4 py-2 bg-red-500 text-gray-800 rounded">
          Cancel
        </button>
        <button onClick={handleSave} className="px-4 py-2 bg-green-500 text-gray-800 rounded">
          Save
        </button>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-8 text-center">Add Subscription</h1>
      {currentStage === 1 && linkInputStep()}
      {currentStage === 2 && subscriptioinInfoStep()}
      {currentStage === 3 && videoDisplayStep()}
      {currentStage === 4 && filterStep()}
      {currentStage === 5 && retentionPolicyStep()}
      {currentStage === 6 && renderSummary()}
    </div>
  );
};

export default MultiStepForm;
