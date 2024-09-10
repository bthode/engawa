import React from 'react';
import { Typography, Box, Paper, Button } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { TableVirtuoso, TableComponents } from 'react-virtuoso';
import { Video, VideoStatus } from '@/types/videoTypes';
import { Subscription } from '@/types/subscriptionTypes';

interface SubscriptionVideosProps {
  subscriptionId: string;
}

interface ColumnData {
  dataKey: keyof Video;
  label: string;
  numeric?: boolean;
  width: number;
  duration?: number;
  status?: VideoStatus;
}

const columns: ColumnData[] = [
  {
    width: 250,
    label: 'Title',
    dataKey: 'title',
  },
  {
    width: 150,
    label: 'Author',
    dataKey: 'author',
  },
  {
    width: 100,
    label: 'Published',
    dataKey: 'published',
  },
  {
    width: 100,
    label: 'Link',
    dataKey: 'link',
  },
  {
    width: 100,
    label: 'Status',
    dataKey: 'status',
  },
  {
    width: 100,
    label: 'Duration',
    dataKey: 'duration',
  },
];

const VirtuosoTableComponents: TableComponents<Video> = {
  Scroller: React.forwardRef<HTMLDivElement>((props, ref) => (
    <TableContainer component={Paper} {...props} ref={ref} />
  )),
  Table: (props) => (
    <Table {...props} sx={{ borderCollapse: 'separate', tableLayout: 'fixed' }} />
  ),
  TableHead,
  TableRow,
  TableBody: React.forwardRef<HTMLTableSectionElement>((props, ref) => (
    <TableBody {...props} ref={ref} />
  )),
};

function fixedHeaderContent() {
  return (
    <TableRow>
      {columns.map((column) => (
        <TableCell
          key={column.dataKey}
          variant="head"
          align={column.numeric || false ? 'right' : 'left'}
          style={{ width: column.width }}
          sx={{ backgroundColor: 'background.paper' }}
        >
          {column.label}
        </TableCell>
      ))}
    </TableRow>
  );
}

function rowContent(_index: number, row: Video) {
  return (
    <React.Fragment>
      {columns.map((column) => (
        <TableCell
          key={column.dataKey}
          align={column.numeric || false ? 'right' : 'left'}
        >
          {column.dataKey === 'link' ? (
            <a href={row[column.dataKey]} target="_blank" rel="noopener noreferrer">
              Watch on YouTube
            </a>
          ) : column.dataKey === 'published' ? (
            new Date(row[column.dataKey]).toLocaleDateString()
          ) : column.dataKey === 'duration' ? (
            row[column.dataKey] ? 
              // Convert the number directly to seconds, then to ISO string
              new Date(row[column.dataKey] * 1000).toISOString().slice(11, 19) :
              'N/A'
          ) : (
            row[column.dataKey]
          )}
        </TableCell>
      ))}
    </React.Fragment>
  );
}

const SubscriptionVideos: React.FC<SubscriptionVideosProps> = ({ subscriptionId }) => {
  const [subscription, setSubscription] = React.useState<Subscription | null>(null);
  const [videos, setVideos] = React.useState<Video[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  // Function to fetch subscription and videos data
  const fetchSubscriptionAndVideos = React.useCallback(async () => {
    try {
      setLoading(true);
      const [subscriptionResponse, videosResponse] = await Promise.all([
        fetch(`/api/subscription/${subscriptionId}`),
        fetch(`/api/subscription/${subscriptionId}/videos`),
      ]);

      if (!subscriptionResponse.ok || !videosResponse.ok) {
        throw new Error('Failed to fetch data');
      }

      const subscriptionData: Subscription = await subscriptionResponse.json();
      const videosData: Video[] = await videosResponse.json();

      setSubscription(subscriptionData);
      setVideos(videosData);
      setError(null);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to load subscription data. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, [subscriptionId]);

  // Initial data fetch
  React.useEffect(() => {
    fetchSubscriptionAndVideos();
  }, [fetchSubscriptionAndVideos]);

  // Refresh button handler
  const handleRefresh = () => {
    fetchSubscriptionAndVideos();
  };

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error || !subscription) {
    return <Typography color="error">{error || 'Subscription not found'}</Typography>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">
          {subscription.title}
        </Typography>
        <Button
          variant="contained"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>
      <Typography variant="h5" gutterBottom>
        Videos
      </Typography>
      <Paper style={{ height: 800, width: '100%' }}>
        <TableVirtuoso
          data={videos}
          components={VirtuosoTableComponents}
          fixedHeaderContent={fixedHeaderContent}
          itemContent={rowContent}
        />
      </Paper>
    </Box>
  );
};

export default SubscriptionVideos;
