import Link from 'next/link';
import styles from './page.module.css';

export default function Home() {
  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>KeyGo Internal Task Tracker</h1>
        
        <p className={styles.description}>
          Welcome to the Internal Task Tracker for KeyGo booking management system.
        </p>

        <div className={styles.section}>
          <h2>📋 About</h2>
          <p>
            This application helps teams manage internal tasks related to bookings. 
            When issues arise with a booking, staff can create internal tasks to track resolution.
          </p>
        </div>

        <div className={styles.section}>
          <h2>🚀 Quick Start</h2>
          <p>To view tasks for a specific booking, use the URL format:</p>
          <code className={styles.code}>/bookings/[BOOKING_ID]</code>
          
          <p className={styles.example}>
            Example: <Link href="/bookings/1" className={styles.link}>/bookings/1</Link>
          </p>
        </div>

        <div className={styles.section}>
          <h2>✨ Features</h2>
          <ul>
            <li>Create internal tasks for bookings</li>
            <li>Track task status (Open → In Progress → Resolved → Closed)</li>
            <li>Filter tasks by status</li>
            <li>Real-time updates</li>
            <li>Error handling and validation</li>
          </ul>
        </div>

        <div className={styles.section}>
          <h2>📚 Documentation</h2>
          <ul>
            <li><Link href="https://github.com/wns444/test_keygo/blob/master/README.md" className={styles.link}>Project README</Link></li>
            <li><Link href="https://github.com/wns444/test_keygo/blob/master/backend/README.md" className={styles.link}>Backend Documentation</Link></li>
            <li><Link href="https://github.com/wns444/test_keygo/blob/master/frontend/README.md" className={styles.link}>Frontend Documentation</Link></li>
          </ul>
        </div>
      </div>
    </main>
  );
}
