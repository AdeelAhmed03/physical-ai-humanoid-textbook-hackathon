import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro-physical-ai/introduction">
            Start Reading - 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An interactive textbook with RAG-powered AI assistance for Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container padding-horiz--md">
            <div className="row">
              <div className="col col--4">
                <h2>Comprehensive Coverage</h2>
                <p>
                  Explore 6 in-depth chapters covering Physical AI, Humanoid Robotics, 
                  ROS 2, Digital Twin Simulation, Vision-Language-Action Systems, 
                  and a Capstone Project.
                </p>
              </div>
              <div className="col col--4">
                <h2>Interactive Learning</h2>
                <p>
                  Ask questions directly about the content and get AI-powered responses 
                  based solely on the textbook material, ensuring accuracy and relevance.
                </p>
              </div>
              <div className="col col--4">
                <h2>Advanced Technologies</h2>
                <p>
                  Learn about cutting-edge technologies including RAG systems, 
                  digital twin simulation, and vision-language-action integration.
                </p>
              </div>
            </div>
          </div>
        </section>
        
        <section className={styles.chapterPreview}>
          <div className="container padding-vert--xl text--center">
            <h2>Textbook Chapters</h2>
            <div className="row">
              <div className="col col--2 col--offset-1">
                <Link className="button button--primary" to="/docs/intro-physical-ai/introduction">
                  1. Physical AI
                </Link>
              </div>
              <div className="col col--2">
                <Link className="button button--primary" to="/docs/humanoid-robotics/basics">
                  2. Humanoid Robotics
                </Link>
              </div>
              <div className="col col--2">
                <Link className="button button--primary" to="/docs/ros2-fundamentals/core-concepts">
                  3. ROS 2 Fundamentals
                </Link>
              </div>
              <div className="col col--2">
                <Link className="button button--primary" to="/docs/digital-twin-simulation/gazebo-isaac">
                  4. Digital Twin Simulation
                </Link>
              </div>
              <div className="col col--2">
                <Link className="button button--primary" to="/docs/vision-language-action/systems">
                  5. Vision-Language-Action
                </Link>
              </div>
            </div>
            <div className="row" style={{marginTop: '1rem'}}>
              <div className="col col--2 col--offset-5">
                <Link className="button button--primary" to="/docs/capstone-project/pipeline">
                  6. Capstone Project
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}