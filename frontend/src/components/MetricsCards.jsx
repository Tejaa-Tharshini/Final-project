import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { formatCurrency } from '../utils';

const MetricCard = ({ title, value, subtext }) => (
    <Paper className="glass-card" sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Typography variant="body2" color="text.secondary" gutterBottom sx={{ fontWeight: 600, textTransform: 'uppercase' }}>
            {title}
        </Typography>
        <Typography variant="h4" component="div" sx={{ mb: 1 }}>
            {value}
        </Typography>
        {subtext && (
            <Typography variant="body2" color="text.secondary">
                {subtext}
            </Typography>
        )}
    </Paper>
);

const MetricsCards = ({ total, byStatus, medianBudget, selectedCity }) => {
    return (
        <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={4}>
                <MetricCard title="Total Projects" value={total.toLocaleString()} />
            </Grid>
            <Grid item xs={12} md={4}>
                <MetricCard
                    title="Median Budget"
                    value={formatCurrency(medianBudget)}
                    subtext={selectedCity ? `In ${selectedCity}` : "Across Filtered Results"}
                />
            </Grid>
            <Grid item xs={12} md={4}>
                <MetricCard
                    title="Active (Ongoing)"
                    value={(byStatus['ongoing'] || 0).toLocaleString()}
                />
            </Grid>
        </Grid>
    );
};

export default MetricsCards;
