import { SaveToStepProps } from '@/types/plexTypes';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import React, { useState } from 'react';

const LocationPicker: React.FC<SaveToStepProps> = ({ directories, setDirectories, onSave }) => {
  const [selectedDirectory, setSelectedDirectory] = useState<number | ''>('');
  const [selectedLocation, setSelectedLocation] = useState<string | ''>('');

  const handleDirectoryChange = (event: SelectChangeEvent<number | ''>) => {
    setSelectedDirectory(event.target.value as number);
    setSelectedLocation(''); // Reset location when directory changes
  };

  const handleLocationChange = (event: SelectChangeEvent<string | ''>) => {
    setSelectedLocation(event.target.value as string);
  };

  const selectedDirectoryObj = directories.find((dir) => dir.key === selectedDirectory);
  if (selectedDirectoryObj && selectedDirectoryObj.locations.length === 1 && !selectedLocation) {
    setSelectedLocation(selectedDirectoryObj.locations[0].path);
    onSave({
      directory: selectedDirectory || 0,
      locationPath: selectedDirectoryObj.locations[0].path,
    });
  }
  return (
    <div>
      <Select value={selectedDirectory} onChange={handleDirectoryChange} displayEmpty className="min-w-[200px] w-auto">
        <MenuItem value="" disabled>
          Select Directory
        </MenuItem>
        {directories.map((directory) => (
          <MenuItem key={directory.key} value={directory.key}>
            {directory.title}
          </MenuItem>
        ))}
      </Select>

      {selectedDirectoryObj && (
        <Select value={selectedLocation} onChange={handleLocationChange} displayEmpty className="min-w-[200px] w-auto">
          <MenuItem value="" disabled>
            Select Location
          </MenuItem>
          {selectedDirectoryObj.locations.map((location, index) => (
            <MenuItem key={index} value={location.path}>
              {location.path}
            </MenuItem>
          ))}
        </Select>
      )}
    </div>
  );
};

export default LocationPicker;
