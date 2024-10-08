'use client';

import React, { ReactNode } from 'react';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  ThemeProvider,
  CssBaseline,
} from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import SubscriptionsIcon from '@mui/icons-material/Subscriptions';
import MovieIcon from '@mui/icons-material/Movie';
import SettingsIcon from '@mui/icons-material/Settings';
import { usePathname, useRouter } from 'next/navigation';
import theme from './theme';

const drawerWidth = 240;

type LayoutProps = {
  children: ReactNode;
  onSubscriptionsClick?: () => void;
};

const navigationItems = [
  { text: 'Home', icon: <HomeIcon />, href: '/' },
  { text: 'Subscriptions', icon: <SubscriptionsIcon />, href: '/subscriptions' },
  { text: 'Plex Server', icon: <MovieIcon />, href: '/plex' },
  { text: 'Settings', icon: <SettingsIcon />, href: '/settings' },
  { text: 'Card', icon: <SettingsIcon />, href: '/card' },
  { text: 'sub2', icon: <SettingsIcon />, href: '/sub2' },
];

const Layout = ({ children, onSubscriptionsClick }: LayoutProps) => {
  const pathname = usePathname();
  const router = useRouter();

  const handleItemClick = (href: string, text: string) => {
    if (text === 'Subscriptions' && onSubscriptionsClick) {
      onSubscriptionsClick();
    }
    router.push(href);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
              borderRight: '1px solid rgba(255, 255, 255, 0.12)',
            },
          }}
        >
          <Toolbar>
            <Typography variant="h6" noWrap component="div" sx={{ color: 'primary.main' }}>
              Engawa
            </Typography>
          </Toolbar>
          <List>
            {navigationItems.map((item) => (
              <ListItem
                key={item.text}
                button
                selected={pathname === item.href}
                onClick={() => handleItemClick(item.href, item.text)}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(144, 202, 249, 0.08)',
                    '&:hover': {
                      backgroundColor: 'rgba(144, 202, 249, 0.12)',
                    },
                  },
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.08)',
                  },
                }}
              >
                <ListItemIcon sx={{ color: pathname === item.href ? 'primary.main' : 'inherit' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  sx={{
                    color: pathname === item.href ? 'primary.main' : 'inherit',
                  }}
                />
              </ListItem>
            ))}
          </List>
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          {children}
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;
