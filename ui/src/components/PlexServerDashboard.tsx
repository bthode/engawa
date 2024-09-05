import React, { useState } from 'react';
import { Card, CardContent, Typography, Grid, Box, Chip, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Alert, Tooltip } from '@mui/material';
import { Movie as MovieIcon, Tv as TvIcon, Photo as PhotoIcon, Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { motion } from 'framer-motion';

import { PlexServer, Directory } from '@/types/plexTypes';
import { deletePlexServer, savePlexServer } from '@/actions/savePlexServer';

const getLibraryIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'movie': return <MovieIcon />;
    case 'show': return <TvIcon />;
    case 'photo': return <PhotoIcon />;
    default: return <MovieIcon />;
  }
};

const PlexServerDashboard: React.FC<{ plexServer: PlexServer | null, onServerUpdate: () => void }> = ({ plexServer, onServerUpdate }) => {
  const [] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newServer, setNewServer] = useState<Partial<PlexServer>>({});
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleAddServer = () => {
    setIsAddModalOpen(true);
    setNewServer({});
    setErrorMessage(null);
  };

  const handleCloseAddModal = () => {
    setIsAddModalOpen(false);
    setNewServer({});
    setErrorMessage(null);
  };

  const handleSaveNewServer = async () => {
    if (!newServer.name || !newServer.endpoint || !newServer.port || !newServer.token) {
      setErrorMessage('Please fill in all fields');
      return;
    }

    try {
      await savePlexServer(newServer as PlexServer);
      setIsAddModalOpen(false);
      onServerUpdate();
      setErrorMessage(null);
    } catch (error) {
      console.error('Error saving new Plex server:', error);
      setErrorMessage('An error occurred while saving the server.');
    }
  };


  const handleDeleteServer = async () => {
    if (!plexServer) return;

    try {
      await deletePlexServer(plexServer);
      onServerUpdate();
    } catch (error) {
      console.error('Error deleting Plex server:', error);
      setErrorMessage('An error occurred while deleting the server.');
    }
  };

  const renderServerForm = (server: Partial<PlexServer>, setServer: React.Dispatch<React.SetStateAction<any>>) => (
    <>
      <TextField
        autoFocus
        margin="dense"
        label="Server Name"
        type="text"
        fullWidth
        value={server.name || ''}
        onChange={(e) => setServer({ ...server, name: e.target.value })}
      />
      <Tooltip title="Use the endpoint as accessible from where Engawa is running.">
      <TextField
        margin="dense"
        label="Endpoint"
        type="text"
        fullWidth
        value={server.endpoint || ''}
        onChange={(e) => setServer({ ...server, endpoint: e.target.value })}
      />
      </Tooltip>
      <TextField
        margin="dense"
        label="Port"
        type="text"
        fullWidth
        value={server.port || ''}
        onChange={(e) => setServer({ ...server, port: e.target.value })}
      />
      <TextField
        margin="dense"
        label="Server Token"
        type="password"
        fullWidth
        value={server.token || ''}
        onChange={(e) => setServer({ ...server, token: e.target.value })}
      />

    </>
  );

  return (
    <Box>
      {plexServer ? (
        <>
          <Card component={motion.div} whileHover={{ scale: 1.02 }} transition={{ type: "spring", stiffness: 300 }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h4" gutterBottom>{plexServer.name}</Typography>
                <Box>
                  <IconButton onClick={handleDeleteServer}><DeleteIcon /></IconButton>
                </Box>
              </Box>
              <Typography variant="subtitle1" gutterBottom>Endpoint: {plexServer.endpoint}</Typography>
              <Typography variant="subtitle1" gutterBottom>Port: {plexServer.port}</Typography>
              <Chip 
                label={plexServer.error_state ? 'Error' : 'Connected'} 
                color={plexServer.error_state ? 'error' : 'success'} 
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>

          <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>Libraries</Typography>
          <Grid container spacing={3}>
            {plexServer.directories.map((directory: Directory) => (
              <Grid item xs={12} sm={6} md={4} key={directory.uuid}>
                <Card component={motion.div} whileHover={{ scale: 1.05 }} transition={{ type: "spring", stiffness: 300 }}>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      {getLibraryIcon(directory.title)}
                      <Typography variant="h6" sx={{ ml: 1 }}>{directory.title}</Typography>
                    </Box>
                    <Typography variant="body2" color="textSecondary">UUID: {directory.uuid}</Typography>
                    {directory.locations.map((location, index) => (
                      <Typography key={index} variant="body2" color="textSecondary">
                        Path: {location.path}
                      </Typography>
                    ))}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      ) : (
        <Card>
          <CardContent>
            <Typography variant="h5" gutterBottom>No Plex Server Configured</Typography>
          </CardContent>
        </Card>
      )}

      {!plexServer && (
        <Box mt={2}>
          <Button startIcon={<AddIcon />} variant="contained" color="primary" onClick={handleAddServer}>
            Add Plex Server
          </Button>
        </Box>
      )}

      <Dialog open={isAddModalOpen} onClose={handleCloseAddModal}>
        <DialogTitle>Add Plex Server</DialogTitle>
        <DialogContent>
          {errorMessage && <Alert severity="error" sx={{ mb: 2 }}>{errorMessage}</Alert>}
          {renderServerForm(newServer, setNewServer)}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAddModal}>Cancel</Button>
          <Button onClick={handleSaveNewServer} color="primary">Add</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PlexServerDashboard;