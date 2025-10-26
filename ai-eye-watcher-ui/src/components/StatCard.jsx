import { Card, CardContent, Typography, Box } from '@mui/material';

const StatCard = ({ title, value, trend, icon: Icon, trendColor = 'success.main' }) => {
  return (
    <Card sx={{ height: '100%', position: 'relative' }}>
      <CardContent sx={{ p: 3 }}>
        {/* Icon in top-right corner */}
        <Box sx={{ position: 'absolute', top: 16, right: 16 }}>
          <Icon sx={{ fontSize: 32, color: 'primary.main', opacity: 0.8 }} />
        </Box>
        
        {/* Main value */}
        <Typography 
          variant="h3" 
          component="div" 
          sx={{ 
            fontWeight: 'bold', 
            mb: 1,
            color: 'text.primary',
            fontSize: { xs: '2rem', sm: '2.5rem' }
          }}
        >
          {value}
        </Typography>
        
        {/* Title */}
        <Typography 
          variant="h6" 
          sx={{ 
            color: 'text.secondary', 
            mb: 1,
            fontSize: '1rem',
            fontWeight: 500
          }}
        >
          {title}
        </Typography>
        
        {/* Trend indicator */}
        {trend && (
          <Typography 
            variant="body2" 
            sx={{ 
              color: trendColor,
              fontSize: '0.875rem',
              fontWeight: 500
            }}
          >
            {trend}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default StatCard;