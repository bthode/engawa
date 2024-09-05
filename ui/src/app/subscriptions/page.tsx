'use client';
import React from 'react';
import Navigation from '../navigation';
import AddSubscriptionForm from '@/components/AddSubscriptionForm';
import SubscriptionList from '@/components/SubscriptionList';
import { SubscriptionProvider } from '@/components/SubscriptionContext';
import { Box, Tabs, Tab } from '@mui/material';
import SubscriptionVideos from '@/components/SubscriptionVideos';


const Subscriptions: React.FC = () => {
  const [selectedTab, setSelectedTab] = React.useState(0);
  const [selectedSubscriptionId, setSelectedSubscriptionId] = React.useState<string | null>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  const handleSubscriptionSelect = (subscriptionId: string) => {
    setSelectedSubscriptionId(subscriptionId);
    setSelectedTab(1);
  };

  return (
    <Navigation>
      <SubscriptionProvider>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={selectedTab} onChange={handleTabChange}>
            <Tab label="Subscriptions" />
            <Tab label="Videos" disabled={!selectedSubscriptionId} />
          </Tabs>
        </Box>
        {selectedTab === 0 && (
          <>
            <AddSubscriptionForm />
            <SubscriptionList onSubscriptionSelect={handleSubscriptionSelect} />
          </>
        )}
        {selectedTab === 1 && selectedSubscriptionId && (
          <SubscriptionVideos subscriptionId={selectedSubscriptionId} />
        )}
      </SubscriptionProvider>
    </Navigation>
  );
};

export default Subscriptions;