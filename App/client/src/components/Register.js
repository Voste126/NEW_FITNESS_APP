import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './register.css';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '', // Added email field
    phone_number: '', // Added phone_number field
  });
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    // Create a JSON object with the user registration data
    const userData = {
      username: formData.username,
      password: formData.password,
      user_email: formData.email, // Updated field name
      user_phone_number: formData.phone_number, // Added phone_number field
    };

    // Send a POST request to your Flask backend to register the user
    fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response or show a success message
        setFormData({
          username: '',
          password: '',
          email: '', // Clear email field
          phone_number: '', // Clear phone_number field
        });
        setTimeout(() => {
          navigate('/login');
        }, 1000);

        // Assuming your Flask backend returns an access token for the registered user
        const accessToken = data.access_token;

        // Save the access token to localStorage or state
        localStorage.setItem('access_token', accessToken);

        // Redirect to the home page or any other desired location
        navigate('/home');
      });
  };

  return (
    <div>
      <div className="centered-form">
        <div className="register-container">
          <h2>Register</h2>
          <h3>Please make sure you have a unique username, email,phone number, password to get registered</h3>
          <form onSubmit={handleSubmit}>
            <div className="register-input">
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
                <label htmlFor="email">Email:
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </label>
              </div>
              <div>
                <label htmlFor="phone_number">Phone Number:
                  <input
                    type="text"
                    id="phone_number"
                    name="phone_number"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
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
            <div className="register-button">
              <button type="submit">Register</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Register;
