/* eslint-disable @next/next/no-img-element */
'use client';
import React, { useState } from 'react';
import '@css/subscriptions.css';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useSubscriptions } from './SubscriptionContext';
import DeleteIcon from '@mui/icons-material/Delete';
import { IconButton } from '@mui/material';
import SyncIcon from '@mui/icons-material/Sync';
import CircularProgress from '@mui/material/CircularProgress';

interface SubscriptionListProps {
  onSubscriptionSelect: (subscriptionId: string) => void;
}

const SubscriptionList: React.FC<SubscriptionListProps> = ({ onSubscriptionSelect }) => {
  const { subscriptions, loading, error, syncSubscription, deleteSubscription } = useSubscriptions();
  const [syncingIds, setSyncingIds] = useState<Set<string>>(new Set());

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  const handleDelete = async (id: string, event: React.MouseEvent) => {
    event.stopPropagation();
    await deleteSubscription(id);
  };

  async function handleSync(id: string, event: React.MouseEvent): Promise<void> {
    event.stopPropagation();
    setSyncingIds((prev) => new Set(prev).add(id));
    try {
      await syncSubscription(id);
    } finally {
      setSyncingIds((prev) => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  }

  return (
    <TableContainer component={Paper} className="box">
      <Table sx={{ minWidth: 1050 }} aria-label="subscription-table">
        <TableHead>
          <TableRow>
            <TableCell></TableCell>
            <TableCell align="right">Channel Name</TableCell>
            <TableCell align="right">Link</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {subscriptions.map((subscription) => (
            <TableRow
              key={subscription.id}
              sx={{ '&:last-child td, &:last-child th': { border: 0 }, cursor: 'pointer' }}
              onClick={() => onSubscriptionSelect(subscription.id)}
            >
              <TableCell align="right">
                <img
                  src={`data:image/png;base64,${subscription.image}`}
                  style={{ width: '50px', height: 'auto' }}
                  alt={subscription.title}
                />
              </TableCell>
              <TableCell align="right">{subscription.title}</TableCell>
              <TableCell align="right">
                <a href={subscription.url} target="_blank" rel="noopener noreferrer">
                  {subscription.url}
                </a>
              </TableCell>
              <TableCell align="right">
                <IconButton
                  aria-label="sync"
                  onClick={(e) => handleSync(subscription.id, e)}
                  disabled={syncingIds.has(subscription.id)}
                >
                  {syncingIds.has(subscription.id) ? <CircularProgress size={24} /> : <SyncIcon />}
                </IconButton>
              </TableCell>
              <TableCell align="right">
                <IconButton aria-label="delete" onClick={(e) => handleDelete(subscription.id, e)}>
                  <DeleteIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SubscriptionList;
