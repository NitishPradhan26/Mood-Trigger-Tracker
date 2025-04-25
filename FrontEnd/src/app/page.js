'use client';
import React, { useState } from 'react';
import Client from './client.js';
import Psychiatrist from './psychiatrist.js';
import styles from './page.module.css';

export default function Home() {
  const [selectedView, setSelectedView] = useState(null);

  return (
    <main className={styles.main}>
      <div className={styles.header}>
        <h1>Mental Health Tracker</h1>
        <p>Supporting better mental health through awareness and tracking</p>
      </div>

      <div className={styles.navigation}>
        <button 
          className={`${styles.navButton} ${selectedView === 'client' ? styles.selected : ''}`}
          onClick={() => setSelectedView('client')}
        >
          Client View
        </button>
        <button 
          className={`${styles.navButton} ${selectedView === 'psychiatrist' ? styles.selected : ''}`}
          onClick={() => setSelectedView('psychiatrist')}
        >
          Psychiatrist View
        </button>
      </div>

      <div className={styles.content}>
        {selectedView === 'client' && <Client />}
        {selectedView === 'psychiatrist' && <Psychiatrist />}
        {!selectedView && (
          <div className={styles.welcomeMessage}>
            <h2>Welcome!</h2>
            <p>Please select a view to continue</p>
          </div>
        )}
      </div>
    </main>
  );
}
