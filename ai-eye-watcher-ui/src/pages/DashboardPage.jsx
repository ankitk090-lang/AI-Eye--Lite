import { Grid, Card, CardContent, Typography, Box, Skeleton, Alert } from '@mui/material';
import {
  Devices as DevicesIcon,
  Security as SecurityIcon,
  Block as BlockIcon,
  NetworkCheck as NetworkIcon,
} from '@mui/icons-material';
import { useState, useEffect } from 'react';
import axios from 'axios';
import StatCard from '../components/StatCard';

const DashboardPage = () => {
  // State for live data
  const [statsData, setStatsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Backend API URL
  const API_BASE_URL = 'http://localhost:9000';

  // Function to fetch dashboard stats
  const fetchDashboardStats = async () => {
    try {
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/api/v1/dashboard/stats`);
      const data = response.data;
      
      // Transform backend data to match our UI format
      const transformedStats = [
        {
          title: 'Connected Hosts',
          value: data.unique_hosts?.toString() || '0',
          trend: `${data.event_count} events collected`,
          icon: DevicesIcon,
          trendColor: 'info.main',
        },
        {
          title: 'Active Alerts',
          value: data.alert_count?.toString() || '0',
          trend: `${data.alert_severity_breakdown?.HIGH || 0} high severity`,
          icon: SecurityIcon,
          trendColor: data.alert_severity_breakdown?.HIGH > 0 ? 'error.main' : 'success.main',
        },
        {
          title: 'Total Events',
          value: data.event_count?.toString() || '0',
          trend: 'Real-time monitoring',
          icon: NetworkIcon,
          trendColor: 'success.main',
        },
        {
          title: 'Pending Commands',
          value: data.pending_command_hosts?.toString() || '0',
          trend: 'Automated responses',
          icon: BlockIcon,
          trendColor: data.pending_command_hosts > 0 ? 'warning.main' : 'success.main',
        },
      ];
      
      setStatsData(transformedStats);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching dashboard stats:', err);
      setError('Failed to fetch dashboard data. Make sure the backend server is running.');
      setLoading(false);
    }
  };

  // Effect for initial load and periodic refresh
  useEffect(() => {
    // Initial fetch
    fetchDashboardStats();

    // Set up periodic refresh every 15 seconds
    const interval = setInterval(fetchDashboardStats, 15000);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  // Loading skeleton component
  const StatCardSkeleton = () => (
    <Card sx={{ height: 140 }}>
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Skeleton variant="circular" width={40} height={40} sx={{ mr: 2 }} />
          <Skeleton variant="text" width="60%" height={24} />
        </Box>
        <Skeleton variant="text" width="40%" height={32} sx={{ mb: 1 }} />
        <Skeleton variant="text" width="80%" height={20} />
      </CardContent>
    </Card>
  );

  return (
    <Box>
      {/* Page Title */}
      <Typography variant="h4" sx={{ mb: 4, fontWeight: 'bold' }}>
        Dashboard Overview
      </Typography>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Stats Cards Row */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {loading ? (
          // Show skeleton loaders while loading
          Array.from({ length: 4 }).map((_, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <StatCardSkeleton />
            </Grid>
          ))
        ) : (
          // Show actual data when loaded
          statsData?.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <StatCard
                title={stat.title}
                value={stat.value}
                trend={stat.trend}
                icon={stat.icon}
                trendColor={stat.trendColor}
              />
            </Grid>
          ))
        )}
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3}>
        {/* Threat Detection Chart */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: 400 }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Threat Detection
              </Typography>
              <Box
                sx={{
                  height: 300,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: 'rgba(126, 87, 194, 0.05)',
                  borderRadius: 2,
                  border: '2px dashed rgba(126, 87, 194, 0.3)',
                }}
              >
                <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                  Chart Placeholder - Threat Detection Timeline
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Network Traffic Chart */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: 400 }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Network Traffic
              </Typography>
              <Box
                sx={{
                  height: 300,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: 'rgba(38, 198, 218, 0.05)',
                  borderRadius: 2,
                  border: '2px dashed rgba(38, 198, 218, 0.3)',
                }}
              >
                <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                  Chart Placeholder - Network Traffic Analysis
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;