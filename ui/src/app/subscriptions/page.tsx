'use client';
import React from 'react';
import Navigation from '../navigation';
import AddSubscriptionForm from '@/components/AddSubscriptionForm';
import SubscriptionList from '@/components/SubscriptionList';
import { SubscriptionProvider } from '@/components/SubscriptionContext';
import { Box, IconButton, Tooltip } from '@mui/material';
import SubscriptionVideos from '@/components/SubscriptionVideos';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const Subscriptions: React.FC = () => {
  const [selectedSubscriptionId, setSelectedSubscriptionId] = React.useState<string | null>(null);

  const handleSubscriptionSelect = (subscriptionId: string) => {
    setSelectedSubscriptionId(subscriptionId);
  };

  const handleBackToList = () => {
    setSelectedSubscriptionId(null);
  };

  return (
    <Navigation onSubscriptionsClick={handleBackToList}>
      <SubscriptionProvider>
        <Box sx={{ mb: 2 }}>
          {selectedSubscriptionId ? (
            <>
              <Tooltip title="Back to Subscriptions">
                <IconButton onClick={handleBackToList} sx={{ mb: 2 }}>
                  <ArrowBackIcon />
                </IconButton>
              </Tooltip>
              <SubscriptionVideos subscriptionId={selectedSubscriptionId} />
            </>
          ) : (
            <>
              <AddSubscriptionForm />
              <SubscriptionList onSubscriptionSelect={handleSubscriptionSelect} />
            </>
          )}
        </Box>
      </SubscriptionProvider>
    </Navigation>
  );
};

export default Subscriptions;
