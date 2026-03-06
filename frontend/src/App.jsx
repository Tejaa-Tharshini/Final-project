import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { Container, Typography, Box, CircularProgress, Alert, Grid, Button } from '@mui/material';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FiltersBar from './components/FiltersBar';
import MetricsCards from './components/MetricsCards';
import BuildersBarChart from './components/BuildersBarChart';
import ProjectsTable from './components/ProjectsTable';
import BackgroundContainer from './components/BackgroundContainer';
import HeatmapPage from './pages/HeatmapPage';
import { calculateMedian } from './utils';

const API_BASE_URL = 'http://localhost:8000';

function Dashboard({
  projects,
  loading,
  error,
  states,
  cities,
  selectedState,
  setSelectedState,
  selectedCity,
  setSelectedCity,
  selectedStatus,
  setSelectedStatus
}) {
  const currentMedian = useMemo(() => {
    const budgets = projects
      .filter(p => p.budget_num)
      .map(p => p.budget_num);
    return calculateMedian(budgets);
  }, [projects]);

  return (
    <Container maxWidth="xl" sx={{ py: 4, position: 'relative', zIndex: 1 }}>
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h3" className="premium-gradient-text" sx={{ fontWeight: 800, mb: 1 }}>
            Real-Time Website Lead Monitoring System
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ opacity: 0.8 }}>
            Monitoring Dashboard
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Button
            component={Link}
            to="/heatmap"
            variant="outlined"
            color="primary"
            sx={{ borderRadius: 2, border: '2px solid' }}
          >
            View Heatmap
          </Button>
          {loading && <CircularProgress size={24} />}
        </Box>
      </Box>

      <FiltersBar
        states={states}
        cities={cities}
        selectedState={selectedState}
        onStateChange={setSelectedState}
        selectedCity={selectedCity}
        onCityChange={setSelectedCity}
        selectedStatus={selectedStatus}
        onStatusChange={setSelectedStatus}
        onApply={() => { }} // Filters are live in this implementation
      />

      <MetricsCards
        total={projects.length}
        byStatus={projects.reduce((acc, p) => {
          acc[p.status] = (acc[p.status] || 0) + 1;
          return acc;
        }, {})}
        medianBudget={currentMedian}
        selectedCity={selectedCity || selectedState}
      />

      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <BuildersBarChart
            projects={projects}
            selectedState={selectedState}
            selectedCity={selectedCity}
          />
        </Grid>
        <Grid item xs={12} lg={4}>
          <ProjectsTable projects={projects} />
        </Grid>
      </Grid>
    </Container>
  );
}

function App() {
  const [allProjects, setAllProjects] = useState([]);
  const [states, setStates] = useState([]);
  const [allCities, setAllCities] = useState([]); // Map of state -> [cities]

  const [selectedState, setSelectedState] = useState('');
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('all');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        const [statesRes, projectsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/states`),
          axios.get(`${API_BASE_URL}/projects?limit=50000`) // Fetch all for instant filtering
        ]);

        setStates(statesRes.data);
        setAllProjects(projectsRes.data);

        // Build city mapping for dependent dropdown
        const cityMap = projectsRes.data.reduce((acc, p) => {
          if (!acc[p.state]) acc[p.state] = new Set();
          if (p.city) acc[p.state].add(p.city);
          return acc;
        }, {});

        setAllCities(Object.fromEntries(
          Object.entries(cityMap).map(([s, c]) => [s, Array.from(c).sort()])
        ));

      } catch (err) {
        setError("Connection failed. Please check backend.");
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const filteredProjects = useMemo(() => {
    return allProjects.filter(p => {
      const stateMatch = !selectedState || p.state === selectedState;
      const cityMatch = !selectedCity || p.city === selectedCity;
      const statusMatch = selectedStatus === 'all' || p.status === selectedStatus;
      return stateMatch && cityMatch && statusMatch;
    });
  }, [allProjects, selectedState, selectedCity, selectedStatus]);

  // Reset city if state changes
  useEffect(() => {
    setSelectedCity('');
  }, [selectedState]);

  return (
    <Router>
      <BackgroundContainer selectedState={selectedState}>
        <Routes>
          <Route path="/" element={
            <Dashboard
              projects={filteredProjects}
              loading={loading}
              error={error}
              states={states}
              cities={selectedState ? (allCities[selectedState] || []) : []}
              selectedState={selectedState}
              setSelectedState={setSelectedState}
              selectedCity={selectedCity}
              setSelectedCity={setSelectedCity}
              selectedStatus={selectedStatus}
              setSelectedStatus={setSelectedStatus}
            />
          } />
          <Route path="/heatmap" element={
            <HeatmapPage
              projects={filteredProjects}
              selectedState={selectedState}
              selectedCity={selectedCity}
            />
          } />
        </Routes>
      </BackgroundContainer>
    </Router>
  );
}

export default App;
