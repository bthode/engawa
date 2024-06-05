import { PlexServer } from '../app/plex/page';

export async function savePlexServer(data: {
  endpoint: string;
  token: string;
  port: string;
  name: string;
}): Promise<PlexServer[]> {
  try {
    const response = await fetch('/api/plex_server', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const newData: PlexServer[] = await response.json();
    return newData;
  } catch (error) {
    console.error('Error:', error);
    return [];
  }
}
