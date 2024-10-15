'use client';
import { Alert, Box, Button, Grid, TextField } from '@mui/material';
import React, { useState } from 'react';
import { useSubscriptions } from './SubscriptionContext';

const AddSubscriptionForm: React.FC = () => {
  const [subscriptionUrl, setSubscriptionUrl] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const { addSubscription, subscriptions } = useSubscriptions();

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
    setErrorMessage(null);

    if (validateUrl(subscriptionUrl)) {
      try {
        const existingSubscription = subscriptions.find((sub) => sub.url === subscriptionUrl);
        if (existingSubscription) {
          setErrorMessage('This subscription already exists.');
        } else {
          await addSubscription(subscriptionUrl as number);
          setSubscriptionUrl(''); // Clear the input after successful addition
        }
      } catch (error) {
        console.error('Error adding subscription:', error);
        setErrorMessage('An error occurred while adding the subscription.');
      }
    }
  };
  return (
    <Box component="form" noValidate autoComplete="off" onSubmit={handleSubmit}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={9}>
          <TextField
            fullWidth
            label="Subscription URL"
            value={subscriptionUrl}
            onChange={handleSubscriptionUrlChange}
            error={(!validateUrl(subscriptionUrl) && subscriptionUrl !== '') || !!errorMessage}
            helperText={(!validateUrl(subscriptionUrl) && subscriptionUrl !== '' ? 'Invalid URL' : '') || errorMessage}
          />
        </Grid>
        <Grid item xs={12} sm={3}>
          <Button variant="contained" color="primary" type="submit">
            Submit
          </Button>
        </Grid>
      </Grid>
      {errorMessage && (
        <Box mt={2}>
          <Alert severity="error">{errorMessage}</Alert>
        </Box>
      )}
    </Box>
  );
};

export default AddSubscriptionForm;
