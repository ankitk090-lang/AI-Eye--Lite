import { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Chip,
  IconButton,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  NetworkCheck as NetworkIcon,
  Security as SecurityIcon,
  Policy as PolicyIcon,
  Devices as DevicesIcon,
  Settings as SettingsIcon,
  Menu as MenuIcon,
} from '@mui/icons-material';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 280;

const navigationItems = [
  { text: 'Dashboard', icon: DashboardIcon, path: '/' },
  { text: 'Network Activity', icon: NetworkIcon, path: '/network' },
  { text: 'Threat Alerts', icon: SecurityIcon, path: '/alerts' },
  { text: 'Policy Management', icon: PolicyIcon, path: '/policies' },
  { text: 'Devices', icon: DevicesIcon, path: '/devices' },
  { text: 'Settings', icon: SettingsIcon, path: '/settings' },
];

const Layout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleNavigation = (path) => {
    navigate(path);
    setMobileOpen(false);
  };

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Logo/Title */}
      <Box sx={{ p: 3, borderBottom: '1px solid rgba(255, 255, 255, 0.12)' }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          AI-Eye Watcher
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary', mt: 0.5 }}>
          Network Security Monitor
        </Typography>
      </Box>

      {/* Navigation Items */}
      <List sx={{ flexGrow: 1, px: 2, py: 1 }}>
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <ListItem key={item.text} disablePadding sx={{ mb: 0.5 }}>
              <ListItemButton
                onClick={() => handleNavigation(item.path)}
                sx={{
                  borderRadius: 2,
                  backgroundColor: isActive ? 'primary.main' : 'transparent',
                  '&:hover': {
                    backgroundColor: isActive ? 'primary.dark' : 'rgba(126, 87, 194, 0.1)',
                  },
                  py: 1.5,
                }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>
                  <Icon sx={{ 
                    color: isActive ? 'white' : 'text.secondary',
                    fontSize: 24 
                  }} />
                </ListItemIcon>
                <ListItemText 
                  primary={item.text}
                  primaryTypographyProps={{
                    fontSize: '0.95rem',
                    fontWeight: isActive ? 600 : 500,
                    color: isActive ? 'white' : 'text.primary',
                  }}
                />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>

      {/* System Status */}
      <Box sx={{ p: 3, borderTop: '1px solid rgba(255, 255, 255, 0.12)' }}>
        <Typography variant="body2" sx={{ color: 'text.secondary', mb: 1 }}>
          System Status
        </Typography>
        <Chip
          label="Online"
          color="success"
          size="small"
          sx={{ fontWeight: 500 }}
        />
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* AppBar */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Dashboard Overview
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8, // Account for AppBar height
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;