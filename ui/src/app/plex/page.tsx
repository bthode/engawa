'use client';
import React, { useState, useEffect } from 'react';
import Navigation from '../navigation';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  ListItem,
  ListItemText,
  Collapse,
  List,
  ListItemIcon,
  Tooltip,
  Link,
  InputLabel,
  Box,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import axios from 'axios';
import { ExpandLess, ExpandMore } from '@mui/icons-material';

const Plex: React.FC = () => {
  const [plexData, setPlexData] = useState<PlexData | null>(null);
  const [open, setOpen] = useState(false);
  const [hostname, setHostname] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [loading, setLoading] = useState(true);
  const [openLibraries, setOpenLibraries] = useState(false);

  const handleClick = () => {
    setOpenLibraries(!openLibraries);
  };

  interface PlexData {
    ip: string;
    libraries: string[];
  }
  const fetchPlexData = async (simulate: boolean) => {
    if (simulate) {
      // Simulate a delay with setTimeout wrapped in a promise
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Placeholder data
      const data = {
        ip: '192.168.1.100',
        libraries: ['Movies', 'TV Shows', 'Music'],
      };

      setPlexData(data);
    } else {
      setPlexData(null);
    }

    setLoading(false);
  };

  //   const fetchPlexData = async () => {
  //     const response = await axios.get('/plex');
  //     setPlexData(response.data);
  //   };

  useEffect(() => {
    fetchPlexData(false);
  }, []);

  const handleAddClick = () => {
    setOpen(true);
  };

  const handleTestClick = async () => {
    const response = await axios.get(`http://${hostname}:32400/library/sections?X-Plex-Token=${accessToken}`);
    if (response.status === 200) {
      alert('Success');
    }
  };

  const handleSaveClick = async () => {
    await axios.post('/plex', { hostname, connectionString: accessToken });
    fetchPlexData(true);
    setOpen(false);
  };

  return (
    <Navigation>
      {loading ? (
        <div>Loading...</div>
      ) : plexData ? (
        <List component="nav">
          <ListItem>
            <ListItemText primary={`Server Host: ${plexData.ip}`} />
          </ListItem>
          <ListItem button onClick={handleClick}>
            {openLibraries ? (
              <ListItemIcon>
                <ExpandMore style={{ color: 'white' }} />
              </ListItemIcon>
            ) : (
              <ListItemIcon>
                <ExpandLess style={{ color: 'white' }} />
              </ListItemIcon>
            )}
            <ListItemText primary="Libraries" />
          </ListItem>
          <Collapse in={openLibraries} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {plexData.libraries.map((library, index) => (
                <ListItem key={index}>
                  <ListItemText primary={library} />
                </ListItem>
              ))}
            </List>
          </Collapse>
        </List>
      ) : (
        <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleAddClick}>
          Add Plex Server
        </Button>
      )}
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Add Plex Server</DialogTitle>
        <DialogContent>
          <InputLabel shrink>Hostname/IP</InputLabel>
          <Tooltip title="Use the endpoint as accessible from where Engawa is running.">
            <TextField
              value={hostname}
              onChange={(e) => setHostname(e.target.value)}
              fullWidth
              placeholder="http://192.168.0.20:32400"
            />
          </Tooltip>
          <Box mt={2}>
            <InputLabel shrink>Access Token</InputLabel>
            <TextField
              value={accessToken}
              onChange={(e) => setAccessToken(e.target.value)}
              fullWidth
              placeholder="nyyWbP6RfyTJZ1b....."
            />
          </Box>
          <Link
            href="https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/"
            target="_blank"
            rel="noopener"
          >
            How to find your Plex Access Token
          </Link>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleTestClick}>Test</Button>
          <Button onClick={handleSaveClick}>Save</Button>
        </DialogActions>
      </Dialog>
    </Navigation>
  );
};

export default Plex;
