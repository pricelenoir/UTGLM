import './globals.css'
import { jetBrainsMono } from './fonts'

export const metadata = {
  title: 'Golf Launch Monitor Demo',
  description: 'BLE-connected golf shot visualizer',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={jetBrainsMono.className}>
      <body className="bg-background text-foreground">
        {children}
      </body>
    </html>
  )
}