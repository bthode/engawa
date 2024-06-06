import React from 'react';
import Navigation from '../navigation';
import SubscriptionList from '@components/SubscriptionList';

const Subscriptions: React.FC = () => {
  return (
    <Navigation>
      <SubscriptionList />
    </Navigation>
  );
};

export default Subscriptions;
