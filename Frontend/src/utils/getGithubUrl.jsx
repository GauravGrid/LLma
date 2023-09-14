export function getGitHubUrl(from) {
    const rootURl = 'https://github.com/login/oauth/authorize';
    const options = {
      client_id: import.meta.env.VITE_REACT_APP_GITHUB_CLIENT_ID,
      redirect_uri: "http://127.0.0.1:8000/auth/github/callback/",
      scope: 'read:user repo',
      state: from,
    };
  
    const qs = new URLSearchParams(options);
  
    return `${rootURl}?${qs.toString()}`;
  }
  
