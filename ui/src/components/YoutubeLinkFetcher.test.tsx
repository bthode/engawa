import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import { SnackbarProvider } from 'notistack';
import axios from 'axios';
import YoutubeLinkFetcher from './YouTubeLinkFetcher';
import '@testing-library/jest-dom';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

const mockChannelInfo = {
  title: 'Test Channel',
  rss_link: 'https://example.com/rss',
  image_link: 'https://example.com/image.jpg',
  description: 'This is a test channel description',
};

const renderWithSnackbar = (component: React.ReactElement) => {
  return render(<SnackbarProvider maxSnack={3}>{component}</SnackbarProvider>);
};

describe('YoutubeLinkFetcher Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders the input field and fetch button', () => {
    renderWithSnackbar(<YoutubeLinkFetcher />);
    expect(screen.getByLabelText('YouTube Channel URL')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Fetch Channel Info' })).toBeInTheDocument();
  });

  test('shows error for invalid URL', async () => {
    renderWithSnackbar(<YoutubeLinkFetcher />);
    const input = screen.getByLabelText('YouTube Channel URL');
    const fetchButton = screen.getByRole('button', { name: 'Fetch Channel Info' });

    fireEvent.change(input, { target: { value: 'invalid-url' } });
    fireEvent.click(fetchButton);

    await waitFor(() => {
      expect(screen.getByText('Invalid URL')).toBeInTheDocument();
    });
  });

  test('fetches channel info for valid URL', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: mockChannelInfo });
    renderWithSnackbar(<YoutubeLinkFetcher />);

    const input = screen.getByLabelText('YouTube Channel URL');
    const fetchButton = screen.getByRole('button', { name: 'Fetch Channel Info' });

    fireEvent.change(input, { target: { value: 'https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw' } });
    fireEvent.click(fetchButton);

    await waitFor(() => {
      expect(screen.getByText('Test Channel')).toBeInTheDocument();
      expect(screen.getByText('This is a test channel description')).toBeInTheDocument();
      expect(screen.getByRole('link', { name: 'RSS Feed' })).toHaveAttribute('href', 'https://example.com/rss');
      expect(screen.getByRole('img')).toHaveAttribute('src', 'https://example.com/image.jpg');
    });
  });

  test('shows error message on fetch failure', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Network Error'));
    renderWithSnackbar(<YoutubeLinkFetcher />);

    const input = screen.getByLabelText('YouTube Channel URL');
    const fetchButton = screen.getByRole('button', { name: 'Fetch Channel Info' });

    fireEvent.change(input, { target: { value: 'https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw' } });
    fireEvent.click(fetchButton);

    await waitFor(() => {
      expect(screen.getByText('Failed to fetch channel information')).toBeInTheDocument();
    });
  });

  test('disables input and button while fetching', async () => {
    mockedAxios.post.mockImplementationOnce(
      () => new Promise((resolve) => setTimeout(() => resolve({ data: mockChannelInfo }), 100)),
    );
    renderWithSnackbar(<YoutubeLinkFetcher />);

    const input = screen.getByLabelText('YouTube Channel URL');
    const fetchButton = screen.getByRole('button', { name: 'Fetch Channel Info' });

    fireEvent.change(input, { target: { value: 'https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw' } });
    fireEvent.click(fetchButton);

    expect(input).toBeDisabled();
    expect(fetchButton).toBeDisabled();
    expect(screen.getByText('Fetching...')).toBeInTheDocument();

    await waitFor(() => {
      expect(input).not.toBeDisabled();
      expect(fetchButton).not.toBeDisabled();
      expect(screen.getByText('Fetch Channel Info')).toBeInTheDocument();
    });
  });
});
