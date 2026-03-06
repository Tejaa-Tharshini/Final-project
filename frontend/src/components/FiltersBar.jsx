import React from 'react';
import { Box, FormControl, InputLabel, Select, MenuItem, Button, Paper, Typography } from '@mui/material';

const FiltersBar = ({
    states,
    cities,
    selectedState,
    onStateChange,
    selectedCity,
    onCityChange,
    selectedStatus,
    onStatusChange,
    onApply
}) => {
    return (
        <Paper className="glass-card" sx={{ p: 2, mb: 3, display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
            <Typography variant="h6" sx={{ mr: 2, color: 'primary.main' }}>Filters</Typography>

            <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>State</InputLabel>
                <Select
                    value={selectedState}
                    label="State"
                    onChange={(e) => {
                        onStateChange(e.target.value);
                    }}
                >
                    <MenuItem value="">All States</MenuItem>
                    {states.map((state) => (
                        <MenuItem key={state} value={state}>{state}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <FormControl size="small" sx={{ minWidth: 200 }} disabled={!selectedState}>
                <InputLabel>City</InputLabel>
                <Select
                    value={selectedCity}
                    label="City"
                    onChange={(e) => onCityChange(e.target.value)}
                >
                    <MenuItem value="">{selectedState ? "All Cities in " + selectedState : "Select State First"}</MenuItem>
                    {cities.map((city) => (
                        <MenuItem key={city} value={city}>{city}</MenuItem>
                    ))}
                </Select>
            </FormControl>

            <FormControl size="small" sx={{ minWidth: 150 }}>
                <InputLabel>Status</InputLabel>
                <Select
                    value={selectedStatus}
                    label="Status"
                    onChange={(e) => onStatusChange(e.target.value)}
                >
                    <MenuItem value="all">All Statuses</MenuItem>
                    <MenuItem value="ongoing">Ongoing</MenuItem>
                    <MenuItem value="completed">Completed</MenuItem>
                    <MenuItem value="upcoming">Upcoming</MenuItem>
                </Select>
            </FormControl>

            <Button variant="contained" color="primary" onClick={onApply} sx={{ height: 40, px: 4, borderRadius: 2 }}>
                Apply Filters
            </Button>
        </Paper>
    );
};

export default FiltersBar;
