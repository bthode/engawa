import { DirectoryPublic } from '@/api/models';
import { Meta, StoryFn } from '@storybook/react';
import { useState } from 'react';
import DownloadToPicker from './DownloadToPicker';
import { SaveToProps } from './SubscriptionSummary';

export default {
  title: 'Components/DownloadToPicker',
  component: DownloadToPicker,
} as Meta;

const directories: DirectoryPublic[] = [
  {
    id: 2,
    title: 'Movies',
    uuid: '364f2ba8-254e-492d-a8d5-8658cfc90161',
    key: 3,
    locations: [
      {
        id: 3,
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
        id: 5,
        path: '/index/YouTube',
      },
      {
        id: 6,
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
        id: 8,
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
        id: 10,
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
        id: 11,
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
        id: 12,
        path: '/media/Media/Video/Personal',
      },
    ],
  },
];

const Template: StoryFn<{
  directories: DirectoryPublic[];
  saveToProps: SaveToProps;
  setSaveToProps: React.Dispatch<React.SetStateAction<SaveToProps>>;
}> = (args) => {
  const [saveToProps, setSaveToProps] = useState<SaveToProps>(args.saveToProps);

  return <DownloadToPicker {...args} saveToProps={saveToProps} setSaveToProps={setSaveToProps} />;
};

export const Default = Template.bind({});
Default.args = {
  directories,
  saveToProps: {
    directoryId: -1,
    locationId: -1,
  },
};

export const WithSelectedDirectory = Template.bind({});
WithSelectedDirectory.args = {
  directories,
  saveToProps: {
    directoryId: 7,
    locationId: -1,
  },
};

export const WithSelectedLocation = Template.bind({});
WithSelectedLocation.args = {
  directories,
  saveToProps: {
    directoryId: 2,
    locationId: 8,
  },
};
