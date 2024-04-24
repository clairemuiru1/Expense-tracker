import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Signin.css";
 
function Signin({ setShowLogin }) {
  const navigate = useNavigate();
 
  const [currentState, setCurrentState] = useState("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
 
  const handleSignup = (event) => {
    event.preventDefault();
 
    fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to create user");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data.message); // Log the success message
        // Redirect the user to the home page after successful signup
        navigate("/");
      })
      .catch((error) => {
        console.error("Error:", error);
        // Optionally, you can show an error message to the user
      });
  };
 
  const handleLogin = (event) => {
    event.preventDefault(); // Prevent the form from submitting normally
 
    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Invalid username or password");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data.token); // Log the token
        localStorage.setItem("token", data.token);
        // Optionally, you can store the token in local storage or session storage
        navigate("/");
      })
      .catch((error) => {
        console.error("Error:", error);
        // Optionally, you can show an error message to the user
      });
  };
 
  return (
    <div className="login-popup">
      <form className="login-popup-container">
        <div className="login-popup-title">
          <h2>{currentState}</h2>
          <img
            src="https://icons.veryicon.com/png/o/miscellaneous/medium-thin-linear-icon/cross-23.png"
            alt="close"
            onClick={() => setShowLogin(false)}
          />
        </div>
        <div className="login-popup-inputs">
          {currentState === "login" ? (
            <input
              type="text"
              placeholder="Username"
              required
              onChange={(e) => setUsername(e.target.value)}
            />
          ) : (
            <input
              type="text"
              placeholder="Your name"
              required
              onChange={(e) => setUsername(e.target.value)}
            />
          )}
          <input
            type="email"
            placeholder="Your email"
            required
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            required
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button
          onClick={currentState === "Sign Up" ? handleSignup : handleLogin}
        >
          {currentState === "Sign Up" ? "Create Account" : "Login"}
        </button>
        <div className="login-popup-condition">
          <input type="checkbox" required />
          <p>By Continuing. I agree to the terms of use & privacy policy.</p>
        </div>
        {currentState === "login" ? (
          <p>
            Create a new account?{" "}
            <span onClick={() => setCurrentState("Sign Up")}>Click Here</span>
          </p>
        ) : (
          <p>
            Already have an account?{" "}
            <span onClick={() => setCurrentState("Login")}>Login here</span>
          </p>
        )}
      </form>
    </div>
  );
}
 
export default Signin;