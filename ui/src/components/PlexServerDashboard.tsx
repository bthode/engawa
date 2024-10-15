import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Movie as MovieIcon,
  Photo as PhotoIcon,
  Tv as TvIcon,
} from '@mui/icons-material';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  IconButton,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material';
import { motion } from 'framer-motion';
import React, { useState } from 'react';

import { deletePlexServer, savePlexServer } from '@/actions/savePlexServer';
import { DirectoryPublic, PlexPublicWithDirectories, PlexServerCreate } from '@/api/models';

const getLibraryIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'movie':
      return <MovieIcon />;
    case 'show':
      return <TvIcon />;
    case 'photo':
      return <PhotoIcon />;
    default:
      return <MovieIcon />;
  }
};

const PlexServerDashboard: React.FC<{ plexServer: PlexPublicWithDirectories | null; onServerUpdate: () => void }> = ({
  plexServer,
  onServerUpdate,
}) => {
  const [localPlexServer, setLocalPlexServer] = useState<PlexPublicWithDirectories | null>(plexServer);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newServer, setNewServer] = useState<Partial<PlexServerCreate>>({});
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
      const savedServer = await savePlexServer(newServer as PlexServerCreate);
      setLocalPlexServer(savedServer[0]);
      setIsAddModalOpen(false);
      setErrorMessage(null);
    } catch (error) {
      console.error('Error saving new Plex server:', error);
      setErrorMessage('An error occurred while saving the server.');
    }
  };

  const handleDeleteServer = async () => {
    if (!localPlexServer) return;

    try {
      await deletePlexServer(localPlexServer);
      setLocalPlexServer(null);
      onServerUpdate();
    } catch (error) {
      console.error('Error deleting Plex server:', error);
      setErrorMessage('An error occurred while deleting the server.');
    }
  };

  const renderServerForm = (
    server: Partial<PlexServerCreate>,
    setServer: React.Dispatch<React.SetStateAction<Partial<PlexServerCreate>>>,
  ) => (
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
      <Tooltip title="Plex default port is 32400">
        <TextField
          margin="dense"
          label="Port"
          type="text"
          fullWidth
          value={server.port || ''}
          onChange={(e) => setServer({ ...server, port: e.target.value })}
        />
      </Tooltip>
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
      {localPlexServer ? (
        <>
          <Card component={motion.div} whileHover={{ scale: 1.02 }} transition={{ type: 'spring', stiffness: 300 }}>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h4" gutterBottom>
                  {localPlexServer.name}
                </Typography>
                <Box>
                  <IconButton onClick={handleDeleteServer}>
                    <DeleteIcon />
                  </IconButton>
                </Box>
              </Box>
              <Typography variant="subtitle1" gutterBottom>
                Endpoint: {localPlexServer.endpoint}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                Port: {localPlexServer.port}
              </Typography>
              <Chip
                label={localPlexServer.errorState ? 'Error' : 'Connected'}
                color={localPlexServer.errorState ? 'error' : 'success'}
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>

          <Typography variant="h5" gutterBottom sx={{ mt: 4, mb: 2 }}>
            Libraries
          </Typography>
          <Grid container spacing={3}>
            {localPlexServer.directories?.map((directory: DirectoryPublic) => (
              <Grid item xs={12} sm={6} md={4} key={directory.uuid}>
                <Card
                  component={motion.div}
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: 'spring', stiffness: 300 }}
                >
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      {getLibraryIcon(directory.title)}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {directory.title}
                      </Typography>
                    </Box>
                    <Typography variant="body2" color="textSecondary">
                      UUID: {directory.uuid}
                    </Typography>
                    {directory.locations?.map((location: { path: string }, index: number) => (
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
            <Typography variant="h5" gutterBottom>
              No Plex Server Configured
            </Typography>
          </CardContent>
        </Card>
      )}

      {!localPlexServer && (
        <Box mt={2}>
          <Button startIcon={<AddIcon />} variant="contained" color="primary" onClick={handleAddServer}>
            Add Plex Server
          </Button>
        </Box>
      )}

      <Dialog open={isAddModalOpen} onClose={handleCloseAddModal}>
        <DialogTitle>Add Plex Server</DialogTitle>
        <DialogContent>
          {errorMessage && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {errorMessage}
            </Alert>
          )}
          {renderServerForm(newServer, setNewServer)}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAddModal}>Cancel</Button>
          <Button onClick={handleSaveNewServer} color="primary">
            Add
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PlexServerDashboard;
