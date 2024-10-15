'use client';
import { SubscriptionApi } from '@/api/apis/SubscriptionApi';
import { Subscription } from '@/api/models/Subscription';
import { Configuration } from '@/api/runtime';
import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';

interface SubscriptionContextType {
  subscriptions: Subscription[];
  loading: boolean;
  error: string | null;
  addSubscription: (url: string) => Promise<void>;
  deleteSubscription: (id: number) => Promise<void>;
  fetchSubscriptions: () => Promise<void>;
  syncSubscription: (id: number) => Promise<void>;
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
      const config = new Configuration({
        basePath: 'http://localhost:3000',
      });
      const subscriptionApi = new SubscriptionApi(config);
      const data = await subscriptionApi.getAllSubscriptionApiSubscriptionGet();
      setSubscriptions(data.sort((a, b) => a.title?.localeCompare(b.title ?? '') ?? 0));
      setError(null);
    } catch (error) {
      console.error('Error fetching subscriptions:', error);
      setError('Failed to fetch subscriptions');
    } finally {
      setLoading(false);
    }
  }, []);

  const syncSubscription = useCallback(
    async (id: string) => {
      try {
        const config = new Configuration({
          basePath: 'http://localhost:3000',
        });
        const subscriptionApi = new SubscriptionApi(config);
        await subscriptionApi.syncSubscriptionApiSubscriptionSubscriptionIdSyncPost({
          subscriptionId: parseInt(id, 10),
        });
        await fetchSubscriptions();
      } catch (error) {
        console.error('Error syncing subscription:', error);
        setError('Failed to sync subscription');
      }
    },
    [fetchSubscriptions],
  );

  const addSubscription = useCallback(
    async (url: string) => {
      try {
        const config = new Configuration({
          basePath: 'http://localhost:3000',
        });
        const subscriptionApi = new SubscriptionApi(config);
        await subscriptionApi.createSubscriptionApiSubscriptionPost({ subscriptionCreate: { url } });
        await fetchSubscriptions();
      } catch (error) {
        console.error('Error adding subscription:', error);
        setError('Failed to add subscription');
      }
    },
    [fetchSubscriptions],
  );

  const deleteSubscription = useCallback(
    async (id: string) => {
      try {
        setLoading(true);
        const config = new Configuration({
          basePath: 'http://localhost:3000',
        });
        const subscriptionApi = new SubscriptionApi(config);
        await subscriptionApi.deleteSubscriptionApiSubscriptionSubscriptionIdDelete({
          subscriptionId: parseInt(id, 10),
        });
        await fetchSubscriptions();
      } catch (error) {
        console.error('Error deleting subscription:', error);
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
