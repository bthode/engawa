import { Directory, SaveToProps } from '@/types/plexTypes';
import { Subscription } from '@/types/subscriptionTypes';
import { Video } from '@/types/videoTypes';
import { List, ListItem, ListItemText, Paper } from '@mui/material';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Grid from '@mui/material/Grid2';
import Typography from '@mui/material/Typography';
import React, { useEffect, useState } from 'react';
import LocationPicker from './DownloadToPicker';
import FilterStep, { Filter } from './FilterStep';
import { directories, mockSubscription, mockVideos } from './JsonMocking';
import RetentionPolicyStep, { RetentionPolicy } from './RetentionPolicyStep';
import SubscriptionVideos from './subvids';

enum FormStage {
  LinkInput = 1,
  SubscriptionInfo,
  PendingVideos,
  VideoDisplay,
  Filter,
  RetentionPolicy,
  Summary,
}

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
        return `Retain videos sinc ${value.toDateString()}`;
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
                <Typography variant="body2">{youtubeLink}</Typography>
              </>
            }
          />
        </Grid>
        <Grid>
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
        </Grid>
        <Grid>
          <SummarySection
            title="Retention Policy"
            content={<Typography variant="body1">{produceRetentionPolicySummaryText(retentionPolicy)}</Typography>}
          />
        </Grid>
        <Grid>
          <SummarySection
            title="Plex Location"
            content={
              selectedDirectory && selectedLocation ? (
                <>
                  <Typography variant="body1">
                    <strong>Library:</strong> {selectedDirectory.title}
                  </Typography>
                  <Typography variant="body2">
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
      {currentStage === FormStage.RetentionPolicy && (
        <RetentionPolicyStep retentionPolicy={retentionPolicy} setRetentionPolicy={setRetentionPolicy} />
      )}
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
