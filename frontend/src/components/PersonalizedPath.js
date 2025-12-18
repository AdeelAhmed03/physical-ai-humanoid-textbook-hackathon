import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { authClient } from '../auth/client';
import config from '../config';
import styles from './PersonalizedPath.module.css';

const PersonalizedPath = ({ currentChapter, onPathChange }) => {
  const { user } = useAuth();
  const [learningPath, setLearningPath] = useState('standard');
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  const pathOptions = [
    { id: 'beginner', name: 'Beginner', description: 'Start from the basics' },
    { id: 'intermediate', name: 'Intermediate', description: 'Skip the basics, focus on core concepts' },
    { id: 'advanced', name: 'Advanced', description: 'Dive deep into advanced topics' },
    { id: 'standard', name: 'Standard', description: 'Follow the recommended path' },
    { id: 'software-focused', name: 'Software Focus', description: 'Emphasize programming and implementation' },
    { id: 'hardware-focused', name: 'Hardware Focus', description: 'Emphasize theory and hardware concepts' }
  ];

  // Get personalized learning path recommendation based on user background
  useEffect(() => {
    if (user) {
      fetchRecommendation();
    }
  }, [user]);

  const fetchRecommendation = async () => {
    if (!user) return;

    setLoading(true);
    try {
      // Use Better-Auth's session to get the token
      const session = await authClient.getSession();
      const token = session?.data?.session?.accessToken;

      if (!token) {
        console.error('No session token available');
        return;
      }

      const response = await fetch(`${config.API_BASE_URL}/personalization/learning-path`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setRecommendation(data.personalization_data);
        if (data.personalization_data?.path) {
          setLearningPath(data.personalization_data.path);
        }
      }
    } catch (error) {
      console.error('Error fetching learning path recommendation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePathChange = (pathId) => {
    setLearningPath(pathId);

    if (onPathChange) {
      onPathChange(pathId);
    }
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Your Learning Path</h3>

      {loading && <p>Loading personalized recommendations...</p>}

      {!loading && (
        <div className={styles.pathSelector}>
          {pathOptions.map((path) => (
            <button
              key={path.id}
              className={`${styles.pathOption} ${
                learningPath === path.id ? styles.selected : ''
              }`}
              onClick={() => handlePathChange(path.id)}
            >
              <div className={styles.pathHeader}>
                <h4 className={styles.pathName}>{path.name}</h4>
                <span className={styles.pathBadge}>
                  {learningPath === path.id ? 'Active' : 'Select'}
                </span>
              </div>
              <p className={styles.pathDescription}>{path.description}</p>
            </button>
          ))}
        </div>
      )}

      {recommendation && (
        <div className={styles.recommendation}>
          <h4>Recommended for you:</h4>
          <p>{recommendation.reason}</p>
          {recommendation.suggested_order && (
            <div className={styles.suggestedOrder}>
              <h5>Suggested order:</h5>
              <ul>
                {recommendation.suggested_order.slice(0, 3).map((chapter, index) => (
                  <li key={index}>{chapter}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PersonalizedPath;