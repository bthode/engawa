import React from 'react';
import Navigation from '../navigation';
import AddSubscriptionForm from '@/components/AddSubscriptionForm';
import SubscriptionList from '@/components/SubscriptionList';
import { SubscriptionProvider } from '@/components/SubscriptionContext';

const Subscriptions: React.FC = () => {
  return (
    <Navigation>
      <SubscriptionProvider>
        <AddSubscriptionForm />
        <SubscriptionList />
      </SubscriptionProvider>
    </Navigation>
  );
};

export default Subscriptions;
