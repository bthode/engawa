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
  IconButton,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import axios from 'axios';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import DeleteIcon from '@mui/icons-material/Delete';
import { savePlexServer } from '../../actions/savePlexServer';
import { PlexServer } from '@/types/plexTypes';

async function getPlexData() {
  // TODO: Replace with server action?
  const res = await fetch('/api/plex_server/');
  if (!res.ok) {
    throw new Error('Failed to fetch Plex data');
  }
  return res.json();
}

const Plex: React.FC = () => {
  const [plexData, setPlexData] = useState<PlexServer[]>([]);
  const [open, setOpen] = useState(false);
  const [endpoint, setEndPoint] = useState('10.1.1.10');
  const [port, setPort] = useState('32400');
  const [token, setToken] = useState('nyyWbP6RfyTJZ1bSCRRZ');
  const [loading, setLoading] = useState(true);
  const [openLibraries, setOpenLibraries] = useState(false);

  const handleClick = () => {
    setOpenLibraries(!openLibraries);
  };

  useEffect(() => {
    getPlexData()
      .then((data) => {
        setPlexData(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setPlexData([]);
        setLoading(false);
      });
  }, []);

  const handleAddClick = () => {
    setOpen(true);
  };

  const handleTestClick = async () => {
    const response = await axios.get(`http://${endpoint}:32400/library/sections?X-Plex-Token=${token}`);
    if (response.status === 200) {
      alert('Success');
    }
  };

  const handleSaveClick = async () => {
    try {
      const data = { endpoint, token, port, name: 'Plex' };
      const newData = await savePlexServer(data);

      setPlexData((prevData) => [...prevData, ...newData]);
      setOpen(false);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Navigation>
      {loading ? (
        <div>Loading...</div>
      ) : plexData && plexData.length > 0 ? (
        plexData.map((server) => (
          <List component="nav" key={server.id}>
            <ListItem>
              <ListItemText primary={`Server Host: ${server.endpoint}`} />
              <br />
              <ListItemText primary={`Name: ${server.name} `} />
              <IconButton
                edge="end"
                aria-label="delete"
                style={{ color: 'white' }}
                onClick={async () => {
                  const response = await fetch(`/api/plex_server/${server.id}`, {
                    method: 'DELETE',
                  });
                  if (!response.ok) {
                    console.error('Error:', response.statusText);
                  } else {
                    console.log('Deleted:', server.id);
                    setPlexData(plexData.filter((plex) => plex.id !== server.id)); // Remove the deleted server from state
                  }
                }}
              >
                <DeleteIcon />
              </IconButton>
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
                {server.directories && server.directories.length > 0 ? (
                  server.directories.map((directory) => (
                    <ListItem key={directory.uuid}>
                      <ListItemText primary={directory.title} />
                    </ListItem>
                  ))
                ) : (
                  <ListItem key="no-directories">
                    <ListItemText primary="No directories available" />
                  </ListItem>
                )}
              </List>
            </Collapse>
          </List>
        ))
      ) : (
        <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleAddClick}>
          Add Plex Server
        </Button>
      )}
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Add Plex Server</DialogTitle>
        <DialogContent>
          <InputLabel shrink>Endpoint</InputLabel>
          <Tooltip title="Use the endpoint as accessible from where Engawa is running.">
            <TextField
              value={endpoint}
              onChange={(e) => setEndPoint(e.target.value)}
              fullWidth
              placeholder="192.168.0.20"
            />
          </Tooltip>
          <Box mt={2}>
            <InputLabel shrink>Access Token</InputLabel>
            <TextField
              type="password"
              value={token}
              onChange={(e) => setToken(e.target.value)}
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
          <InputLabel shrink>Port</InputLabel>
          <TextField value={port} onChange={(e) => setPort(e.target.value)} fullWidth />
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
