import React, { useMemo } from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { calculateMedian } from '../utils';

const AnalyticsCharts = ({ projects }) => {
    const chartData = useMemo(() => {
        if (!projects || projects.length === 0) return [];

        // Group projects by city
        const cityGroups = projects.reduce((acc, p) => {
            if (p.budget_num && p.city) {
                if (!acc[p.city]) acc[p.city] = [];
                acc[p.city].push(p.budget_num);
            }
            return acc;
        }, {});

        // Calculate median for each city
        const data = Object.entries(cityGroups)
            .map(([city, budgets]) => ({
                city,
                median: calculateMedian(budgets) / 10000000, // Convert to Crores for display
            }))
            .sort((a, b) => b.median - a.median) // Sort by median descending
            .slice(0, 10); // Top 10 cities

        return data;
    }, [projects]);

    if (chartData.length === 0) {
        return (
            <Paper className="glass-card" sx={{ p: 4, textAlign: 'center', height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">Insufficient budget data for visualization.</Typography>
            </Paper>
        );
    }

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <Paper className="glass-card" sx={{ p: 1.5, border: 'none' }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>{label}</Typography>
                    <Typography variant="body2" color="primary.main">
                        Median: ₹{payload[0].value.toFixed(2)} Cr
                    </Typography>
                </Paper>
            );
        }
        return null;
    };

    return (
        <Paper className="glass-card" sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
                Median Budget by City (Top 10 Cities)
            </Typography>
            <Box sx={{ width: '100%', height: 400 }}>
                <ResponsiveContainer>
                    <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 60 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                        <XAxis
                            dataKey="city"
                            angle={-45}
                            textAnchor="end"
                            interval={0}
                            stroke="#8b949e"
                            fontSize={12}
                        />
                        <YAxis
                            stroke="#8b949e"
                            fontSize={12}
                            tickFormatter={(val) => `₹${val}Cr`}
                        />
                        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.05)' }} />
                        <Bar dataKey="median" radius={[4, 4, 0, 0]}>
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#58a6ff' : '#bc8cff'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </Box>
        </Paper>
    );
};

export default AnalyticsCharts;
