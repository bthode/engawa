export interface Location {
  path: string;
}

export interface Directory {
  title: string;
  uuid: string;
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
