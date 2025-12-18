import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import styles from './UserProfile.module.css';

const UserProfile = () => {
  const { user, logout } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className={styles.userProfile}>
      <div className={styles.userInfo}>
        <h3>Welcome, {user.full_name}</h3>
        <p><strong>Email:</strong> {user.email}</p>
        {user.software_background && (
          <p><strong>Software Background:</strong> {user.software_background}</p>
        )}
        {user.hardware_background && (
          <p><strong>Hardware Background:</strong> {user.hardware_background}</p>
        )}
        {user.experience_level && (
          <p><strong>Experience Level:</strong> {user.experience_level}</p>
        )}
      </div>
      <button onClick={logout} className={styles.logoutButton}>
        Logout
      </button>
    </div>
  );
};

export default UserProfile;