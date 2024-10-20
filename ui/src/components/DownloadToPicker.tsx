import { DirectoryPublic } from '@/api/models';
import Box from '@mui/material/Box';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import React, { useEffect } from 'react';
import { PlexLibraryDestination } from './SubscriptionSummary';

interface LocationPickerProps {
  directories: DirectoryPublic[];
  PlexLibraryDestination: PlexLibraryDestination;
  setPlexLibraryDestination: React.Dispatch<React.SetStateAction<PlexLibraryDestination>>;
}

const LocationPicker: React.FC<LocationPickerProps> = ({
  directories,
  PlexLibraryDestination,
  setPlexLibraryDestination,
}) => {
  const handleDirectoryChange = (event: SelectChangeEvent<string | number>) => {
    const newDirectoryId = event.target.value as number;
    setPlexLibraryDestination((prev) => ({
      ...prev,
      directoryId: newDirectoryId,
      locationId: -1,
    }));
  };

  const handleLocationChange = (event: SelectChangeEvent<string | number>) => {
    const newLocationId = event.target.value as number;
    setPlexLibraryDestination((prev) => ({
      ...prev,
      locationId: newLocationId,
    }));
  };

  // TODO: This code isn't being hit in the debugger, thus we're not seeing the only location value when there's only one location
  // Even before useEffect was added, I think the invalid locationId in addition to the disabled 'Select Location' value was
  // inadvertently causing the first location to be selected by default
  useEffect(() => {
    const selectedDirectoryObj = directories.find((dir) => dir.key === PlexLibraryDestination.directoryId);
    if (selectedDirectoryObj && selectedDirectoryObj.locations?.length === 1 && !PlexLibraryDestination.locationId) {
      const defaultLocation = selectedDirectoryObj.locations[0].id as number;
      setPlexLibraryDestination((prev) => ({
        ...prev,
        locationId: defaultLocation,
      }));
    }
  }, [directories, PlexLibraryDestination.directoryId, PlexLibraryDestination.locationId, setPlexLibraryDestination]);

  return (
    <Box
      sx={{
        width: 100,
        height: 100,
        borderRadius: 2,
        alignContent: 'center',
      }}
    >
      <Select
        value={PlexLibraryDestination.directoryId ?? ''}
        onChange={handleDirectoryChange}
        displayEmpty
        className="min-w-[200px] w-auto"
      >
        <MenuItem value="-1" disabled>
          Select Directory
        </MenuItem>
        {directories.map((directory) => (
          <MenuItem key={directory.key} value={directory.key}>
            {directory.title}
          </MenuItem>
        ))}
      </Select>

      <Select
        value={PlexLibraryDestination.locationId ?? ''}
        onChange={handleLocationChange}
        displayEmpty
        className="min-w-[200px] w-auto"
      >
        <MenuItem value="-1" disabled>
          Select Location
        </MenuItem>
        {directories
          .find((dir) => dir.key === PlexLibraryDestination.directoryId)
          ?.locations?.map((location) => (
            <MenuItem key={location.id} value={location.id as number}>
              {location.path}
            </MenuItem>
          )) || (
          <MenuItem value="" disabled>
            No locations available
          </MenuItem>
        )}
      </Select>
    </Box>
  );
};

export default LocationPicker;
