import React from 'react';
import {
    Container,
    Paper,
    Typography,
    Grid,
    Card,
    CardContent,
    Box,
    Chip,
    LinearProgress,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Divider
} from '@mui/material';
import {
    CheckCircle,
    Science,
    Storage,
    People,
    TrendingUp
} from '@mui/icons-material';

export default function ModelTraining() {
    const flRounds = [
        { round: 1, hospitals: 3, accuracy: 95.2, loss: 0.145 },
        { round: 2, hospitals: 3, accuracy: 98.1, loss: 0.052 },
        { round: 3, hospitals: 3, accuracy: 100.0, loss: 0.012 }
    ];

    const hospitals = [
        { name: 'Italy', samples: 1000, normal: 700, minor: 250, major: 50 },
        { name: 'Pakistan', samples: 1000, normal: 500, minor: 350, major: 150 },
        { name: 'USA', samples: 1000, normal: 750, minor: 200, major: 50 }
    ];

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Science sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
                <Typography variant="h3">
                    Federated Learning Model Training
                </Typography>
            </Box>

            {/* Status Cards */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <CheckCircle color="success" sx={{ mr: 1 }} />
                                <Typography variant="h6" color="success.main">
                                    Status
                                </Typography>
                            </Box>
                            <Typography variant="h4">Complete</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Training finished successfully
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <TrendingUp color="primary" sx={{ mr: 1 }} />
                                <Typography variant="h6" color="primary">
                                    FL Rounds
                                </Typography>
                            </Box>
                            <Typography variant="h4">3</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Federated aggregation rounds
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <People color="info" sx={{ mr: 1 }} />
                                <Typography variant="h6" color="info.main">
                                    Hospitals
                                </Typography>
                            </Box>
                            <Typography variant="h4">3</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Italy, Pakistan, USA
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Storage color="warning" sx={{ mr: 1 }} />
                                <Typography variant="h6" color="warning.main">
                                    Final Accuracy
                                </Typography>
                            </Box>
                            <Typography variant="h4">100%</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Global model performance
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Training Progress */}
            <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h5" gutterBottom>
                    Training Progress by Round
                </Typography>
                <Divider sx={{ mb: 2 }} />

                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell><strong>Round</strong></TableCell>
                                <TableCell><strong>Hospitals</strong></TableCell>
                                <TableCell><strong>Accuracy</strong></TableCell>
                                <TableCell><strong>Loss</strong></TableCell>
                                <TableCell><strong>Progress</strong></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {flRounds.map((round) => (
                                <TableRow key={round.round}>
                                    <TableCell>Round {round.round}</TableCell>
                                    <TableCell>{round.hospitals}</TableCell>
                                    <TableCell>
                                        <Chip
                                            label={`${round.accuracy}%`}
                                            color={round.accuracy === 100 ? "success" : "primary"}
                                            size="small"
                                        />
                                    </TableCell>
                                    <TableCell>{round.loss.toFixed(3)}</TableCell>
                                    <TableCell>
                                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                            <Box sx={{ width: '100%', mr: 1 }}>
                                                <LinearProgress
                                                    variant="determinate"
                                                    value={round.accuracy}
                                                    color={round.accuracy === 100 ? "success" : "primary"}
                                                />
                                            </Box>
                                            <Box sx={{ minWidth: 35 }}>
                                                <Typography variant="body2" color="text.secondary">
                                                    {round.accuracy}%
                                                </Typography>
                                            </Box>
                                        </Box>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>

            {/* Hospital Data Distribution */}
            <Paper sx={{ p: 3 }}>
                <Typography variant="h5" gutterBottom>
                    Hospital Data Distribution
                </Typography>
                <Divider sx={{ mb: 2 }} />

                <Grid container spacing={2}>
                    {hospitals.map((hospital) => (
                        <Grid item xs={12} md={4} key={hospital.name}>
                            <Card variant="outlined">
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        {hospital.name}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        Total Samples: {hospital.samples}
                                    </Typography>
                                    <Box sx={{ mt: 2 }}>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                            <Typography variant="body2">Normal:</Typography>
                                            <Typography variant="body2" fontWeight="bold">
                                                {hospital.normal} ({(hospital.normal / hospital.samples * 100).toFixed(1)}%)
                                            </Typography>
                                        </Box>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                            <Typography variant="body2">Minor:</Typography>
                                            <Typography variant="body2" fontWeight="bold">
                                                {hospital.minor} ({(hospital.minor / hospital.samples * 100).toFixed(1)}%)
                                            </Typography>
                                        </Box>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                            <Typography variant="body2">Major:</Typography>
                                            <Typography variant="body2" fontWeight="bold">
                                                {hospital.major} ({(hospital.major / hospital.samples * 100).toFixed(1)}%)
                                            </Typography>
                                        </Box>
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Paper>

            {/* Model Info */}
            <Paper sx={{ p: 3, mt: 3, bgcolor: 'success.light', color: 'success.contrastText' }}>
                <Typography variant="h6" gutterBottom>
                    ✓ Model Successfully Trained
                </Typography>
                <Typography variant="body2">
                    The federated learning model has been trained across 3 hospitals with 3,000 samples total.
                    The final global model achieved 100% accuracy and is ready for deployment.
                </Typography>
                <Box sx={{ mt: 2 }}>
                    <Chip label="Model Size: 18.6 KB" sx={{ mr: 1 }} />
                    <Chip label="Blockchain: 13 blocks" sx={{ mr: 1 }} />
                    <Chip label="Privacy-Preserving: Yes" />
                </Box>
            </Paper>
        </Container>
    );
}
