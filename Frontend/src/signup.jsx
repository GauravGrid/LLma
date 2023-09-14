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
import { setJwtToken } from "./login";



export default function SignUp() {
  const [confirmPassword, setConfirmPassword] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const[email,setEmail] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match");
      return;
    }
    else{
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/signup/",
            { "username": username, 
            "email":email,
             "password":password }
          );
          const  jwtToken  = response.data.token;
          sessionStorage.clear();
          setJwtToken(jwtToken);
    
          navigate("/repositories");
        } catch (error) {
          
          
            console.error("SignUp failed:", error.response.data.error);
            console.error("Failed");
            setErrorMessage(error.response.data.error);
          }
      }
    
    }
  return (
    <Grid container className="logo-grid-signup" component="main" sx={{ height: "100vh" }}>
      <CssBaseline />
    
      <Grid
        item
        sx={{
            backgroundColor: "white",
              opacity:0.8,
              borderRadius:'25px'
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
            my: 4,
            mx: 4,
            display: "flex",
            flexDirection: "column",
            alignItems: "left",
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
           Hi There!
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
            Sign Up
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
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
                className="email-input inputs"
                name="todo"
                type="text"
                placeholder="Email"
                value={email}
                required
                style={{ color: "#0474bb", fontFamily: "Nunito Sans" }}
                onChange={(e) => setEmail (e.target.value)}
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
                <input
  className="password-input inputs"
  name="todo"
  value={confirmPassword}
  required
  type="password"
  placeholder="Confirm Password"
  style={{
    color: "#0474bb",
    fontFamily: "Nunito Sans",
  }}
  onChange={(e) => setConfirmPassword(e.target.value)}
/>
              </form>
              <button
                className="login-button"
                type="submit"
                fullWidth
                variant="contained"
              >
                Register
              </button>
            </div>
            {errorMessage && <p className="error-message">{errorMessage}</p>}

            <Grid className="test1" container>
              <Grid item>
                <div className="sign-up-test">
                  <p style={{ color: "#0474bb" }}>Aleady Have An Account?</p>
                  <Link
                    style={{
                        textDecoration: "underline",
                        outline: 'none',
                        color: "#4D68D2",
                        fontSize:'16px',
                      }}
                    className="link-style"
                    onClick={() => {
                      navigate("/login");
                    }}
                    variant="body2"
                  >
                    {"Login"}
                  </Link>
                  
                </div>
                <div className="flex">
                <img src="/GDYN.svg" height={18} width={18} className="ml-4 mr-2" />
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