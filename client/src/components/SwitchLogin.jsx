import React from "react";
import "../styles/signup.css";
import { useState } from "react";
import SignUp from "./SignUp";
import LogIn from "./LogIn";
// MUI imports
import Paper from "@mui/material/Paper";
import Chip from "@mui/material/Chip";
import LockOpenIcon from "@mui/icons-material/LockOpen";
import LockIcon from "@mui/icons-material/Lock";
import Switch from "@mui/material/Switch";

function SwitchLogin() {
  const [checked, setChecked] = useState(true); // Changed to useState instead of React.useState

  const handleChange = (event) => {
    setChecked(event.target.checked);
  };

  return (
    <div className="signup-container">
      <Paper elevation={3}>
        {checked ? (
          <Chip
            icon={<LockOpenIcon />}
            label="Sign Up"
            color="primary"
            variant="outlined"
          />
        ) : (
          <Chip
            icon={<LockIcon />}
            label="Log In"
            color="primary"
            variant="outlined"
          />
        )}
        <br />
        <Switch
          checked={checked}
          onChange={handleChange}
          inputProps={{ "aria-label": "controlled" }}
        />
        <br/>
        {checked ? <SignUp /> : <LogIn />}
      </Paper>
    </div>
  );
}

export default SwitchLogin;
