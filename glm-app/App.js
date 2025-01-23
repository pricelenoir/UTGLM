import React from 'react';
// import { useBLE } from './services/useBLE';
// import BLEScreen from './screens/BLEScreen';
import MainScreen from './screens/MainScreen';

function AppNavigator() {
  // const { isConnected } = useBLE();
  const isConnected = true; // Temporarily hardcode to true
  return isConnected ? <MainScreen /> : <BLEScreen />;
}

export default function App() {
  return (
    <BluetoothProvider>
      <AppNavigator />
    </BluetoothProvider>
  );
}
