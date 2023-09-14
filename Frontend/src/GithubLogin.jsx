import React from 'react';
import { Box, Container, Typography, Link as MuiLink } from '@mui/material';
import { useLocation } from 'react-router-dom';
import GitHubLogo from './assets/github.svg';
import { getGitHubUrl } from './utils/getGithubUrl';

const GithubLoginPage = () => {
  const location = useLocation();
  let from = (location.state?.from?.pathname || '/');

  const handleGitHubLogin = () => {
    window.location.href = getGitHubUrl(from);
  };

  return (
    <Container
      maxWidth={false}
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#2363eb',
      }}
    >
      <Box width='27rem'>
        <Typography
          variant='h6'
          component='p'
          sx={{
            my: '1.5rem',
            textAlign: 'center',
            color: 'white',
          }}
        >
          Log in with Github:
        </Typography>
        <Box
          width='100%'
          sx={{
            backgroundColor: '#e5e7eb',
            p: { xs: '1rem', sm: '2rem' },
            borderRadius: 2,
          }}
        >
          <MuiLink
            onClick={handleGitHubLogin} 
            sx={{
              backgroundColor: '#f5f6f7',
              borderRadius: 1,
              py: '0.6rem',
              mt: '1.5rem',
              columnGap: '1rem',
              textDecoration: 'none',
              color: '#393e45',
              cursor: 'pointer',
              fontWeight: 500,
              '&:hover': {
                backgroundColor: '#fff',
                boxShadow: '0 1px 13px 0 rgb(0 0 0 / 15%)',
              },
            }}
            display='flex'
            justifyContent='center'
            alignItems='center'
          >
            <img src={GitHubLogo} alt="GitHub Logo" style={{ height: '2rem' }} />
            GitHub
          </MuiLink>
        </Box>
      </Box>
    </Container>
  );
};


export default GithubLoginPage;
