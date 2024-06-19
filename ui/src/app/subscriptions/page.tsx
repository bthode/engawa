import React from 'react';
import Navigation from '../navigation';
import SubscriptionList from '@components/SubscriptionList';
import AddSubscription from '@components/AddSubscription';

const Subscriptions: React.FC = () => {
  return (
    <Navigation>
      <AddSubscription />
      <SubscriptionList />
    </Navigation>
  );
};

export default Subscriptions;
