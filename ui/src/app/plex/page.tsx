'use client';
import React, { useState, useEffect } from 'react';
import Navigation from '../navigation';
import PlexServerDashboard from '@/components/PlexServerDashboard';
import { CircularProgress, Box, Typography } from '@mui/material';
import { PlexServer } from '@/types/plexTypes';

const Plex: React.FC = () => {
  const [plexData, setPlexData] = useState<PlexServer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlexData = async () => {
      try {
        const response = await fetch('/api/plex_server');
        if (!response.ok) {
          throw new Error('Failed to fetch Plex data');
        }
        const data = await response.json();
        setPlexData(data[0] || null); // empty collection means no plex server
        setLoading(false);
      } catch (err) {
        console.error('Error:', err);
        setError('Failed to load Plex server data. Please try again later.');
        setLoading(false);
      }
    };

    fetchPlexData();
  }, []);

  return (
    <Navigation>
      <Box sx={{ padding: 3 }}>
        <Typography variant="h4" gutterBottom>
          Plex Server
        </Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
            <CircularProgress />
          </Box>
        ) : error ? (
          <Typography color="error">{error}</Typography>
        ) : (
          <PlexServerDashboard plexServer={plexData} onServerUpdate={() => {}} />
        )}
      </Box>
    </Navigation>
  );
};

export default Plex;
