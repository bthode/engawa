'use client';

import React, { useState, useEffect } from 'react';
import { Subscription } from '@/types/subscriptionTypes';
import '@css/subscriptions.css';

const SubscriptionList: React.FC = () => {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const response = await fetch('/api/subscription');
        const data: Subscription[] = await response.json();
        setSubscriptions(data);
      } catch (error) {
        setError('Failed to fetch subscriptions');
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptions();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="wapper">
      {subscriptions.map((sub) => (
        <div className="box" key={sub.id}>
          <img
            src={`data:image/png;base64,${sub.image}`}
            alt={sub.title}
            style={{ width: '100%', borderRadius: '8px' }}
          />
          <div className="title">{sub.title}</div>
        </div>
      ))}
    </div>
  );
};

export default SubscriptionList;
