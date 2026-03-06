import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { Box, Typography, Button, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default marker icon in Leaflet + React
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const ChangeView = ({ center, zoom }) => {
    const map = useMap();
    useEffect(() => {
        map.setView(center, zoom);
    }, [center, zoom, map]);
    return null;
};

const HeatmapPage = ({ projects, selectedState, selectedCity }) => {
    // Filter projects that have lat/long
    const validProjects = projects.filter(p => p.latitude && p.longitude);

    // Dynamic map center/zoom
    const mapSettings = React.useMemo(() => {
        if (selectedCity && validProjects.length > 0) {
            return { center: [parseFloat(validProjects[0].latitude), parseFloat(validProjects[0].longitude)], zoom: 12 };
        }
        if (selectedState && validProjects.length > 0) {
            return { center: [parseFloat(validProjects[0].latitude), parseFloat(validProjects[0].longitude)], zoom: 7 };
        }
        return { center: [20.5937, 78.9629], zoom: 5 }; // India center
    }, [selectedState, selectedCity, validProjects]);

    return (
        <Box sx={{ height: '100vh', width: '100vw', position: 'relative' }}>
            {/* Header Overlay */}
            <Paper
                className="glass-card"
                sx={{
                    position: 'absolute',
                    top: 20,
                    left: 20,
                    right: 20,
                    zIndex: 1000,
                    p: 2,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}
            >
                <Box>
                    <Typography variant="h5" color="primary.main" sx={{ fontWeight: 'bold' }}>
                        Project Discovery Map
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Showing {validProjects.length} geo-tagged projects
                    </Typography>
                </Box>
                <Button
                    component={Link}
                    to="/"
                    variant="contained"
                    sx={{ borderRadius: 2 }}
                >
                    Back to Dashboard
                </Button>
            </Paper>

            <MapContainer
                center={mapSettings.center}
                zoom={mapSettings.zoom}
                style={{ height: '100%', width: '100%' }}
                scrollWheelZoom={true}
            >
                <ChangeView center={mapSettings.center} zoom={mapSettings.zoom} />
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {validProjects.slice(0, 1000).map((project, idx) => (
                    <Marker
                        key={`${project.id || idx}`}
                        position={[parseFloat(project.latitude), parseFloat(project.longitude)]}
                    >
                        <Popup>
                            <Box sx={{ p: 1 }}>
                                <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>{project.project_name}</Typography>
                                <Typography variant="caption" display="block">{project.builder_name}</Typography>
                                <Typography variant="caption" color="primary">{project.budget_raw}</Typography>
                            </Box>
                        </Popup>
                    </Marker>
                ))}
            </MapContainer>
        </Box>
    );
};

export default HeatmapPage;
