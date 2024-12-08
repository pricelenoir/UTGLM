import serial
from src.parser_scripts.parser_mmw_demo import parser_one_mmw_demo_output_packet  # Import the parser function from mmWave SDK

def main():
    # Serial port configuration
    SERIAL_PORT = '/dev/ttyUSB1'
    BAUD_RATE = 921600

    # Open the serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    if ser.is_open:
        print(f"Connected to {SERIAL_PORT}")
    else:
        print("Error: Serial port is not open.")
        return

    data_buffer = bytearray()
    num_frames_parsed = 0

    while True:
        try:
            # Read available data from the serial port
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                data_buffer.extend(data)

                # Attempt to parse the buffer
                while True:
                    parser_result, \
                    header_start_index, \
                    total_packet_num_bytes, \
                    num_det_obj, \
                    num_tlv, \
                    sub_frame_number, \
                    detected_x_array, \
                    detected_y_array, \
                    detected_z_array, \
                    detected_v_array, \
                    detected_range_array, \
                    detected_azimuth_array, \
                    detected_elevation_array, \
                    detected_snr_array, \
                    detected_noise_array = parser_one_mmw_demo_output_packet(data_buffer, len(data_buffer))

                    # Check parser result
                    if parser_result == 0:
                        # Successfully parsed a frame
                        num_frames_parsed += 1
                        print(f"Frame {num_frames_parsed} parsed:")
                        print(f"Number of detected objects: {num_det_obj}")
                        for i in range(num_det_obj):
                            print(f"Object {i}: X={detected_x_array[i]}, Y={detected_y_array[i]}, Z={detected_z_array[i]}, "
                                  f"Velocity={detected_v_array[i]}, SNR={detected_snr_array[i]}, Noise={detected_noise_array[i]}")

                        # Remove parsed bytes from the buffer
                        del data_buffer[:header_start_index + total_packet_num_bytes]
                    else:
                        # Parsing incomplete or error; wait for more data
                        break
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
