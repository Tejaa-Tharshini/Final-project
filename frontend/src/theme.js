import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#58a6ff',
            contrastText: '#ffffff',
        },
        secondary: {
            main: '#bc8cff',
        },
        background: {
            default: '#0d1117',
            paper: '#161b22',
        },
        text: {
            primary: '#c9d1d9',
            secondary: '#8b949e',
        },
        divider: 'rgba(48, 54, 61, 0.8)',
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h4: {
            fontWeight: 800,
            letterSpacing: '-0.02em',
        },
        h6: {
            fontWeight: 600,
        },
    },
    shape: {
        borderRadius: 12,
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none',
                    fontWeight: 600,
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                    border: '1px solid rgba(48, 54, 61, 0.8)',
                },
            },
        },
    },
});

export default theme;
