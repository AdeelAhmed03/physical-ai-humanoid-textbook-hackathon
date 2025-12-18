import React, { useState } from 'react';
import LoginForm from './LoginForm';
import RegistrationForm from './RegistrationForm';
import styles from './AuthWrapper.module.css';

const AuthWrapper = () => {
  const [isLoginView, setIsLoginView] = useState(true);

  const switchToLogin = () => setIsLoginView(true);
  const switchToRegister = () => setIsLoginView(false);

  return (
    <div className={styles.authWrapper}>
      <div className={styles.authCard}>
        {isLoginView ? (
          <LoginForm onSwitchToRegister={switchToRegister} />
        ) : (
          <RegistrationForm onSwitchToLogin={switchToLogin} />
        )}
      </div>
    </div>
  );
};

export default AuthWrapper;