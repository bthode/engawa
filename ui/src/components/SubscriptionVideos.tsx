import React from 'react';
import { Typography, Box, Paper } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { TableVirtuoso, TableComponents } from 'react-virtuoso';
import { Video } from '@/types/videoTypes';
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

  React.useEffect(() => {
    const fetchSubscriptionAndVideos = async () => {
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
    };

    fetchSubscriptionAndVideos();
  }, [subscriptionId]);

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error || !subscription) {
    return <Typography color="error">{error || 'Subscription not found'}</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {subscription.title}
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        URL: {subscription.url}
      </Typography>
      <Typography variant="body2" paragraph>
        {subscription.description}
      </Typography>

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
