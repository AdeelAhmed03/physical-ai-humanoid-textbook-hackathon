import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './AuthForm.module.css';

const RegistrationForm = ({ onSwitchToLogin }) => {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    software_background: '',
    hardware_background: '',
    experience_level: 'beginner'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await register(formData);
      if (!result.success) {
        setError(result.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <h2>Create Account</h2>
      {error && <div className={styles.error}>{error}</div>}

      <form onSubmit={handleSubmit} className={styles.authForm}>
        <div className={styles.formGroup}>
          <label htmlFor="full_name">Full Name</label>
          <input
            type="text"
            id="full_name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="software_background">Software Background</label>
          <textarea
            id="software_background"
            name="software_background"
            value={formData.software_background}
            onChange={handleChange}
            placeholder="Describe your software development experience, programming languages you know, etc."
            rows="3"
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="hardware_background">Hardware Background</label>
          <textarea
            id="hardware_background"
            name="hardware_background"
            value={formData.hardware_background}
            onChange={handleChange}
            placeholder="Describe your hardware experience, robotics, electronics, etc."
            rows="3"
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="experience_level">Experience Level</label>
          <select
            id="experience_level"
            name="experience_level"
            value={formData.experience_level}
            onChange={handleChange}
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <button type="submit" disabled={loading} className={styles.submitButton}>
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <p className={styles.switchForm}>
        Already have an account?{' '}
        <button onClick={onSwitchToLogin} className={styles.linkButton}>
          Sign In
        </button>
      </p>
    </div>
  );
};

export default RegistrationForm;