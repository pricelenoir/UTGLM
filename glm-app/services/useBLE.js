import { useMemo, useState } from "react";
import { PermissionsAndroid, Platform } from "react-native";
import * as ExpoDevice from "expo-device";
import base64 from "react-native-base64";
import { BleError, BleManager, Characteristic, Device } from "react-native-ble-plx";

const GLM_SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214";
const SHOT_DATA_CHARACTERISTIC_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214";
const CLUB_SELECTION_CHARACTERISTIC_UUID = "19b10001-e8f2-537e-4f6c-d104768a1217";

const bleManager = new BleManager();

function useBLE() {
    const [allDevices, setAllDevices] = useState([]);
    const [connectedDevice, setConnectedDevice] = useState(null);    

  const requestAndroid31Permissions = async () => {
    const bluetoothScanPermission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
      {
        title: "Location Permission",
        message: "Bluetooth Low Energy requires Location",
        buttonPositive: "OK",
      }
    );
    const bluetoothConnectPermission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
      {
        title: "Location Permission",
        message: "Bluetooth Low Energy requires Location",
        buttonPositive: "OK",
      }
    );
    const fineLocationPermission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: "Location Permission",
        message: "Bluetooth Low Energy requires Location",
        buttonPositive: "OK",
      }
    );

    return (
      bluetoothScanPermission === "granted" &&
      bluetoothConnectPermission === "granted" &&
      fineLocationPermission === "granted"
    );
  };

  const requestPermissions = async () => {
    if (Platform.OS === "android") {
      if ((ExpoDevice.platformApiLevel ?? -1) < 31) {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            title: "Location Permission",
            message: "Bluetooth Low Energy requires Location",
            buttonPositive: "OK",
          }
        );
        return granted === PermissionsAndroid.RESULTS.GRANTED;
      } else {
        const isAndroid31PermissionsGranted =
          await requestAndroid31Permissions();

        return isAndroid31PermissionsGranted;
      }
    } else {
      return true;
    }
  };

  const connectToDevice = async (device) => {
    try {
      const deviceConnection = await bleManager.connectToDevice(device.id);
      setConnectedDevice(deviceConnection);
      await deviceConnection.discoverAllServicesAndCharacteristics();
      bleManager.stopDeviceScan();

      startStreamingData(deviceConnection);
    } catch (e) {
      console.log("FAILED TO CONNECT", e);
    }
  };

  const isDuplicteDevice = (devices, nextDevice) =>
    devices.findIndex((device) => nextDevice.id === device.id) > -1;

  const scanForPeripherals = () => bleManager.startDeviceScan(null, null, (error, device) => {
    if (error) {
      console.log(error);
    }

    if (device && (device.localName === "UTGLM" || device.name === "UTGLM")) {
      setAllDevices((prevState) => {
      if (!isDuplicteDevice(prevState, device)) {
        return [...prevState, device];
      }
      return prevState;
      });
    }
  });

  const onDataUpdate = (error, characteristic) => {
    if (error) {
      console.log(error);
      return;
    } else if (!characteristic?.value) {
      console.log("No Data was received");
      return;
    }

    const shotData = base64.decode(characteristic.value);

    // Handle the shot data logic here
    // Deconstruct the shotData string and set the state for each value so that it all updates at once.
    // Maybe add an overlay or animation when new data arrives to show the user that the data is updating.

    // setShotData(shotData);
  };

  const startStreamingData = async (device) => {
    if (device) {
      device.monitorCharacteristicForService(
        GLM_SERVICE_UUID,
        SHOT_DATA_CHARACTERISTIC_UUID,
        onDataUpdate
      );
    } else {
      console.log("No Device Connected");
    }
  };

  const setClubSelection = async (club) => {
    try {  
      const clubSelection = base64.encode(club);
  
      // Write the encoded club selection to the characteristic
      await connectedDevice.writeCharacteristicWithResponseForService(
        GLM_SERVICE_UUID,
        CLUB_SELECTION_CHARACTERISTIC_UUID,
        clubSelection
      );
  
      console.log(`Club changed to: ${club}`);
    } catch (error) {
      console.log("Failed to write club selection", error);
    }
  };

  return {
    connectToDevice,
    allDevices,
    connectedDevice,
    isConnected: connectedDevice !== null,
    requestPermissions,
    scanForPeripherals,
    startStreamingData,
    setClubSelection,
  };
}

export default useBLE;