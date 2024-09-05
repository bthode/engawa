'use client';
import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { Subscription } from '@/types/subscriptionTypes';

interface SubscriptionContextType {
  subscriptions: Subscription[];
  loading: boolean;
  error: string | null;
  fetchSubscriptions: () => Promise<void>;
  addSubscription: (url: string) => Promise<void>;
  syncSubscription: (id: string) => Promise<void>;
  deleteSubscription: (id: string) => Promise<void>;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(undefined);

export const useSubscriptions = () => {
  const context = useContext(SubscriptionContext);
  if (!context) {
    throw new Error('useSubscriptions must be used within a SubscriptionProvider');
  }
  return context;
};

export const SubscriptionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSubscriptions = useCallback(async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/subscription');
      const data: Subscription[] = await response.json();
      setSubscriptions(data);
      setError(null);
    } catch (error) {
      setError('Failed to fetch subscriptions');
    } finally {
      setLoading(false);
    }
  }, []);

  const syncSubscription = useCallback(
    async (id: string) => {
      try {
        const response = await fetch(`/api/subscription/${id}/sync`, {
          method: 'POST',
        });
        if (!response.ok) {
          throw new Error('Failed to sync subscription');
        }
        await fetchSubscriptions();
      } catch (error) {
        setError('Failed to sync subscription');
      }
    },
    [fetchSubscriptions],
  );

  const addSubscription = useCallback(
    async (url: string) => {
      try {
        const response = await fetch('/api/subscription', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url }),
        });
        if (!response.ok) {
          throw new Error('Failed to add subscription');
        }
        await fetchSubscriptions();
      } catch (error) {
        setError('Failed to add subscription');
      }
    },
    [fetchSubscriptions],
  );

  

  const deleteSubscription = useCallback(
    async (id: string) => {
      try {
        const response = await fetch(`/api/subscription/${id}`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          throw new Error('Failed to delete subscription');
        }
        await fetchSubscriptions();
      } catch (error) {
        setError('Failed to delete subscription');
      }
    },
    [fetchSubscriptions],
  );

  useEffect(() => {
    fetchSubscriptions();
  }, [fetchSubscriptions]);

  const value = {
    subscriptions,
    loading,
    error,
    fetchSubscriptions,
    addSubscription,
    syncSubscription,
    deleteSubscription,
  };

  return <SubscriptionContext.Provider value={value}>{children}</SubscriptionContext.Provider>;
};
