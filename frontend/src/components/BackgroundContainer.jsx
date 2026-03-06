import React from 'react';
import { Box, Typography } from '@mui/material';

const stateBackgrounds = {
    'Andaman and Nicobar Islands': '/backgrounds/Andaman and Nicobar.JPG',
    'Andhra Pradesh': '/backgrounds/Andhra pradesh.jpg',
    'Arunachal Pradesh': '/backgrounds/Arunachal Pradesh.jpg',
    'Assam': '/backgrounds/Assam.jpg',
    'Bihar': '/backgrounds/Bihar.jpg',
    'Chandigarh': '/backgrounds/Chandigarh.jpg',
    'Chhattisgarh': '/backgrounds/Chhattisgarh.jpg',
    'Dadra and Nagar Haveli and Daman and Diu': '/backgrounds/Dadra and Nagar Haveli.jpg',
    'Delhi': '/backgrounds/Delhi.jpg',
    'Goa': '/backgrounds/goa.jpg',
    'Gujarat': '/backgrounds/Gujarat.JPG',
    'Haryana': '/backgrounds/Haryana.jpg',
    'Himachal Pradesh': '/backgrounds/Himachal Pradesh.jpg',
    'Jammu and Kashmir': '/backgrounds/Jammu and Karshmir.jpg',
    'Jharkhand': '/backgrounds/Jharkhand.jpg',
    'Karnataka': '/backgrounds/karanataka.jpg',
    'Kerala': '/backgrounds/kerala.jpg',
    'Madhya Pradesh': '/backgrounds/Madhya pradesh.jpg',
    'Maharashtra': '/backgrounds/Maharashtra.jpg',
    'Meghalaya': '/backgrounds/Meghalaya.jpg',
    'Mizoram': '/backgrounds/Mizoram.jpg',
    'Nagaland': '/backgrounds/Nagaland.jpg',
    'Odisha': '/backgrounds/Odisha.jpg',
    'Punjab': '/backgrounds/Punjab.jpg',
    'Rajasthan': '/backgrounds/Rajasthan.jpg',
    'Sikkim': '/backgrounds/Sikkim.jpg',
    'Tamil Nadu': '/backgrounds/Tamil Nadu.jpg',
    'Telangana': '/backgrounds/Telangana.jpg',
    'Tripura': '/backgrounds/Tripura.jpg',
    'Uttar Pradesh': '/backgrounds/Uttar Pradesh.JPG',
    'Uttarakhand': '/backgrounds/Uttarakhand.jpg',
    'West Bengal': '/backgrounds/West Bengal.jpg',
};

const defaultBg = '/backgrounds/Delhi.jpg';

const BackgroundContainer = ({ children, selectedState }) => {
    // Normalize mapping lookup
    const stateKey = Object.keys(stateBackgrounds).find(
        key => key.toLowerCase().trim() === (selectedState || "").toLowerCase().trim()
    );

    const bgImage = stateKey ? stateBackgrounds[stateKey] : defaultBg;

    return (
        <Box
            sx={{
                position: 'relative',
                minHeight: '100vh',
                width: '100%',
                background: '#000',
            }}
        >
            {/* The Background Layer */}
            <Box
                sx={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundImage: `url("${bgImage}")`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    filter: 'brightness(0.8) contrast(1.1)',
                    transition: 'background-image 0.5s ease-in-out',
                    zIndex: 0,
                }}
            />
            {/* The Overlay to ensure text readability if needed */}
            <Box
                sx={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0,0,0,0.3)',
                    zIndex: 1,
                }}
            />
            {/* The Content Layer */}
            <Box sx={{ position: 'relative', zIndex: 2 }}>
                {children}
            </Box>

            {/* Debug Info (Can be removed later) */}
            <Typography variant="caption" sx={{ position: 'fixed', bottom: 10, right: 10, color: 'white', opacity: 0.3, zIndex: 100 }}>
                BG: {bgImage} | State: {selectedState}
            </Typography>
        </Box>
    );
};

export default BackgroundContainer;
