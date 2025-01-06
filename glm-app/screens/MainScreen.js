import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import { useBluetooth } from '../services/BluetoothContext';

export default function MainScreen() {
  const { setIsConnected } = useBluetooth();

  const handleDisconnect = () => {
    // Simulate Bluetooth disconnection logic
    setIsConnected(false);
  };

  return (
    <View style={styles.container}>
      <Text>Main Screen</Text>
      <Button title="Disconnect" onPress={handleDisconnect} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
