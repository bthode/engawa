import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';
import React from 'react';

export interface Filter {
  criteria: 'Duration' | 'Title' | 'Published' | 'Description';
  operand: '>' | '<' | '>=' | '<=' | '==' | '!=' | 'contains' | '!contains';
  value: string | number | Date;
}

export interface FilterStepProps {
  filters: Filter[];
  setFilters: React.Dispatch<React.SetStateAction<Filter[]>>;
}

const FilterStep: React.FC<FilterStepProps> = ({ filters, setFilters }) => {
  return (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-4">Filters</h2>
      {filters.map((filter, index) => (
        <div key={index} className="grid grid-cols-4 gap-2 mb-2 rounded w-full max-w-md">
          <select
            value={filter.criteria}
            onChange={(e) => {
              const newFilters = [...filters];
              newFilters[index].criteria = e.target.value as 'Duration' | 'Title' | 'Published' | 'Description';
              setFilters(newFilters);
            }}
            className="p-2 border rounded bg-white text-gray-800 w-full"
          >
            <option value="Duration">Duration</option>
            <option value="Title">Title</option>
            <option value="Published">Published</option>
            <option value="Description">Description</option>
          </select>
          <select
            value={filter.operand}
            onChange={(e) => {
              const newFilters = [...filters];
              newFilters[index].operand = e.target.value as
                | '>'
                | '<'
                | '>='
                | '<='
                | '=='
                | '!='
                | 'contains'
                | '!contains';
              setFilters(newFilters);
            }}
            className="p-2 border rounded bg-white text-gray-800 w-full"
          >
            {filter.criteria === 'Title' || filter.criteria === 'Description' ? (
              <>
                <option value="contains">contains</option>
                <option value="!contains">does not contain</option>
              </>
            ) : (
              <>
                <option value=">">{'>'}</option>
                <option value="<">{'<'}</option>
                <option value=">=">{'≥'}</option>
                <option value="<=">{'≤'}</option>
                <option value="==">{'='}</option>
                <option value="!=">{'≠'}</option>
              </>
            )}
          </select>
          <input
            type={filter.criteria === 'Published' ? 'date' : 'text'}
            value={filter.value as string}
            onChange={(e) => {
              const newFilters = [...filters];
              newFilters[index].value = e.target.value;
              setFilters(newFilters);
            }}
            className="p-2 border rounded text-gray-800 bg-white w-full"
          />

          <IconButton
            onClick={() => setFilters(filters.filter((_, i) => i !== index))}
            disableRipple
            style={{ color: 'white' }}
            onMouseOver={(e) => (e.currentTarget.style.color = 'red')}
            onMouseOut={(e) => (e.currentTarget.style.color = 'white')}
          >
            <DeleteIcon />
          </IconButton>
        </div>
      ))}
      <button
        onClick={() => setFilters([...filters, { criteria: 'Title', operand: 'contains', value: '' }])}
        className="mb-4 px-4 py-2 bg-green-500 text-white rounded"
      >
        Add Filter
      </button>
    </div>
  );
};

export default FilterStep;
