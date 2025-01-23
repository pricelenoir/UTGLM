import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, FlatList, Dimensions } from 'react-native';
// import RNPickerSelect from 'react-native-picker-select';
// import { useBLE } from '../services/useBLE';

const clubs = [
  { label: 'Driver',   value: '1d' },
  { label: '3-Wood',   value: '3w' },
  { label: '3-Hybrid', value: '3h' },
  { label: '3-Iron',   value: '3i' },
  { label: '4-Iron',   value: '4i' },
  { label: '5-Iron',   value: '5i' },
  { label: '6-Iron',   value: '6i' },
  { label: '7-Iron',   value: '7i' },
  { label: '8-Iron',   value: '8i' },
  { label: '9-Iron',   value: '9i' },
  { label: 'P-Wedge',  value: 'pw' },
  { label: 'G-Wedge',  value: 'gw' },
  { label: 'S-Wedge',  value: 'sw' },
  { label: 'L-Wedge',  value: 'lw' },
];

const formatData = (data, numColumns) => {
  const numberOfFullRows = Math.floor(data.length / numColumns);

  let numberOfElementsLastRow = data.length - (numberOfFullRows * numColumns);
  while (numberOfElementsLastRow !== numColumns && numberOfElementsLastRow !== 0) {
    data.push({ key: `blank-${numberOfElementsLastRow}`, empty: true });
    numberOfElementsLastRow++;
  }

  return data;
};

export default function App() {
  const [orientation, setOrientation] = useState("PORTRAIT"); // Default orientation

  useEffect(() => {
    const updateOrientation = () => {
      const { width, height } = Dimensions.get("window");
      setOrientation(width > height ? "LANDSCAPE" : "PORTRAIT");
    };

    Dimensions.addEventListener("change", updateOrientation);

    // Initial check
    updateOrientation();

    return () => Dimensions.removeEventListener("change", updateOrientation);
  }, []);

  const numColumns = orientation === "PORTRAIT" ? 2 : 3; // Adjust columns based on orientation

  const renderItem = ({ item }) => {
    if (item.empty === true) {
      return <View style={[styles.item, styles.itemInvisible]} />;
    }
    return (
      <View style={styles.item}>
        <Text style={styles.nameText}>{item.statName}</Text>
        <Text style={styles.valueText}>{item.statValue}</Text>
        <Text style={styles.unitText}>{item.statUnit}</Text>
      </View>
    );
  };

  // Replace with const shotStats = getShotStats or something from useBLE
  const shotStats = [
    { statName: 'CARRY',        statValue: '220',  statUnit: "YARDS" },
    { statName: 'TOTAL',        statValue: '234',  statUnit: "YARDS" },
    { statName: 'BALL SPEED',   statValue: '120',  statUnit: "MPH" }, 
    { statName: 'CLUB SPEED',   statValue: '100',  statUnit: "MPH" },
    { statName: 'EFFICIENCY',   statValue: '1.2',  statUnit: "SMASH" },
    { statName: 'LAUNCH ANGLE', statValue: '9.4',  statUnit: "DEG" },
  ];

  return (
    <View style={styles.mainContainer}>
      {/* FlatList */}
      <FlatList
        data={formatData(shotStats, numColumns)}
        style={styles.listContainer}
        renderItem={renderItem}
        numColumns={numColumns}
        key={numColumns}
      />

      {/* Footer */}
      <View style={[ styles.footer, orientation === "PORTRAIT" ? styles.footerPortrait : styles.footerLandscape, ]}>
        <Text style={styles.footerText}>
          This footer adjusts to the device orientation!
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
  },
  listContainer: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center', // Center vertically
  },
  item: {
    backgroundColor: '#FFFFFF',
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    margin: 1,
    height: Dimensions.get('window').width / 2, // Approximate square items
  },
  itemInvisible: {
    backgroundColor: 'transparent',
  },
  nameText: {
    color: '#000',
    fontSize: 16,
    fontWeight: 'bold',
    fontFamily: 'Futura LT Condensed Extra Bold Oblique',
  },
  valueText: {
    color: '#000',
    fontSize: 64,
    fontWeight: 'bold',
  },
  unitText: {
    color: '#000',
    fontSize: 14,
    fontWeight: 'bold',
  },
  footer: {
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
  },
  footerPortrait: {
    height: 150,
    width: '100%',
    position: 'absolute',
    bottom: 0,
    left: 0,
  },
  footerLandscape: {
    width: 150,
    height: '100%',
    position: 'absolute',
    right: 0,
    top: 0,
  },
  footerText: {
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',
    transform: [{ rotate: '0deg' }], // Ensures text remains upright
  },
});
