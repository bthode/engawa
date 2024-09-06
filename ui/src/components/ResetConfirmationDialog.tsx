import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button } from '@mui/material';

interface ResetConfirmationDialogProps {
  open: boolean;
  onClose: () => void;
}

const ResetConfirmationDialog: React.FC<ResetConfirmationDialogProps> = ({ open, onClose }) => {
  const handleReset = async () => {
    try {
      const response = await fetch('/api/settings/reset', { method: 'POST' });
      if (response.ok) {
        // Handle successful reset
        console.log('Reset successful');
        onClose();
      } else {
        // Handle error
        console.error('Reset failed');
      }
    } catch (error) {
      console.error('Error during reset:', error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Confirm Reset</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Are you sure you want to reset all data? This action will delete all Plex, Subscription, and Video data. This
          action cannot be undone.
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleReset} color="error" autoFocus>
          Reset
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ResetConfirmationDialog;
