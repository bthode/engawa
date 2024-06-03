'use client';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button, Card, CardContent, CardMedia, Grid, Link, Slider, Typography } from '@mui/material';
import YouTubeIcon from '@mui/icons-material/YouTube';
import { differenceInDays, formatDistanceToNow, parseISO } from 'date-fns';

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
  thumbnail: VideoThumbnail;
}

const VideoItemComponent: React.FC<{ video: VideoItem; selectedDateRange: number }> = ({
  video,
  selectedDateRange,
}) => {
  const formatDate = (date: string) => {
    const videoDate = parseISO(date);
    return formatDistanceToNow(videoDate, { addSuffix: true });
  };

  const videoDate = parseISO(video.published);
  const mark = marks.find((mark) => mark.value === selectedDateRange);
  const isDimmed = mark && differenceInDays(new Date(), videoDate) > mark.days;

  return (
    <Card
      sx={{
        display: 'flex',
        width: '100%',
        boxShadow: 'none',
        border: '1px solid white',
        marginBottom: 2,
        opacity: isDimmed ? 0.5 : 1,
      }}
    >
      <CardMedia
        component="img"
        sx={{ width: '30%', height: '100%', objectFit: 'cover', border: '1px solid black' }}
        image={video.thumbnail.url}
        alt="Video Thumbnail"
      />
      <CardContent
        sx={{
          flex: '1 0 auto',
          padding: '16px !important',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
        }}
      >
        <div>
          <Typography variant="subtitle2" component="span" sx={{ fontWeight: 'bold' }}>
            {video.author}
          </Typography>
          <Typography variant="body2" component="div" sx={{ marginLeft: 1 }}>
            - {video.title}
          </Typography>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <Typography variant="caption" color="black" sx={{ fontWeight: 'bold' }}>
            {formatDate(video.published)}
          </Typography>
          <Link href={video.link} target="_blank" rel="noopener noreferrer">
            <YouTubeIcon color="error" />
          </Link>
        </div>
      </CardContent>
    </Card>
  );
};

// TODO: We will likely need to "fudge" these days values a bit to align with the date-fns generated dates
// Or find another solution so a video showing an age of 2 months and 1 day is not dimmed when 2 months is selected
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

const VideoList: React.FC = () => {
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [selectedDateRange, setSelectedDateRange] = useState(marks[0].value);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/get_videos', {
          params: {
            rss_url: 'https://www.youtube.com/feeds/videos.xml?channel_id=UCCD4-G3Aokt2sM7TYQV2HmA',
          },
        });
        if (response.data && response.data.length) {
          setVideos(response.data);
        }
      } catch (error) {
        console.error('Failed to fetch videos', error);
      }
    };

    fetchData().catch((error) => console.error('Error in fetchData:', error));
  }, []);

  return (
    <div>
      <Button variant="contained" color="primary" sx={{ borderRadius: '50px', fontWeight: 'bold', margin: '20px 0' }}>
        Save
      </Button>
      <Grid container spacing={0} sx={{ maxWidth: 740, margin: 'auto' }}>
        <Slider
          aria-label="Restricted values"
          getAriaValueText={valuetext}
          step={null}
          onChange={(event, newValue) => setSelectedDateRange(Array.isArray(newValue) ? newValue[0] : newValue)}
          valueLabelDisplay="on"
          valueLabelFormat={valuetext}
          marks={marks}
          sx={{ marginTop: '30px' }}
        />
        {videos.map((video, index) => (
          <Grid item xs={12} key={index}>
            <VideoItemComponent video={video} selectedDateRange={selectedDateRange} />
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default VideoList;
