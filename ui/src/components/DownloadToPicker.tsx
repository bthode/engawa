import { Directory, SaveToProps } from '@/types/plexTypes';
import Box from '@mui/material/Box';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import React from 'react';

interface LocationPickerProps {
  directories: Directory[];
  saveToProps: SaveToProps;
  setSaveToProps: React.Dispatch<React.SetStateAction<SaveToProps>>;
}

const LocationPicker: React.FC<LocationPickerProps> = ({ directories, saveToProps, setSaveToProps }) => {
  const handleDirectoryChange = (event: SelectChangeEvent<number | ''>) => {
    const newDirectoryId = event.target.value as number;
    setSaveToProps((prev) => ({
      ...prev,
      directoryId: newDirectoryId,
      locationId: 0,
    }));
  };

  const handleLocationChange = (event: SelectChangeEvent<number | ''>) => {
    const newLocationId = event.target.value as number;
    setSaveToProps((prev) => ({
      ...prev,
      locationId: newLocationId,
    }));
  };

  const selectedDirectoryObj = directories.find((dir) => dir.key === saveToProps.directoryId);
  if (selectedDirectoryObj && selectedDirectoryObj.locations.length === 1 && !saveToProps.locationId) {
    const defaultLocation = selectedDirectoryObj.locations[0].id;
    setSaveToProps((prev) => ({
      ...prev,
      locationId: defaultLocation,
    }));
  }

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
        value={saveToProps.directoryId}
        onChange={handleDirectoryChange}
        displayEmpty
        className="min-w-[200px] w-auto"
      >
        <MenuItem value="" disabled>
          Select Directory
        </MenuItem>
        {directories.map((directory) => (
          <MenuItem key={directory.key} value={directory.key}>
            {directory.title}
          </MenuItem>
        ))}
      </Select>

      <Select
        value={saveToProps.locationId}
        onChange={handleLocationChange}
        displayEmpty
        className="min-w-[200px] w-auto"
      >
        <MenuItem value="" disabled>
          Select Location
        </MenuItem>
        {selectedDirectoryObj ? (
          selectedDirectoryObj.locations.map((location) => (
            <MenuItem key={location.id} value={location.id}>
              {location.path}
            </MenuItem>
          ))
        ) : (
          <MenuItem value="" disabled>
            No locations available
          </MenuItem>
        )}
      </Select>
    </Box>
  );
};

export default LocationPicker;
