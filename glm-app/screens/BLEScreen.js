import React, { useState } from "react";
import { StyleSheet, Text, View, Button } from "react-native";
import { useBLE } from "../services/useBLE";
import DeviceModal from "../components/DeviceConnectionModal";

export default function BLEScreen() {
  const { scanForPeripherals, allDevices, connectToDevice } = useBLE();
  const [isModalVisible, setIsModalVisible] = useState(false);

  const handleConnect = () => {
    // Trigger device scan
    scanForPeripherals();
    setIsModalVisible(true); // Show the modal when the scan starts
  };

  const closeModal = () => {
    setIsModalVisible(false);
  };

  return (
    <View style={styles.container}>
      <Text>Connect via Bluetooth</Text>
      <Button title="Connect" onPress={handleConnect} />
      
      {/* Device Modal */}
      <DeviceModal
        devices={allDevices}
        visible={isModalVisible}
        connectToPeripheral={connectToDevice}
        closeModal={closeModal}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
});
