export async function connectToBLE() {
    try {
      const device = await navigator.bluetooth.requestDevice({
        filters: [{ namePrefix: 'Raspberry Pi' }],
        optionalServices: ['device_information'],
      })
  
      await device.gatt.connect()
      return device.name || 'Unknown Device'
    } catch (error) {
      if (error.name === 'NotFoundError') {
        // User cancelled the dialog — handle silently
        console.log('User cancelled device chooser')
      } else {
        console.error('BLE connection error:', error)
      }
      return null
    }
  }
  