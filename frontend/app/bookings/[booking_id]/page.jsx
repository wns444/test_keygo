'use client';

import { useParams } from 'next/navigation';
import InternalTasks from '@/components/InternalTasks';
import styles from './page.module.css';

export default function BookingPage() {
  const params = useParams();
  const bookingId = params.booking_id;

  return (
    <main className={styles.main}>
      <div className={styles.header}>
        <h1>Booking Details</h1>
        <p className={styles.bookingInfo}>Booking ID: <code>{bookingId}</code></p>
      </div>

      <InternalTasks bookingId={bookingId} />
    </main>
  );
}
