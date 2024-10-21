import { DirectoryPublic } from '@/api/models/DirectoryPublic';
import { Subscription } from '@/api/models/Subscription';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';
import { Box, Divider, List, ListItem, ListItemIcon, ListItemText, Paper, Typography } from '@mui/material';
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

const SummarySection: React.FC<SummarySectionProps> = ({ title, content }) => (
  <Box mb={3}>
    <Typography variant="h6" gutterBottom>
      {title}
    </Typography>
    <Box ml={2}>{content}</Box>
  </Box>
);

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
    <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
      <Typography variant="h4" gutterBottom align="center" mb={4}>
        Subscription Summary
      </Typography>

      <SummarySection
        title="Channel Information"
        content={
          <>
            <Typography variant="body1">
              <strong>Title:</strong> {subscription?.title}
            </Typography>
            <Typography variant="body1" mt={1}>
              <strong>YouTube Link:</strong> {youtubeLink}
            </Typography>
          </>
        }
      />

      <Divider sx={{ my: 3 }} />

      <SummarySection
        title="Applied Filters"
        content={
          <List dense disablePadding>
            {filters.length === 0 ? (
              <ListItem>
                <ListItemText primary="No filters applied" />
              </ListItem>
            ) : (
              filters.map((filter, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <FiberManualRecordIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary={`${filter.criteria} ${filter.operand} ${filter.value}`} />
                </ListItem>
              ))
            )}
          </List>
        }
      />

      <Divider sx={{ my: 3 }} />

      <SummarySection
        title="Retention Policy"
        content={<Typography variant="body1">{produceRetentionPolicySummaryText(retentionPolicy)}</Typography>}
      />

      <Divider sx={{ my: 3 }} />

      <SummarySection
        title="Plex Library Destination"
        content={
          selectedDirectory && selectedLocation ? (
            <>
              <Typography variant="body1">
                <strong>Library:</strong> {selectedDirectory.title}
              </Typography>
              <Typography variant="body1" mt={1}>
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
    </Paper>
  );
};

export default SubscriptionSummary;
