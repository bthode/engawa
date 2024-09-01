'use client';
import React, { useState } from 'react';
import {
  TextField,
  CircularProgress,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Link,
  Button,
  Box,
} from '@mui/material';
import axios from 'axios';
import { isValidYoutubeUrl } from '@utilities/urlUtils';
import { useSnackbar } from 'notistack';

interface ChannelInfo {
  title: string;
  rss_link: string;
  image_link: string;
  description: string;
}

const YouTubeLinkFetcher: React.FC = () => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [channelInfo, setChannelInfo] = useState<ChannelInfo | null>(null);
  const { enqueueSnackbar } = useSnackbar();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUrl(value);
    setError('');
  };

  const validateAndFetch = async () => {
    if (!isValidYoutubeUrl(url)) {
      setError('Invalid URL');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/api/fetch_rss', { channel_url: url });
      setChannelInfo(response.data);
      enqueueSnackbar('Channel information fetched successfully!', { variant: 'success' });
    } catch (error) {
      console.error('Error fetching RSS:', error);
      setError('Failed to fetch channel information');
      enqueueSnackbar('Error fetching channel information', { variant: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', mt: 4 }}>
      <TextField
        fullWidth
        label="YouTube Channel URL"
        variant="outlined"
        value={url}
        onChange={handleChange}
        error={!!error}
        helperText={error}
        disabled={loading}
        sx={{ mb: 2 }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={validateAndFetch}
        disabled={loading || !url}
        startIcon={loading && <CircularProgress size={20} color="inherit" />}
        sx={{ mb: 2 }}
      >
        {loading ? 'Fetching...' : 'Fetch Channel Info'}
      </Button>

      {channelInfo && (
        <Card>
          <CardMedia component="img" height="140" image={channelInfo.image_link} alt={channelInfo.title} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {channelInfo.title}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              {channelInfo.description}
            </Typography>
            <Link href={channelInfo.rss_link} target="_blank" rel="noopener noreferrer">
              RSS Feed
            </Link>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default YouTubeLinkFetcher;
