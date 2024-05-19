'use client'
import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import axios from 'axios';
import CircularProgress from '@mui/material/CircularProgress';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Link from '@mui/material/Link';

const urlPattern = /^(https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:@([\w-]+)|channel\/)|youtu\.be\/)([\w-]+)/i;


const UrlTextField = () => {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [imageLink, setImageLink] = useState('');
  const [rssLink, setRssLink] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setUrl(value);
    debounce(validateUrl, 500)(value);
  };
  
  const validateUrl = (value: string) => {
    if (!urlPattern.test(value)) {
      setError('Invalid URL');
    } else {
      setError('');
      fetchRss(value);
    }
  };
  
  const fetchRss = async (url: string) => {
    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:8000/fetch_rss', {
      channel_url: url,
    });
    setRssLink(response.data.rss_link);
    setImageLink(response.data.image_link);
    setTitle(response.data.title);
    setDescription(response.data.description);
    setUrl('');
    setError('');
  } catch (error: any) {
    setError(error.message);
    alert(`Error: ${error.message}`);
  } finally {
    setLoading(false);
  }
};

const debounce = (func: Function, delay: number) => {
  let timeoutId: ReturnType<typeof setTimeout>;
  return (...args: any[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

return (
  <div>
  <TextField
  fullWidth
  autoFocus
  autoComplete="off"
  placeholder="Enter URL"
  value={url}
  onChange={handleChange}
  error={!!error}
  helperText={error}
  disabled={loading}
  InputProps={{
    endAdornment: loading && <CircularProgress size={20} />,
  }}
  />
  {title && rssLink && imageLink && (
    <Card sx={{ maxWidth: 345 }}>
    <CardMedia
    sx={{ height: 140 }}
    image={imageLink}
    title={title}
    />
<CardContent>
  <Typography gutterBottom variant="h5" component="div">
    {title}
  </Typography>
  <Typography variant="body2" color="text.secondary">
    Description: {description}
  </Typography>
  <Typography variant="body2" color="text.secondary">
    <Link href={rssLink}>RSS Feed</Link>
  </Typography>
</CardContent>
  </Card>
)}
</div>
);
};

export default UrlTextField;
