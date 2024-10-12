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
  locationId: number;
}
