import serial
import asyncio
import json
import time
import websockets

from src.parser_scripts.parser_mmw_demo import parser_one_mmw_demo_output_packet
from src.calculate_golf_shot import calculate_golf_shot

SERIAL_PORT = '/dev/ttyUSB1'
BAUD_RATE = 921600

connected_clients = set()
data_buffer = bytearray()

current_club = "7i"  # Default club
THRESHOLD_SPEED = 5  # Golf shot detection threshold (m/s)
SHOT_COOLDOWN_TIME = 2
LAST_SHOT_TIME = 0

async def radar_task(websocket):
    global current_club, data_buffer, LAST_SHOT_TIME
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    while True:
        await asyncio.sleep(0.01)  # Yield to the event loop

        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            data_buffer.extend(data)

            while True:
                parser_result, header_start_index, total_packet_num_bytes, num_det_obj, _, _, \
                detected_x_array, detected_y_array, detected_z_array, detected_v_array, \
                detected_range_array, detected_azimuth_array, detected_elevation_array, \
                detected_snr_array, detected_noise_array = parser_one_mmw_demo_output_packet(data_buffer, len(data_buffer))

                if parser_result == 0:
                    current_time = time.time()
                    for i in range(num_det_obj):
                        if detected_v_array[i] > THRESHOLD_SPEED and (current_time - LAST_SHOT_TIME > SHOT_COOLDOWN_TIME):
                            club_head_speed = detected_v_array[i]
                            print(f"Club Head Speed: {club_head_speed} m/s")
                            print(f"Club: {current_club}")
                            golf_shot = calculate_golf_shot(club_head_speed, current_club)

                            message = json.dumps({
                                "type": "shot",
                                "data": golf_shot
                            })
                            await broadcast(message)
                            LAST_SHOT_TIME = current_time  # Prevent duplicates

                    del data_buffer[:header_start_index + total_packet_num_bytes]
                else:
                    break

async def broadcast(message):
    print(f"Sending to clients: {message}")
    if connected_clients:
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def handler(websocket):
    connected_clients.clear()
    connected_clients.add(websocket)

    print(f"Client connected: {websocket.remote_address}")
    try:
        device_name = "Raspberry Pi 5"
        await websocket.send(json.dumps({
            "type": "device",
            "name": device_name
        }))
    
        consumer_task = asyncio.create_task(receive_messages(websocket))
        producer_task = asyncio.create_task(radar_task(websocket))
        await asyncio.gather(consumer_task, producer_task)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

async def receive_messages(websocket):
    global current_club
    async for message in websocket:
        try:
            data = json.loads(message)
            if data["type"] == "club_change":
                new_club = data["club"]
                current_club = new_club
                print(f"Club changed to {new_club}")
        except Exception as e:
            print(f"Error parsing message: {e}")

async def main():
    print("WebSocket server running on ws://0.0.0.0:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
