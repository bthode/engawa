import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SubscriptionVideos from './SubscriptionVideos';
import { VirtuosoMockContext } from 'react-virtuoso'

global.fetch = jest.fn();

const renderWithVirtuosoContext = (ui: React.ReactElement) => {
  return render(
    <VirtuosoMockContext.Provider value={{ viewportHeight: 800, itemHeight: 50 }}>
      {ui}
    </VirtuosoMockContext.Provider>
  );
};

describe('SubscriptionVideos', () => {
  const mockSubscriptionId = '123';
  const mockSubscription = {
    id: 123,
    title: 'Test Channel',
    url: 'https://example.com',
    description: 'Test description',
  };
  const mockVideos = [
    {
      id: 1,
      title: 'Test Video 1',
      published: '2023-05-01T12:00:00Z',
      video_id: 'abc123',
      link: 'https://youtube.com/watch?v=abc123',
      author: 'Test Author',
      subscription_id: 123,
      thumbnail_url: 'https://example.com/thumbnail1.jpg',
      status: 'Complete',
    },
  ];

  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  it('renders loading state initially', () => {
    (fetch as jest.Mock).mockImplementation(() => new Promise(() => {}));
    renderWithVirtuosoContext(<SubscriptionVideos subscriptionId={mockSubscriptionId} />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders subscription details and video table', async () => {
    (fetch as jest.Mock).mockImplementation((url) => {
      if (url.includes('/api/subscription/123')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockSubscription),
        });
      } else if (url.includes('/api/subscription/123/videos')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockVideos),
        });
      }
    });

    renderWithVirtuosoContext(<SubscriptionVideos subscriptionId={mockSubscriptionId} />);

      await waitFor(() => {
        expect(screen.getByText('Test Channel')).toBeInTheDocument();
        expect(screen.getByText('URL: https://example.com')).toBeInTheDocument();
        expect(screen.getByText('Test description')).toBeInTheDocument();
        
        expect(screen.getByText('Videos')).toBeInTheDocument();
        expect(screen.getByRole('table')).toBeInTheDocument();
        expect(screen.getByRole('columnheader', { name: 'Title' })).toBeInTheDocument();
      });
  });

  it('renders error message when fetch fails', async () => {
    (fetch as jest.Mock).mockImplementation(() =>
      Promise.resolve({
        ok: false,
      })
    );

    renderWithVirtuosoContext(<SubscriptionVideos subscriptionId={mockSubscriptionId} />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load subscription data. Please try again later.')).toBeInTheDocument();
    });
  });
});
