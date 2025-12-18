import React from 'react';
import { useDocsPreferredVersion, useDocsVersion } from '@docusaurus/plugin-content-docs/client';
import { useLocation } from '@docusaurus/router';
import clsx from 'clsx';
import styles from './TextbookNavigation.module.css';

function TextbookNavigation() {
  const location = useLocation();
  const preferredVersion = useDocsPreferredVersion('default');
  const version = useDocsVersion('default');
  
  // For a textbook, we'll create navigation based on our chapter structure
  const chapters = [
    { id: 'intro-physical-ai', title: 'Introduction to Physical AI', path: '/docs/intro-physical-ai' },
    { id: 'humanoid-robotics', title: 'Basics of Humanoid Robotics', path: '/docs/humanoid-robotics' },
    { id: 'ros2-fundamentals', title: 'ROS 2 Fundamentals', path: '/docs/ros2-fundamentals' },
    { id: 'digital-twin-simulation', title: 'Digital Twin Simulation', path: '/docs/digital-twin-simulation' },
    { id: 'vision-language-action', title: 'Vision-Language-Action Systems', path: '/docs/vision-language-action' },
    { id: 'capstone-project', title: 'Capstone: Simple AI-Robot Pipeline', path: '/docs/capstone-project' },
  ];

  // Determine current chapter based on URL
  const currentChapterIndex = chapters.findIndex(chapter => 
    location.pathname.startsWith(chapter.path)
  );

  const previousChapter = currentChapterIndex > 0 ? chapters[currentChapterIndex - 1] : null;
  const nextChapter = currentChapterIndex < chapters.length - 1 ? chapters[currentChapterIndex + 1] : null;

  return (
    <div className={clsx('pagination-nav', styles.textbookNavigation)}>
      <div className="container">
        <div className="row">
          {previousChapter && (
            <div className="col col--5">
              <div className="card-demo padding--sm">
                <a className="button button--outline button--primary" href={previousChapter.path}>
                  ← Previous: {previousChapter.title}
                </a>
              </div>
            </div>
          )}
          
          <div className="col text--center">
            <div className="dropdown dropdown--hoverable dropdown--right">
              <button className="button button--secondary">Table of Contents</button>
              <ul className="dropdown__menu">
                {chapters.map((chapter, index) => (
                  <li key={chapter.id}>
                    <a 
                      className={clsx(
                        'dropdown__link',
                        currentChapterIndex === index && 'dropdown__link--active'
                      )} 
                      href={chapter.path}
                    >
                      {index + 1}. {chapter.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          {nextChapter && (
            <div className="col col--5">
              <div className="card-demo padding--sm text--right">
                <a className="button button--outline button--primary" href={nextChapter.path}>
                  Next: {nextChapter.title} →
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TextbookNavigation;