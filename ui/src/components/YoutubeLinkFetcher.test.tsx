import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import YouTubeLinkFetcher from './YoutubeLinkFetcher';
import axios from 'axios';
import '@testing-library/jest-dom';

const mockSuccessResponse = {
  data: {
    rss_link: 'https://example.com/rss',
    image_link: 'https://example.com/image.jpg',
    title: 'Example Channel',
    description: 'This is an example channel description',
  },
};

const mockNetworkError = {
  message: 'Network Error',
};

describe('YouTubeLinkFetcher Tests', () => {
  beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    (console.error as jest.Mock).mockRestore();
  });

  test('renders the input field', () => {
    render(<YouTubeLinkFetcher />);
    const inputField = screen.getByPlaceholderText('Enter URL');
    expect(inputField).toBeInTheDocument();
  });

  test('validates valid channel or playlist URLs', async () => {
    const validUrl = 'https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw';
    render(<YouTubeLinkFetcher />);
    const inputField = screen.getByPlaceholderText('Enter URL');

    fireEvent.change(inputField, { target: { value: validUrl } });
    await waitFor(() => expect(screen.queryByText('Invalid URL')).not.toBeInTheDocument());
  });

  test('validates invalid URLs', async () => {
    const invalidUrl = 'https://example.com';
    render(<YouTubeLinkFetcher />);
    const inputField = screen.getByPlaceholderText('Enter URL');

    fireEvent.change(inputField, { target: { value: invalidUrl } });
    await waitFor(() => expect(screen.getByText('Invalid URL')).toBeInTheDocument());
  });

  test('fetches RSS data and renders the card on successful API response', async () => {
    const validUrl = 'https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw';
    jest.spyOn(axios, 'post').mockResolvedValueOnce(mockSuccessResponse);

    render(<YouTubeLinkFetcher />);
    const inputField = screen.getByPlaceholderText('Enter URL');

    fireEvent.change(inputField, { target: { value: validUrl } });
    await waitFor(() => expect(screen.getByText('Example Channel')).toBeInTheDocument());
    expect(screen.getByText('Description: This is an example channel description')).toBeInTheDocument();
    expect(screen.getByText('RSS Feed')).toHaveAttribute('href', 'https://example.com/rss');

    const postSpy = jest.spyOn(axios, 'post').mockResolvedValueOnce(mockSuccessResponse);
    postSpy.mockRestore();
  });

  test('shows an error message on network error', async () => {
    const validUrl = 'https://www.youtube.com/channel/UCXuqSBlHAE6Xw-yeJA0Tunw';
    jest.spyOn(axios, 'post').mockRejectedValueOnce(mockNetworkError);
    window.alert = jest.fn();

    render(<YouTubeLinkFetcher />);
    const inputField = screen.getByPlaceholderText('Enter URL');

    fireEvent.change(inputField, { target: { value: validUrl } });
    await waitFor(() => expect(window.alert).toHaveBeenCalledWith('Error: Network Error'));

    const postSpy = jest.spyOn(axios, 'post').mockResolvedValueOnce(mockSuccessResponse);
    postSpy.mockRestore();
  });
});
