import { PlexServer } from '@/types/plexTypes';

export async function savePlexServer(data: PlexServer): Promise<PlexServer[]> {
  try {
    const { name, endpoint, port, token } = data;
    const response = await fetch('/api/plex_server', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ endpoint, port, name, token }),
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const newData: PlexServer[] = await response.json();
    return newData;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export async function editPlexServer(data: PlexServer): Promise<PlexServer[]> {
  try {
    const { id, name, endpoint, port, token } = data;
    const response = await fetch(`/api/plex_server/${data.id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ endpoint, port, name, token }),
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const updatedData: PlexServer[] = await response.json();
    return updatedData;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export async function deletePlexServer(data: PlexServer): Promise<PlexServer[]> {
  try {
    const response = await fetch(`/api/plex_server/${data.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
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
