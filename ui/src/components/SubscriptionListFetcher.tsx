'use client';

import React, { useState, useEffect } from 'react';
import { Subscription } from '@/types/subscriptionTypes';
import '@css/subscriptions.css';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const SubscriptionList: React.FC = () => {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSubscriptions = async () => {
      try {
        const response = await fetch('/api/subscription');
        const data: Subscription[] = await response.json();
        setSubscriptions(data);
      } catch (error) {
        setError('Failed to fetch subscriptions');
      } finally {
        setLoading(false);
      }
    };

    fetchSubscriptions();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <TableContainer component={Paper} class="box">
      <Table sx={{ minWidth: 1050 }} aria-label="subscription-table">
        <TableHead>
          <TableRow>
            <TableCell></TableCell>
            <TableCell align="right">Channel Name</TableCell>
            <TableCell align="right">Link</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {subscriptions.map((subscription) => (
            <TableRow key={subscription.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell align="right">
                <img src={`data:image/png;base64,${subscription.image}`} style={{ width: '50px', height: 'auto' }} />
              </TableCell>
              <TableCell align="right">{subscription.title}</TableCell>
              <TableCell align="right">
                <a href={subscription.url} target="_blank" rel="noopener noreferrer">
                  {subscription.url}
                </a>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SubscriptionList;
