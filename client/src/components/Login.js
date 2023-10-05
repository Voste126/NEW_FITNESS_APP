import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';

function Login() {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Create a JSON object with the user credentials
    const userCredentials = {
      username: formData.username,
      password: formData.password,
    };
  
    // Send a POST request to your Flask backend to login the user
    fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userCredentials),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Login failed');
        }
      })
      .then((data) => {
        // Assuming your Flask backend returns an access token
        const accessToken = data.access_token;
  
        // Save the access token to localStorage or state
        localStorage.setItem('access_token', accessToken);
  
        // Show a success message
        alert('Login successful');
  
        // Redirect to the home page after a delay
        setTimeout(() => {
          navigate('/home');
        }, 2000); // Adjust the delay time as needed
      })
      .catch((error) => {
        // Handle login error, e.g., show an error message
        console.error('Login failed:', error);
      });
  };
  

  return (
    <div>
        <div className="centered-form">
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="login-input">
            <div>
              <label htmlFor="username">Username:</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                required
              />
            </div>
            <div>
              <label htmlFor="password">Password:</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                required
              />
            </div>
          </div>
          <div className="login-button">
            <button type="submit">Login</button>
          </div>
        </form>
      </div>
      </div>
    </div>
  )
}

export default Login
