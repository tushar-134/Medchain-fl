import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './components/Dashboard';
import ModelTraining from './components/ModelTraining';
import Prediction from './components/Prediction';
import Blockchain from './components/Blockchain';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#4caf50',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              MedChain-FL
            </Typography>
            <Button color="inherit" component={Link} to="/">
              Dashboard
            </Button>
            <Button color="inherit" component={Link} to="/training">
              Model Training
            </Button>
            <Button color="inherit" component={Link} to="/prediction">
              Disease Prediction
            </Button>
            <Button color="inherit" component={Link} to="/blockchain">
              Blockchain
            </Button>
          </Toolbar>
        </AppBar>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/training" element={<ModelTraining />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/blockchain" element={<Blockchain />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
