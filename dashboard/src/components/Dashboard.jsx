import React from 'react';
import { Box, Container, Typography, Paper, Grid, Card, CardContent } from '@mui/material';

export default function Dashboard() {
    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h3" gutterBottom>
                MedChain-FL Dashboard
            </Typography>

            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" color="primary">
                                FL Rounds
                            </Typography>
                            <Typography variant="h3">3</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Completed
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" color="primary">
                                Hospitals
                            </Typography>
                            <Typography variant="h3">3</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Italy, Pakistan, USA
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" color="primary">
                                Accuracy
                            </Typography>
                            <Typography variant="h3">100%</Typography>
                            <Typography variant="body2" color="text.secondary">
                                Final model
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h5" gutterBottom>
                            System Status
                        </Typography>
                        <Typography variant="body1" paragraph>
                            ✅ Federated Learning: Operational
                        </Typography>
                        <Typography variant="body1" paragraph>
                            ✅ Blockchain Ledger: 13 blocks
                        </Typography>
                        <Typography variant="body1" paragraph>
                            ✅ Global Model: Saved (18.6 KB)
                        </Typography>
                        <Typography variant="body1">
                            ✅ Data: 3,300 samples across 3 hospitals
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
}
