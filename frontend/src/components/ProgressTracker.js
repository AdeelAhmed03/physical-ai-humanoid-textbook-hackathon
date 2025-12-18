import React, { useState, useEffect } from 'react';
import config from '@site/src/config';
import { useTheme } from '../contexts/ThemeContext';
import './ProgressTracker.module.css';

const ProgressTracker = ({ chapterId, userId, title }) => {
  const [completed, setCompleted] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);
  const [loading, setLoading] = useState(true);
  const { isDark } = useTheme();

  useEffect(() => {
    loadProgress();
  }, [chapterId, userId]);

  const loadProgress = async () => {
    if (!userId || !chapterId) {
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${config.API_BASE_URL}/user/progress/${userId}`);
      if (response.ok) {
        const data = await response.json();
        const chapterProgress = data.progress.find(p => p.chapter_id === parseInt(chapterId));
        if (chapterProgress) {
          setCompleted(chapterProgress.completed);
          setTimeSpent(chapterProgress.time_spent || 0);
        }
      }
    } catch (error) {
      console.error('Error loading progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateProgress = async (completedStatus) => {
    if (!userId || !chapterId) return;

    try {
      const progressData = {
        user_id: userId,
        chapter_id: parseInt(chapterId),
        completed: completedStatus,
        time_spent: timeSpent
      };

      const response = await fetch(`${config.API_BASE_URL}/user/progress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(progressData)
      });

      if (response.ok) {
        setCompleted(completedStatus);
        // Update time spent to current if marking as completed
        if (completedStatus && timeSpent === 0) {
          setTimeSpent(Date.now()); // Actually store time in seconds later
        }
      } else {
        throw new Error('Failed to update progress');
      }
    } catch (error) {
      console.error('Error updating progress:', error);
      alert('Failed to update progress. Please try again.');
    }
  };

  const markAsRead = () => {
    updateProgress(true);
  };

  const markAsUnread = () => {
    updateProgress(false);
  };

  if (loading) {
    return <div className="progress-tracker">Loading progress...</div>;
  }

  return (
    <div className={`progress-tracker-container ${isDark ? 'dark-theme' : 'light-theme'}`}>
      <div className="progress-header">
        <h4>Chapter Progress</h4>
        <div className={`status-indicator ${completed ? 'completed' : 'incomplete'}`}>
          {completed ? '✓ Completed' : '○ Incomplete'}
        </div>
      </div>
      
      <div className="progress-actions">
        {!completed ? (
          <button 
            className="mark-complete-button"
            onClick={markAsRead}
          >
            Mark as Read
          </button>
        ) : (
          <button 
            className="mark-incomplete-button"
            onClick={markAsUnread}
          >
            Mark as Unread
          </button>
        )}
      </div>
      
      <div className="progress-stats">
        <div className="time-spent">
          Time spent: {formatTime(timeSpent)}
        </div>
      </div>
      
      <div className="progress-bar">
        <div 
          className={`progress-fill ${completed ? 'completed' : ''}`} 
          style={{ width: completed ? '100%' : '0%' }}
        ></div>
      </div>
    </div>
  );
};

const formatTime = (seconds) => {
  if (!seconds) return '0 min';
  
  // If seconds is a timestamp, calculate difference
  const duration = typeof seconds === 'number' && seconds > 10000000000 ? 
    Math.floor((Date.now() - seconds) / 1000) : seconds;
  
  const mins = Math.floor(duration / 60);
  return mins > 0 ? `${mins} min` : '< 1 min';
};

export default ProgressTracker;