'use client';
import React, { useState } from 'react';
import { TextField, Button, Grid, Box } from '@mui/material';
import { useSubscriptions } from './SubscriptionContext';

const AddSubscriptionForm: React.FC = () => {
  const [subscriptionUrl, setSubscriptionUrl] = useState<string>('');
  const { addSubscription } = useSubscriptions();

  const validateUrl = (url: string): boolean => {
    const urlPattern =
      /^(https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:c\/|user\/|playlist\?list=|@([\w-]+)|channel\/|)?|youtu\.be\/)([\w-]+)/i;
    return urlPattern.test(url);
  };

  const handleSubscriptionUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSubscriptionUrl(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (validateUrl(subscriptionUrl)) {
      try {
        await addSubscription(subscriptionUrl);
        setSubscriptionUrl(''); // Clear the input after successful addition
      } catch (error) {
        console.error('Error adding subscription:', error);
      }
    }
  };

  return (
    <Box component="form" noValidate autoComplete="off" onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Subscription URL"
            value={subscriptionUrl}
            onChange={handleSubscriptionUrlChange}
            error={!validateUrl(subscriptionUrl) && subscriptionUrl !== ''}
            helperText={!validateUrl(subscriptionUrl) && subscriptionUrl !== '' ? 'Invalid URL' : ''}
          />
        </Grid>
      </Grid>
      <Box mt={2}>
        <Button variant="contained" color="primary" type="submit">
          Submit
        </Button>
      </Box>
    </Box>
  );
};

export default AddSubscriptionForm;
