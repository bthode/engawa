interface Location {
  path: string;
}

interface Directory {
  id: number;
  title: string;
  uuid: string;
  key: number;
  locations: Location[];
}

export const directories: Directory[] = [
  {
    id: 2,
    title: 'Movies',
    uuid: '364f2ba8-254e-492d-a8d5-8658cfc90161',
    key: 3,
    locations: [
      {
        path: '/media/Media/Video/Movies',
      },
    ],
  },
  {
    id: 4,
    title: 'Youtube',
    uuid: '0c717b05-2deb-419c-a2d0-e68cceddea04',
    key: 7,
    locations: [
      {
        path: '/index/YouTube',
      },
      {
        path: '/index/media',
      },
    ],
  },
  {
    id: 7,
    title: 'TV Shows',
    uuid: '50b6e1e0-e274-41e4-ade8-1e71e95c9330',
    key: 2,
    locations: [
      {
        path: '/media/Media/Video/TV',
      },
    ],
  },
  {
    id: 9,
    title: 'Fitness',
    uuid: 'e32e9e32-b24c-4867-b113-95fc3914e37e',
    key: 16,
    locations: [
      {
        path: '/index/YouTube/reference',
      },
    ],
  },
  {
    id: 10,
    title: 'Misc',
    uuid: '2c507cdc-36d7-43cc-beee-efbee3644bbd',
    key: 1,
    locations: [
      {
        path: '/media/Media/Video/Video',
      },
    ],
  },
  {
    id: 11,
    title: 'Personal',
    uuid: '3df269f4-004e-4c00-b522-4acb6c8dfe54',
    key: 14,
    locations: [
      {
        path: '/media/Media/Video/Personal',
      },
    ],
  },
];

// let results = directories.map(({ title, locations }) => [title, locations]);

import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import React, { useState } from 'react';

const LocationPicker: React.FC = () => {
  const [selectedDirectory, setSelectedDirectory] = useState<number | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<string | null>(null);

  const handleDirectoryChange = (event: SelectChangeEvent<number>) => {
    setSelectedDirectory(event.target.value as number);
    setSelectedLocation(null); // Reset location when directory changes
  };

  const handleLocationChange = (event: SelectChangeEvent<string>) => {
    setSelectedLocation(event.target.value as string);
  };

  const selectedDirectoryObj = directories.find((dir) => dir.key === selectedDirectory);
  if (selectedDirectoryObj && selectedDirectoryObj.locations.length === 1 && !selectedLocation) {
    setSelectedLocation(selectedDirectoryObj.locations[0].path);
  }
  return (
    <div>
      <Select value={selectedDirectory ?? ''} onChange={handleDirectoryChange} displayEmpty>
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
        <Select value={selectedLocation ?? ''} onChange={handleLocationChange} displayEmpty>
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
