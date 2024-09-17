'use client';
import React, { useState } from 'react';
import Navigation from '../navigation';
import { Button, Box } from '@mui/material';
import ResetConfirmationDialog from '@/components/ResetConfirmationDialog';

const Settings: React.FC = () => {
  const [isResetDialogOpen, setIsResetDialogOpen] = useState(false);

  return (
    <Navigation>
      <Box mt={2}>
        <Button variant="contained" color="error" onClick={() => setIsResetDialogOpen(true)}>
          Reset All
        </Button>
      </Box>
      <ResetConfirmationDialog open={isResetDialogOpen} onClose={() => setIsResetDialogOpen(false)} />
    </Navigation>
  );
};

export default Settings;
