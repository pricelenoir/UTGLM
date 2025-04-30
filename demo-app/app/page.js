'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { connectToBLE } from '@/lib/bluetooth'
import { rubik } from './fonts'


export default function Home() {
  const [device, setDevice] = useState(null)
  const [data, setData] = useState(null)
  const [selectedClub, setSelectedClub] = useState('7 Iron')

  const clubs = [
    'Driver',
    '3 Wood',
    '3 Iron',
    '4 Iron',
    '5 Iron',
    '6 Iron',
    '7 Iron',
    '8 Iron',
    '9 Iron',
    'Pitching Wedge',
    'Sand Wedge',
    'Lob Wedge',
  ]

  useEffect(() => {
    if (!device) return
    const interval = setInterval(() => {
      setData({
        carryDistance: Math.random() * 100 + 200,
        ballSpeed: Math.random() * 30 + 120,
        clubHeadSpeed: Math.random() * 20 + 100,
        smashFactor: Math.random() * 0.5 + 1.2,
        launchAngle: Math.random() * 15 + 10,
        apexHeight: Math.random() * 30 + 10,
      })
    }, 1000)
    return () => clearInterval(interval)
  }, [device])

  return (
    <main className="min-h-screen flex flex-col items-center bg-background text-foreground p-6">
      {/* Header */}
      <header className="w-full max-w-5xl flex flex-col items-center mb-10">
        <div className="flex items-center gap-4">
          <img src="/ut.png" alt="UT Logo" className="h-20 w-auto object-contain" />
          
          <h1 className={`text-5xl font-bold tracking-tight ${rubik.className}`}>
            Golf Launch Monitor
          </h1>
        </div>

        {/* Connected Device Text */}
        <div className="mt-2 text-sm text-gray-500">
          {device ? `Connected: ${device}` : 'Device not connected.'}
        </div>
      </header>
      {!device ? (
        <div className="flex flex-col items-center gap-6 mt-20 w-full max-w-md">
          {/* Bluetooth Connection Animation */}
          <div className="flex flex-col items-center gap-2">
            <img
              src="/bluetooth.png"
              alt="Bluetooth Logo"
              className="h-20 w-auto animate-bounce"
            />
            <p className="text-md text-center font-medium">
              Waiting for Bluetooth connection...
            </p>
            <p className="text-xs text-center text-gray-600">
              Please turn on your device and ensure Bluetooth is enabled.
            </p>
          </div>
          {/* Connect Button for testing */}
          <Button variant="outline" onClick={() => setDevice('Raspberry Pi 5')}>
            Connect to Launch Monitor
          </Button>
          
          {/*
          <Button variant="outline" onClick={async () => {const name = await connectToBLE() 
            if (name) {setDevice(name)}}}>
            Scan Bluetooth devices
          </Button>
          */}
        </div>
      ) : (
        <>
        <div className="relative w-full flex justify-center">
          {/* Club Selector */}
          <div className="w-40 flex flex-col items-center">
          <div className="w-full text-center mb-1">
            <label htmlFor="club-select" className="text-sm font-medium block text-left">
              Selected Club
            </label>
              <Select value={selectedClub} onValueChange={setSelectedClub}>
                <SelectTrigger id="club-select">
                  <SelectValue placeholder="Select a club" />
                </SelectTrigger>
                <SelectContent>
                  {clubs.map((club) => (
                    <SelectItem key={club} value={club}>
                      {club}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-4xl">
            {/* Shot Statistic Cards */}
            <Card className="w-full">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground text-xs uppercase tracking-wider">
                  Carry Distance
                </p>
                <p className="text-5xl font-semibold mt-2">
                  {data?.carryDistance.toFixed(1)}
                </p>
                <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                  yards
                </p>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground text-xs uppercase tracking-wider">
                  Club Head Speed
                </p>
                <p className="text-5xl font-semibold mt-2">
                  {data?.clubHeadSpeed.toFixed(1)}
                </p>
                <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                  mph
                </p>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground text-xs uppercase tracking-wider">
                  Ball Speed
                </p>
                <p className="text-5xl font-semibold mt-2">
                  {data?.ballSpeed.toFixed(1)}
                </p>
                <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                  mph
                </p>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground text-xs uppercase tracking-wider">
                  Smash Factor
                </p>
                <p className="text-5xl font-semibold mt-2">
                  {data?.smashFactor.toFixed(2)}
                </p>
                <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                  ratio
                </p>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground text-xs uppercase tracking-wider">
                  Launch Angle
                </p>
                <p className="text-5xl font-semibold mt-2">
                  {data?.launchAngle.toFixed(1)}
                </p>
                <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                  degrees
                </p>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardContent className="p-4 text-center">
                <p className="text-muted-foreground text-xs uppercase tracking-wider">
                  Apex Height
                </p>
                <p className="text-5xl font-semibold mt-2">
                  {data?.apexHeight.toFixed(1)}
                </p>
                <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                  feet
                </p>
              </CardContent>
            </Card>
          </div>
          </div>
        </>
      )}
    </main>
  )
}