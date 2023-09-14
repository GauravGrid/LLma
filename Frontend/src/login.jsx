import * as React from "react";
import { useState, useEffect } from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./login.css";
export function getJwtToken() {
    return sessionStorage.getItem("jwt")
}

export function setJwtToken(token) {
    sessionStorage.setItem("jwt", token)
}

export function deleteJwtToken(){
    sessionStorage.removeItem("jwt")
}

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/login/",
        { "username": username, 
         "password":password }
      );
      const  jwtToken  = response.data.token;
      sessionStorage.clear();
      setJwtToken(jwtToken);

      navigate("/repositories");
    } catch (error) {
      if (username === "" || password === "") {
        setErrorMessage("Please enter username and password");
      } else {
        console.error("Login failed:", error);
        console.error("Failed");
        setErrorMessage("Invalid Credentials");
      }
    }
  };

  return (
    <Grid container className="logo-grid" component="main" sx={{ height: "100vh" }}>
      <CssBaseline />
      <Grid
        item
        sx={{
          backgroundColor: "white",
            opacity:0.8,
            borderRadius:'25px',
          
        }}
         xs={12}
         sm={8}
         md={5}
        component={Paper}
        elevation={6}
        square
      >
        <Box
          sx={{
            my: 8,
            mx: 4,
            display: "flex",
            flexDirection: "column",
            alignItems: "left",
            marginTop: 4 + "rem",
            marginRight: 4 + "rem",
          }}
        >        
        <Typography className="sign-in-header login-headers">CodeBridge</Typography>

          <Typography
            className="welcome-back login-headers"
            sx={{
              color: "#0474bb",
              fontFamily: "Bebas Neue",
              letterSpacing: 2 + "px",
            }}
            component="h1"
            variant="h5"
          >
            Welcome Back
          </Typography>
          <Typography
            className="sign-in-header login-headers"
            sx={{
              color: "black",
              fontFamily: "Bebas Neue",
              letterSpacing: 2 + "px",
            }}
            component="h1"
            variant="h5"
          >
            Sign in
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleLogin}
            sx={{ mt: 1 }}
          >
            <div className="form-styler">
              <form className="user-input-form">
                <input
                  className="username-input inputs"
                  name="todo"
                  type="text"
                  placeholder="Username"
                  value={username}
                  required
                  style={{ color: "#0474bb", fontFamily: "Nunito Sans" }}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <input
                  className="password-input inputs"
                  name="todo"
                  value={password}
                  required
                  type="password"
                  placeholder="Password"
                  style={{
                    color: "#0474bb",
                    fontFamily: "Nunito Sans",
                  }}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </form>
              <button
                className="login-button"
                type="submit"
                fullWidth
                variant="contained"
              >
                Login
              </button>
            </div>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            <Grid className="test1" container>
              <Grid item>
                <div className="sign-up-test">
                  <p style={{ color: "#0474bb" }}>New?</p>
                  <Link
                    style={{
                      textDecoration: "underline",
                      outline: 'none',
                      color: "#4D68D2",
                      fontSize:'16px',
                    }}
                    className="link-style"
                    onClick={() => {
                      navigate("/signup");
                    }}
                    variant="body2"
                  >
                    {" Sign Up"}
                  </Link>
                </div>
                <div className="flex">
                <img src="/GDYN.svg" height={18} width={18} className="mr-2" />
                  <Typography sx={{
                  color: "#2B3140",
                  }} className="ml-2 mt-3">Grid Dynamics © 2023</Typography>
                </div>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}