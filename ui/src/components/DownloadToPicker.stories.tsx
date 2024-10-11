import { Meta, StoryFn } from '@storybook/react';
import DownloadToPicker from './DownloadToPicker';

export default {
  title: 'Components/DownloadToPicker',
  component: DownloadToPicker,
} as Meta;

const Template: StoryFn = (args) => <DownloadToPicker {...args} />;

export const Default = Template.bind({});
Default.args = {};
