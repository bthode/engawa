export type Location = {
  path: string;
};

export type Directory = {
  title: string;
  uuid: string;
  locations: Location[];
};

export type PlexServer = {
  name: string;
  id: number;
  directories: Directory[];
  endpoint: string;
  port: string;
  error_state: null | string;
};
