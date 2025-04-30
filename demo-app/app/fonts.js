import { JetBrains_Mono, Rubik } from 'next/font/google'

export const jetBrainsMono = JetBrains_Mono({
  variable: '--font-jetbrains-mono',
  subsets: ['latin'],
  display: 'swap',
})

export const rubik = Rubik({
    variable: '--font-rubik',
    subsets: ['latin'],
    display: 'swap',
    weight: ['400', '500', '700'], // adjust weights as needed
})