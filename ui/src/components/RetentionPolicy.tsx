import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';

import { Slider } from '@mui/material';

export type RetentionPolicyType = 'RetainAll' | 'LastNEntities' | 'EntitiesSince';

export interface RetentionPolicy {
  type: RetentionPolicyType;
  value?: number | Date | string;
}

export interface RetentionPolicypProps {
  retentionPolicy: RetentionPolicy[];
  setRetentionPolicy: React.Dispatch<React.SetStateAction<RetentionPolicy[]>>;
}

const retentionPolicy: React.FC<RetentionPolicypProps> = ({ retentionPolicy, setRetentionPolicy }) => (
  <div className="flex flex-col items-center">
    <h2 className="text-xl font-bold mb-4">Retention Policy</h2>
    <FormControl>
      <FormLabel id="retention-policy-step-label">Retention Policy Step</FormLabel>
      <RadioGroup row aria-labelledby="retention-policy-step-label" name="retention-policy-step-group">
        <FormControlLabel value="step1" control={<Radio />} label="All Videos" />
        <FormControlLabel value="step2" control={<Radio />} label="Last N Videos" />
        <FormControlLabel value="step3" control={<Radio />} label="Since Date" />
        <FormControlLabel value="step4" control={<Radio />} label="Relative Date Offset" />
      </RadioGroup>
    </FormControl>
    <select
      value={retentionPolicy.type}
      onChange={(e) => setRetentionPolicy({ type: e.target.value as RetentionPolicyType, value: undefined })}
      className="mb-4 p-2 border rounded text-gray-800 bg-white"
    >
      <option value="RetainAll">Keep All Videos</option>
      <option value="LastNEntities">Keep Last N Videos</option>
      <option value="EntitiesSince">Keep Videos Since...</option>
    </select>
    {retentionPolicy.type === 'LastNEntities' && (
      <Slider
        value={retentionPolicy.value as number}
        onChange={(e, newValue) => setRetentionPolicy({ ...retentionPolicy, value: newValue as number })}
        aria-labelledby="input-slider"
        valueLabelDisplay="on"
      />
      // <input
      //   type="number"
      //   value={retentionPolicy.value as number}
      //   onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: parseInt(e.target.value) })}
      //   placeholder="Enter number of entities"
      //   className="mb-4 p-2 border rounded text-gray-800 bg-white"
      // />
    )}
    {retentionPolicy.type === 'EntitiesSince' && (
      <div className="flex flex-col items-center">
        <input
          type="date"
          value={retentionPolicy.value as string}
          onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: e.target.value })}
          className="mb-2 p-2 border rounded text-gray-800 bg-white"
        />
        <input
          type="text"
          value={retentionPolicy.value as string}
          onChange={(e) => setRetentionPolicy({ ...retentionPolicy, value: e.target.value })}
          placeholder="Or enter relative time (e.g., '2 weeks ago')"
          className="mb-4 p-2 border rounded text-gray-800 bg-white"
        />
      </div>
    )}
  </div>
);

export default retentionPolicy;
