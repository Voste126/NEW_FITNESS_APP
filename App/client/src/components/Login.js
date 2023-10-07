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
      .then((data) => {
        const accessToken = data.access_token;
        localStorage.setItem('access_token', accessToken);
        setTimeout(() => {
          navigate('/home');
        }, 2000);
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
                <label htmlFor="username">Username:
                  <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                </label>
              </div>
              <div>
                <label htmlFor="password">Password:
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </label>
              </div>
            </div>
            <div className="login-button">
              <button type="submit">Login</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
