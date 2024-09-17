'use client';
import React, { useState } from 'react';
import Navigation from '../navigation';
import { Button, Box, Typography } from '@mui/material';
import ResetConfirmationDialog from '@/components/ResetConfirmationDialog';
import RequirementsCheck from '@/components/RequirementsCheck';

const Settings: React.FC = () => {
  const [isResetDialogOpen, setIsResetDialogOpen] = useState(false);

  return (
    <Navigation>
      <Box mt={2} mb={4}>
        <RequirementsCheck />
      </Box>
      <Box mt={2}>
        <Typography variant="h6" gutterBottom>
          Database Reset
        </Typography>
        <Button variant="contained" color="error" onClick={() => setIsResetDialogOpen(true)}>
          Reset All
        </Button>
      </Box>
      <ResetConfirmationDialog open={isResetDialogOpen} onClose={() => setIsResetDialogOpen(false)} />
    </Navigation>
  );
};

export default Settings;
