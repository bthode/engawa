import React, { useEffect, useState } from 'react';
import { Alert, AlertTitle, Box, Card, CardContent, Typography, Chip } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

interface Requirement {
  name: string;
  available: boolean;
  path: string | null;
}

interface RequirementsResponse {
  ffmpeg: Requirement;
  ffprobe: Requirement;
}

const RequirementsCheck: React.FC = () => {
  const [requirements, setRequirements] = useState<RequirementsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRequirements = async () => {
      try {
        const response = await fetch('/api/settings/requirements');
        if (!response.ok) {
          throw new Error('Failed to fetch requirements');
        }
        const data: RequirementsResponse = await response.json();
        setRequirements(data);
      } catch (err) {
        console.error('Error checking requirements:', err);
        setError('Failed to check requirements. Please try again later.');
      }
    };

    fetchRequirements();
  }, []);

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!requirements) {
    return <Typography>Loading requirements check...</Typography>;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          System Requirements Check
        </Typography>
        {Object.entries(requirements).map(([key, requirement]) => (
          <Box key={key} mb={2}>
            <Typography variant="subtitle1">
              {requirement.name}:{' '}
              <Chip
                icon={requirement.available ? <CheckCircleOutlineIcon /> : <ErrorOutlineIcon />}
                label={requirement.available ? 'Found' : 'Not Found'}
                color={requirement.available ? 'success' : 'error'}
                size="small"
              />
            </Typography>
            {requirement.available && requirement.path && (
              <Typography variant="body2" color="textSecondary">
                Path: {requirement.path}
              </Typography>
            )}
            {!requirement.available && key === 'ffmpeg' && (
              <Alert severity="warning" sx={{ mt: 1 }}>
                <AlertTitle>ffmpeg not found</AlertTitle>
                The downloaded format may not be the best available. Installing ffmpeg is strongly recommended:{' '}
                <a
                  href="https://github.com/yt-dlp/yt-dlp#dependencies"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: '#007BFF' }}
                >
                  https://github.com/yt-dlp/yt-dlp#dependencies
                </a>
              </Alert>
            )}
          </Box>
        ))}
      </CardContent>
    </Card>
  );
};

export default RequirementsCheck;
