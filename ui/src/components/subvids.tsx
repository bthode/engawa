import React from 'react';
import { Typography, Box, Paper } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import { TableVirtuoso, TableComponents } from 'react-virtuoso';
import { Video, VideoStatus } from '@/types/videoTypes';

interface SubscriptionVideosProps {
  videos: Video[];
  subscriptionTitle: string;
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
  Scroller: React.forwardRef(function VirtuosoScroller(props, ref) {
    return <TableContainer component={Paper} {...props} ref={ref} />;
  }),
  Table: function VirtuosoTable(props) {
    return <Table {...props} sx={{ borderCollapse: 'separate', tableLayout: 'fixed' }} />;
  },
  TableHead: React.forwardRef(function VirtuosoTableHead(props, ref) {
    return <TableHead {...props} ref={ref} />;
  }),
  TableRow,
  TableBody: React.forwardRef(function VirtuosoTableBody(props, ref) {
    return <TableBody {...props} ref={ref} />;
  }),
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
        <TableCell key={column.dataKey} align={column.numeric || false ? 'right' : 'left'}>
          {column.dataKey === 'link' ? (
            <a href={row[column.dataKey]} target="_blank" rel="noopener noreferrer">
              Watch on YouTube
            </a>
          ) : column.dataKey === 'published' ? (
            new Date(row[column.dataKey]).toLocaleDateString()
          ) : column.dataKey === 'duration' ? (
            row[column.dataKey] ? (
              new Date(row[column.dataKey] * 1000).toISOString().slice(11, 19)
            ) : (
              'N/A'
            )
          ) : (
            row[column.dataKey]
          )}
        </TableCell>
      ))}
    </React.Fragment>
  );
}

const SubscriptionVideos: React.FC<SubscriptionVideosProps> = ({ videos, subscriptionTitle }) => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h4">{subscriptionTitle}</Typography>
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
