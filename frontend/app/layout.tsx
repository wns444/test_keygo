import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'KeyGo - Internal Task Tracker',
  description: 'Internal task tracker for booking management',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
