import React, { useState, useEffect } from 'react';
import styles from './LanguageSelector.module.css';

const LanguageSelector = ({ currentLanguage = 'en', onLanguageChange }) => {
  const [selectedLanguage, setSelectedLanguage] = useState(currentLanguage);
  const [isOpen, setIsOpen] = useState(false);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'ur', name: 'Urdu' }
  ];

  useEffect(() => {
    setSelectedLanguage(currentLanguage);
  }, [currentLanguage]);

  const handleLanguageSelect = (languageCode) => {
    setSelectedLanguage(languageCode);
    setIsOpen(false);
    if (onLanguageChange) {
      onLanguageChange(languageCode);
    }
  };

  return (
    <div className={styles.languageSelector}>
      <button 
        className={styles.languageButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Select language"
      >
        {languages.find(lang => lang.code === selectedLanguage)?.name || 'Language'}
        <span className={styles.arrow}>{isOpen ? '▲' : '▼'}</span>
      </button>
      
      {isOpen && (
        <div className={styles.languageDropdown}>
          {languages.map((language) => (
            <button
              key={language.code}
              className={`${styles.languageOption} ${
                selectedLanguage === language.code ? styles.selected : ''
              }`}
              onClick={() => handleLanguageSelect(language.code)}
            >
              {language.name}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default LanguageSelector;