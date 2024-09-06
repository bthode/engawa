/* eslint-disable @next/next/no-img-element */
'use client';
import React, { useState, useEffect } from 'react';
import { Typography, Grid, Box, CardContent, Card, CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';
import { Subscription } from '@/types/subscriptionTypes';
import { Video } from '@/types/videoTypes';

interface SubscriptionVideosProps {
  subscriptionId: string;
}

const SubscriptionVideos: React.FC<SubscriptionVideosProps> = ({ subscriptionId }) => {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubscriptionAndVideos = async () => {
      try {
        setLoading(true);
        const [subscriptionResponse, videosResponse] = await Promise.all([
          fetch(`/api/subscription/${subscriptionId}`),
          fetch(`/api/subscription/${subscriptionId}/videos`),
        ]);

        if (!subscriptionResponse.ok || !videosResponse.ok) {
          throw new Error('Failed to fetch data');
        }

        if (subscriptionResponse.status === 404) {
          throw new Error('Subscription not found');
        }

        const subscriptionData: Subscription = await subscriptionResponse.json();
        const videosData: Video[] = await videosResponse.json();

        setSubscription(subscriptionData);
        setVideos(videosData);
        setError(null);
      } catch (err) {
        console.error('Error:', err);
        setError('Failed to load subscription data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptionAndVideos();
  }, [subscriptionId]);
  if (loading) {
    return <CircularProgress />;
  }

  if (error || !subscription) {
    return <Typography color="error">{error || 'Subscription not found'}</Typography>;
  }

  return (
    <Box>
      <Card component={motion.div} whileHover={{ scale: 1.02 }} transition={{ type: 'spring', stiffness: 300 }}>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            {subscription.title}
          </Typography>
          <Typography variant="subtitle1" gutterBottom>
            URL: {subscription.url}
          </Typography>
          <Typography variant="body2">{subscription.description}</Typography>
        </CardContent>
      </Card>

      <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
        Videos
      </Typography>
      <Grid container spacing={3}>
        {videos.map((video) => (
          <Grid item xs={12} sm={6} md={4} key={video.video_id}>
            <Card component={motion.div} whileHover={{ scale: 1.05 }} transition={{ type: 'spring', stiffness: 300 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {video.title}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Author: {video.author}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Published: {new Date(video.published).toLocaleDateString()}
                </Typography>
                <img src={video.thumbnail_url} />
                <Box mt={2}>
                  <a href={video.link} target="_blank" rel="noopener noreferrer">
                    Watch on YouTube
                  </a>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default SubscriptionVideos;
