import { Meta, StoryFn } from '@storybook/react';
import { useState } from 'react';
import FilterStep, { Filter, FilterStepProps } from './FilterStep';

export default {
  title: 'Components/FilterStep',
  component: FilterStep,
} as Meta;

const Template: StoryFn<FilterStepProps> = (args) => {
  const [filters, setFilters] = useState<Filter[]>(args.filters);
  return <FilterStep {...args} filters={filters} setFilters={setFilters} />;
};

export const Default = Template.bind({});
Default.args = {
  filters: [{ criteria: 'Title', operand: 'contains', value: 'example' }],
};

export const MultipleFilters = Template.bind({});
MultipleFilters.args = {
  filters: [
    { criteria: 'Title', operand: 'contains', value: 'example' },
    { criteria: 'Duration', operand: '>', value: 10 },
    { criteria: 'Published', operand: '>=', value: new Date().toISOString().split('T')[0] },
  ],
};

export const NoFilters = Template.bind({});
NoFilters.args = {
  filters: [],
};
