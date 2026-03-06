import React, { useMemo } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell } from 'recharts';
import { Paper, Typography, Box } from '@mui/material';

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#0088fe', '#00c49f', '#ffbb28', '#ff8042'];

const BuildersBarChart = ({ projects, selectedState, selectedCity }) => {
    const data = useMemo(() => {
        if (selectedCity) {
            // City Mode: Builders in that city
            const counts = projects.reduce((acc, p) => {
                acc[p.builder_name] = (acc[p.builder_name] || 0) + 1;
                return acc;
            }, {});
            return Object.entries(counts)
                .map(([name, count]) => ({ name, count }))
                .sort((a, b) => b.count - a.count)
                .slice(0, 10);
        } else if (selectedState) {
            // State Mode: Cities in that state
            const counts = projects.reduce((acc, p) => {
                acc[p.city] = (acc[p.city] || 0) + 1;
                return acc;
            }, {});
            return Object.entries(counts)
                .map(([name, count]) => ({ name, count }))
                .sort((a, b) => b.count - a.count)
                .slice(0, 10);
        }
        return [];
    }, [projects, selectedState, selectedCity]);

    if (!selectedState) {
        return (
            <Paper className="glass-card" sx={{ p: 3, textAlign: 'center', minHeight: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">Select a state to visualize builder/city distributions</Typography>
            </Paper>
        );
    }

    const title = selectedCity
        ? `Top Builders in ${selectedCity}`
        : `Projects per City in ${selectedState}`;

    return (
        <Paper className="glass-card" sx={{ p: 3, minHeight: 400 }}>
            <Typography variant="h6" gutterBottom color="primary.main">
                {title}
            </Typography>
            <Box sx={{ width: '100%', height: 350 }}>
                <ResponsiveContainer>
                    <BarChart data={data} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis type="number" hide />
                        <YAxis
                            dataKey="name"
                            type="category"
                            width={150}
                            tick={{ fill: '#aaa', fontSize: 12 }}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: 8 }}
                            itemStyle={{ color: '#fff' }}
                        />
                        <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </Box>
        </Paper>
    );
};

export default BuildersBarChart;
