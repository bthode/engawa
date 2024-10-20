import { DirectoryPublic } from '@/api/models';
import { Subscription } from '@/api/models/Subscription';
import { List, ListItem, ListItemText, Paper, Typography } from '@mui/material';
import Grid from '@mui/material/Grid2';
import React from 'react';
import { Filter } from './FilterStep';
import { RetentionPolicy } from './RetentionPolicyStep';

interface SummarySectionProps {
  title: string;
  content: React.ReactNode;
}

export interface PlexLibraryDestination {
  directoryId: number;
  locationId: number;
}

const SummarySection: React.FC<SummarySectionProps> = ({ title, content }) => (
  <>
    <Grid>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
    </Grid>
    <Grid>{content}</Grid>
  </>
);

interface SubscriptionSummaryProps {
  subscription: Subscription | null;
  youtubeLink: string;
  filters: Filter[];
  retentionPolicy: RetentionPolicy;
  directories: DirectoryPublic[];
  PlexLibraryDestination: PlexLibraryDestination;
}

const transformLastNVideoHelperText = (value: number | Date | string): string => {
  switch (typeof value) {
    case 'number':
      return `Retain the last ${value} videos`;
    case 'object':
      if (value instanceof Date) {
        return `Retain videos since ${value.toDateString()}`;
      }
      return 'N/A';
    case 'string':
      return 'N/A';
  }
};

const produceRetentionPolicySummaryText = (retentionPolicy: RetentionPolicy): string => {
  switch (retentionPolicy.type) {
    case 'RetainAll':
      return 'Retain all videos';
    case 'LastNEntities':
      return retentionPolicy.value !== undefined
        ? transformLastNVideoHelperText(retentionPolicy.value)
        : 'Invalid value';
    case 'EntitiesSince':
      return retentionPolicy.value !== undefined
        ? transformLastNVideoHelperText(retentionPolicy.value)
        : 'Invalid value';
    default:
      return 'N/A';
  }
};

const SubscriptionSummary: React.FC<SubscriptionSummaryProps> = ({
  subscription,
  youtubeLink,
  filters,
  retentionPolicy,
  directories,
  PlexLibraryDestination,
}) => {
  const selectedDirectory = directories.find((dir) => dir.key === PlexLibraryDestination.directoryId);
  const selectedLocation = selectedDirectory?.locations?.find((loc) => loc.id === PlexLibraryDestination.locationId);

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        Subscription Summary
      </Typography>
      <Grid container spacing={2}>
        <SummarySection
          title="Channel"
          content={
            <>
              <Typography variant="body1">{subscription?.title}</Typography>
              <Typography variant="body2">{youtubeLink}</Typography>
            </>
          }
        />
      </Grid>
      <Grid>
        <SummarySection
          title="Filters"
          content={
            <List dense>
              {filters.length === 0 ? (
                <ListItem>
                  <ListItemText primary="No filters applied" />
                </ListItem>
              ) : (
                filters.map((filter, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={`${filter.criteria} ${filter.operand} ${filter.value}`} />
                  </ListItem>
                ))
              )}
            </List>
          }
        />
      </Grid>
      <Grid>
        <SummarySection
          title="Retention Policy"
          content={<Typography variant="body1">{produceRetentionPolicySummaryText(retentionPolicy)}</Typography>}
        />
      </Grid>
      <Grid>
        <SummarySection
          title="Plex Location"
          content={
            selectedDirectory && selectedLocation ? (
              <>
                <Typography variant="body1">
                  <strong>Library:</strong> {selectedDirectory.title}
                </Typography>
                <Typography variant="body2">
                  <strong>Path:</strong> {selectedLocation.path}
                </Typography>
              </>
            ) : (
              <Typography variant="body1" color="error">
                No Plex location selected
              </Typography>
            )
          }
        />
      </Grid>
    </Paper>
  );
};

export default SubscriptionSummary;
