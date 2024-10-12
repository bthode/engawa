export interface Location {
  id: number;
  path: string;
}

export interface Directory {
  id: number;
  title: string;
  uuid: string;
  key: number;
  locations: Location[];
}

export interface PlexServer {
  name: string;
  id: number;
  directories: Directory[];
  endpoint: string;
  token: string;
  port: string;
  error_state: null | string;
}

export interface SaveToProps {
  directoryId: number;
  locationid: number;
  directories: Directory[];
}

// TODO: We need to pass in the directory and location tuple, but we also need to persist the selected directory and location in the component state. We can do this by using the useState hook. We will create two state variables, selectedDirectory and selectedLocation, and initialize them to null.
export interface SaveToStepProps {
  directories: Directory[];
  onSave: (saveTo: SaveToProps) => void;
}
