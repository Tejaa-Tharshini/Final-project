import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Link, Chip, Box } from '@mui/material';
import { formatCurrency } from '../utils';

const ProjectsTable = ({ projects }) => {
    if (!projects || projects.length === 0) {
        return (
            <Paper className="glass-card" sx={{ p: 4, textAlign: 'center' }}>
                <Typography color="text.secondary">No projects found matching the filters.</Typography>
            </Paper>
        );
    }

    return (
        <TableContainer component={Paper} className="glass-card" sx={{ maxHeight: 600 }}>
            <Table stickyHeader>
                <TableHead>
                    <TableRow>
                        <TableCell sx={{ fontWeight: 600 }}>Project Name</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>Builder</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>City</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>Budget</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {projects.map((project) => (
                        <TableRow key={project.id} hover>
                            <TableCell>
                                <Typography variant="body2" sx={{ fontWeight: 600 }}>{project.project_name}</Typography>
                                <Typography variant="caption" color="text.secondary">{project.location_text}</Typography>
                            </TableCell>
                            <TableCell>
                                <Link href={project.builder_website} target="_blank" rel="noopener" sx={{ color: 'accent.color' }}>
                                    {project.builder_name}
                                </Link>
                            </TableCell>
                            <TableCell>{project.city}</TableCell>
                            <TableCell>
                                <Chip
                                    label={project.status}
                                    size="small"
                                    color={project.status === 'ongoing' ? 'primary' : project.status === 'completed' ? 'success' : 'default'}
                                    sx={{ textTransform: 'capitalize', fontWeight: 600 }}
                                />
                            </TableCell>
                            <TableCell>
                                {project.budget_num ? formatCurrency(project.budget_num) : project.budget_raw || 'N/A'}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default ProjectsTable;
