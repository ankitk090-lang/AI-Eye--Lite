import {
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Skeleton,
  Alert,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useState, useEffect } from 'react';
import axios from 'axios';

const AlertsPage = () => {
  // State for alerts data
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Backend API URL
  const API_BASE_URL = 'http://localhost:9000';

  // Function to fetch alerts
  const fetchAlerts = async () => {
    try {
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/api/v1/alerts`);
      setAlerts(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching alerts:', err);
      setError('Failed to fetch alerts data. Make sure the backend server is running.');
      setLoading(false);
    }
  };

  // Effect for initial load and periodic refresh
  useEffect(() => {
    // Initial fetch
    fetchAlerts();

    // Set up periodic refresh every 30 seconds
    const interval = setInterval(fetchAlerts, 30000);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  // Function to get severity color
  const getSeverityColor = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'HIGH':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'info';
      default:
        return 'default';
    }
  };

  // Function to get severity icon
  const getSeverityIcon = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'HIGH':
        return <SecurityIcon fontSize="small" />;
      case 'MEDIUM':
        return <WarningIcon fontSize="small" />;
      case 'LOW':
        return <InfoIcon fontSize="small" />;
      default:
        return <InfoIcon fontSize="small" />;
    }
  };

  // Function to format timestamp
  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return timestamp;
    }
  };

  // Loading skeleton for table rows
  const TableRowSkeleton = () => (
    <TableRow>
      <TableCell><Skeleton variant="text" width="80%" /></TableCell>
      <TableCell><Skeleton variant="rectangular" width={60} height={24} /></TableCell>
      <TableCell><Skeleton variant="text" width="90%" /></TableCell>
      <TableCell><Skeleton variant="text" width="70%" /></TableCell>
      <TableCell><Skeleton variant="text" width="60%" /></TableCell>
    </TableRow>
  );

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          Threat Alerts
        </Typography>
        <Tooltip title="Refresh alerts">
          <IconButton onClick={fetchAlerts} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Alerts Table */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          <TableContainer component={Paper} elevation={0}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: 'grey.50' }}>
                  <TableCell sx={{ fontWeight: 600 }}>Timestamp</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Severity</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Finding Type</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Host</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Details</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  // Show skeleton loaders while loading
                  Array.from({ length: 5 }).map((_, index) => (
                    <TableRowSkeleton key={index} />
                  ))
                ) : alerts.length === 0 ? (
                  // Show empty state
                  <TableRow>
                    <TableCell colSpan={5} sx={{ textAlign: 'center', py: 4 }}>
                      <Typography variant="body1" color="text.secondary">
                        No alerts found. The system is monitoring for threats.
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  // Show actual alerts
                  alerts.map((alert, index) => (
                    <TableRow key={index} hover>
                      <TableCell>
                        <Typography variant="body2">
                          {formatTimestamp(alert.timestamp)}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          icon={getSeverityIcon(alert.severity)}
                          label={alert.severity || 'UNKNOWN'}
                          color={getSeverityColor(alert.severity)}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                          {alert.finding_type || 'N/A'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {alert.host || 'N/A'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ maxWidth: 300 }}>
                          {alert.details || 'No details available'}
                        </Typography>
                        {alert.process_name && (
                          <Typography variant="caption" display="block" color="text.secondary">
                            Process: {alert.process_name} (PID: {alert.process_pid})
                          </Typography>
                        )}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Summary Info */}
      {!loading && alerts.length > 0 && (
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Showing {alerts.length} alert{alerts.length !== 1 ? 's' : ''}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Auto-refresh every 30 seconds
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default AlertsPage;