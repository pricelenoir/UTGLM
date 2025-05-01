'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Spinner } from '@/components/ui/spinner'
import { rubik } from './fonts'

export default function Home() {
  const [device, setDevice] = useState(null)
  const [data, setData] = useState(null)
  const [selectedClub, setSelectedClub] = useState('7 Iron')
  const [socket, setSocket] = useState(null)

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
    'Gap Wedge',
    'Sand Wedge',
    'Lob Wedge',
  ]

  useEffect(() => {
    let ws;
    let retryTimeout;
  
    const connectWebSocket = () => {
      ws = new WebSocket('ws://10.0.0.70:8765'); // Raspberry Pi’s IP
  
      ws.onopen = () => {
        console.log('WebSocket connected');
        setSocket(ws);
        setSelectedClub('7 Iron'); // Set default club on connection
        setData(null); // Reset data on connection
      };
  
      ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        if (message.type === 'shot') {
          setData(message.data)
          console.log('Received shot data:', message.data)
        } else if (message.type === 'device') {
          setDevice(message.name)
          console.log('Device connected:', message.device)
        }
      };
  
      ws.onerror = () => {
        console.log('WebSocket failed to connect. Retrying in 3s...');
      };
  
      ws.onclose = () => {
        setSocket(null);
        retryTimeout = setTimeout(connectWebSocket, 3000); // Retry after 3 seconds
      };
    };
  
    connectWebSocket();
  
    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
      if (retryTimeout) clearTimeout(retryTimeout);
    };    
  }, []);
  

  const handleClubChange = (club) => {
    setSelectedClub(club)

    const compactClub = club
      .replace(' ', '')
      .toLowerCase()
      .replace('3wood', '3w')
      .replace('iron', 'i')
      .replace('wedge', 'w')
      .replace('pitchingw', 'pw')
      .replace('gapw', 'gw')
      .replace('sandw', 'sw')
      .replace('lobw', 'lw')

    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ type: 'club_change', club: compactClub }))
      console.log('Sent club change:', compactClub)
    }
  }

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
        <div className="mt-2 text-sm text-gray-500">
          {socket ? `Connected: ${device}` : 'Device not connected.'}
        </div>
      </header>

      {!socket ? (
        <div className="flex flex-col items-center gap-6 mt-20 w-full max-w-md">
          <Spinner />
          <p className="text-md text-center font-medium">
            Waiting for WebSocket connection...
          </p>
          <p className="text-sm text-center text-gray-600">
            Please make sure your device is powered on and connected to the same network.
          </p>
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
                <Select value={selectedClub} onValueChange={handleClubChange}>
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

            {/* Shot Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-4xl">
              {[
                { label: 'Carry Distance', value: data?.carry_distance?.toFixed(1), unit: 'yards' },
                { label: 'Club Head Speed', value: data?.club_head_speed?.toFixed(1), unit: 'mph' },
                { label: 'Ball Speed', value: data?.ball_speed?.toFixed(1), unit: 'mph' },
                { label: 'Smash Factor', value: data?.smash_factor?.toFixed(2), unit: 'ratio' },
                { label: 'Launch Angle', value: data?.launch_angle?.toFixed(1), unit: 'degrees' },
                { label: 'Apex Height', value: data?.apex_height?.toFixed(1), unit: 'feet' },
              ].map((stat, index) => (
                <Card key={index} className="w-full">
                  <CardContent className="p-4 text-center">
                    <p className="text-muted-foreground text-xs uppercase tracking-wider">
                      {stat.label}
                    </p>
                    <p className="text-5xl font-semibold mt-2">
                      {stat.value ?? '--'}
                    </p>
                    <p className="text-muted-foreground text-xs uppercase tracking-wider mt-1">
                      {stat.unit}
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </>
      )}
    </main>
  )
}