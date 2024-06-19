'use client';
import React, { useState } from 'react';
import { TextField, MenuItem, Button, Grid, Box } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

const FormComponent: React.FC = () => {
  const [subscriptionUrl, setSubscriptionUrl] = useState<string>('');
  const [retentionType, setRetentionType] = useState<string>('');
  const [retentionValue, setRetentionValue] = useState<string | number | null>(null);
  const [dateFrom, setDateFrom] = useState<Date | null>(null);
  const [durationUnit, setDurationUnit] = useState<string>('');
  const [durationValue, setDurationValue] = useState<number | null>(null);
  const [durationFilter, setDurationFilter] = useState<number | null>(null);
  const [durationFilterType, setDurationFilterType] = useState<string>('greater');
  const [titleFilter, setTitleFilter] = useState<string>('');

  const retentionTypes = [
    { value: 'dateFrom', label: 'Date From' },
    { value: 'count', label: 'Count' },
    { value: 'dateWindow', label: 'Date Window' },
    { value: 'all', label: 'All' },
  ];

  const durationUnits = [
    { value: 'days', label: 'Days' },
    { value: 'weeks', label: 'Weeks' },
    { value: 'months', label: 'Months' },
    { value: 'years', label: 'Years' },
  ];

  const durationFilterTypes = [
    { value: 'greater', label: 'Greater Than' },
    { value: 'lesser', label: 'Less Than' },
  ];

  const validateUrl = (url: string): boolean => {
    const urlPattern =
      /^(https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:c\/|user\/|playlist\?list=|@([\w-]+)|channel\/|)?|youtu\.be\/)([\w-]+)/i;
    return urlPattern.test(url);
  };

  const handleSubscriptionUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSubscriptionUrl(event.target.value);
  };

  const handleRetentionTypeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRetentionType(event.target.value);
    setRetentionValue(null);
    setDateFrom(null);
    setDurationUnit('');
    setDurationValue(null);
  };

  const handleDateFromChange = (date: Date | null) => {
    setDateFrom(date);
  };

  const handleDurationUnitChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDurationUnit(event.target.value);
  };

  const handleDurationValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDurationValue(Number(event.target.value));
  };

  const handleDurationFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDurationFilter(Number(event.target.value));
  };

  const handleDurationFilterTypeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setDurationFilterType(event.target.value);
  };

  const handleTitleFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTitleFilter(event.target.value);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Box component="form" noValidate autoComplete="off">
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Subscription URL"
              value={subscriptionUrl}
              onChange={handleSubscriptionUrlChange}
              error={!validateUrl(subscriptionUrl) && subscriptionUrl !== ''}
              helperText={!validateUrl(subscriptionUrl) && subscriptionUrl !== '' ? 'Invalid URL' : ''}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              select
              label="Retention Type"
              value={retentionType}
              onChange={handleRetentionTypeChange}
            >
              {retentionTypes.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          {retentionType === 'dateFrom' && (
            <Grid item xs={12}>
              <DatePicker
                label="Date From"
                value={dateFrom}
                onChange={handleDateFromChange}
                renderInput={(params) => <TextField fullWidth {...params} />}
                maxDate={new Date()}
              />
            </Grid>
          )}
          {retentionType === 'count' && (
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Count"
                type="number"
                inputProps={{ min: 1, max: 999 }}
                value={retentionValue ?? ''}
                onChange={(e) => setRetentionValue(Number(e.target.value))}
              />
            </Grid>
          )}
          {retentionType === 'dateWindow' && (
            <Grid item xs={6}>
              <TextField
                fullWidth
                select
                label="Duration Unit"
                value={durationUnit}
                onChange={handleDurationUnitChange}
              >
                {durationUnits.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
          )}
          {retentionType === 'dateWindow' && (
            <Grid item xs={6}>
              <TextField
                fullWidth
                label="Duration Value"
                type="number"
                inputProps={{ min: 1 }}
                value={durationValue ?? ''}
                onChange={handleDurationValueChange}
              />
            </Grid>
          )}
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Duration Filter (minutes)"
              type="number"
              value={durationFilter ?? ''}
              onChange={handleDurationFilterChange}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              select
              label="Duration Filter Type"
              value={durationFilterType}
              onChange={handleDurationFilterTypeChange}
            >
              {durationFilterTypes.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth label="Title Contains" value={titleFilter} onChange={handleTitleFilterChange} />
          </Grid>
        </Grid>
        <Box mt={2}>
          <Button variant="contained" color="primary" type="submit">
            Submit
          </Button>
        </Box>
      </Box>
    </LocalizationProvider>
  );
};

export default FormComponent;
