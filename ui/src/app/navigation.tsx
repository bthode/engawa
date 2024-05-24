import Link from 'next/link';
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material';
import { ReactNode } from 'react';

type LayoutProps = {
  children: ReactNode;
};

const Layout = ({ children }: LayoutProps) => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Box sx={{ display: 'flex', justifyContent: 'center', width: '50%', margin: '0 auto' }}>
            <Link href="/" passHref>
              <Button color="secondary" variant="contained">
                Home
              </Button>
            </Link>
            <Link href="/subscriptions" passHref>
              <Button color="secondary" variant="contained">
                Subscriptions
              </Button>
            </Link>
            <Link href="/plex" passHref>
              <Button color="secondary" variant="contained">
                Plex Server
              </Button>
            </Link>
            <Link href="/settings" passHref>
              <Button color="secondary" variant="contained">
                Settings
              </Button>
            </Link>
          </Box>
        </Toolbar>
      </AppBar>
      <main>{children}</main>
    </div>
  );
};

export default Layout;
