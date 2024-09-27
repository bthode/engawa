import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  Link,
  Paper,
  Slider,
  Typography,
  Table,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
} from '@mui/material';
import { differenceInDays, formatDistanceToNow, parseISO } from 'date-fns';
import { TableVirtuoso, TableComponents } from 'react-virtuoso';

interface VideoThumbnail {
  url: string;
  width: string;
  height: string;
}

interface VideoItem {
  title: string;
  published: string;
  video_id: string;
  link: string;
  author: string;
  thumbnail_url: VideoThumbnail;
}

const marks = [
  { value: 0, label: 'Forever', days: Infinity },
  { value: 8, label: '3 years', days: 365 * 3 },
  { value: 16, label: '2 years', days: 365 * 2 },
  { value: 24, label: '1 year', days: 365 },
  { value: 31, label: '6 months', days: 180 },
  { value: 39, label: '3 months', days: 90 },
  { value: 47, label: '2 months', days: 60 },
  { value: 54, label: '1 month', days: 30 },
  { value: 62, label: '3 weeks', days: 21 },
  { value: 70, label: '2 weeks', days: 14 },
  { value: 77, label: '1 week', days: 7 },
  { value: 85, label: '3 days', days: 3 },
  { value: 92, label: '2 days', days: 2 },
  { value: 98, label: '1 day', days: 1 },
  { value: 100, label: 'Now', days: 0 },
];

function valuetext(value: number) {
  const mark = marks.find((mark) => mark.value === value);
  return mark ? mark.label : '';
}

const formatDate = (date: string) => {
  const videoDate = parseISO(date);
  return formatDistanceToNow(videoDate, { addSuffix: true });
};

const VirtuosoTableComponents: TableComponents<VideoItem> = {
  Scroller: React.forwardRef<HTMLDivElement>((props, ref) => <div {...props} ref={ref} />),
  Table: (props) => <Table {...props} style={{ borderCollapse: 'separate' }} />,
  TableHead,
  TableRow,
  TableBody,
};

const YoutubeCardFetcher: React.FC = () => {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [selectedDateRange, setSelectedDateRange] = useState(marks[0].value);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/get_videos', {
          params: {
            rss_url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UConVfxXodg78Tzh5nNu85Ew',
          },
        });
        if (response.data && response.data.length) {
          setVideos(response.data);
        }
        setError(null);
      } catch (error) {
        console.error('Failed to fetch videos', error);
        setError('Failed to fetch videos. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const isDimmed = (publishedDate: string) => {
    if (selectedDateRange === 0) return false;
    else if (selectedDateRange === Infinity) return true;
    else {
      const videoDate = parseISO(publishedDate);
      const mark = marks.find((mark) => mark.value === selectedDateRange);
      return mark && differenceInDays(new Date(), videoDate) > mark.days;
    }
  };

  const rowContent = (_index: number, video: VideoItem) => (
    <React.Fragment>
      <TableCell style={{ opacity: isDimmed(video.published) ? 0.5 : 1 }}>
        <Typography variant="subtitle2" component="span" sx={{ fontWeight: 'bold' }}>
          {video.author}
        </Typography>
        <Typography variant="body2" component="div" sx={{ marginLeft: 1 }}>
          - {video.title}
        </Typography>
      </TableCell>
      <TableCell style={{ opacity: isDimmed(video.published) ? 0.5 : 1 }}>
        <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
          {formatDate(video.published)}
        </Typography>
      </TableCell>
      <TableCell style={{ opacity: isDimmed(video.published) ? 0.5 : 1 }}>
        <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
          54:31
        </Typography>
      </TableCell>
    </React.Fragment>
  );

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', paddingY: 4, display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Paper elevation={3} sx={{ padding: 2, marginBottom: 4 }}>
        <Button
          variant="contained"
          color="primary"
          sx={{
            borderRadius: '50px',
            fontWeight: 'bold',
            marginBottom: 2,
          }}
        >
          Next
        </Button>
        <Typography variant="h6" gutterBottom>
          Filter videos by date
        </Typography>
        <Slider
          aria-label="Date range filter"
          value={selectedDateRange}
          onChange={(_, newValue) => setSelectedDateRange(Array.isArray(newValue) ? newValue[0] : newValue)}
          valueLabelDisplay="auto"
          valueLabelFormat={valuetext}
          step={null}
          marks={marks}
        />
      </Paper>
      <Box sx={{ flexGrow: 1, overflow: 'hidden' }}>
        <TableVirtuoso
          data={videos}
          components={VirtuosoTableComponents}
          fixedHeaderContent={() => (
            <TableRow style={{ background: 'black' }}>
              <TableCell style={{ width: '60%' }}>Video</TableCell>
              <TableCell style={{ width: '30%' }}>Published</TableCell>
              <TableCell style={{ width: '10%' }}>Duration</TableCell>
            </TableRow>
          )}
          itemContent={rowContent}
        />
      </Box>
    </Box>
  );
};

export default YoutubeCardFetcher;
