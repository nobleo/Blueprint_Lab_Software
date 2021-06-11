
from bplprotocol import BPLProtocol, PacketID, PacketReader


# install pyserial with pip install pyserial

import time

import serial


if __name__ == '__main__':

    device_ids = [0x01, 0x02, 0x03, 0x04, 0x05]

    frequency = 20

    packet_reader = PacketReader

    serial_port_name = "COM0"

    serial_port = serial.Serial("COM0", baud=115200, parity=serial.PARITY_NONE, stopbits=0, timeout=0)

    request_packet = b''

    # Request packets can be concatenated
    for device_id in device_ids:
        request_packet += BPLProtocol.encode_packet(device_id, PacketID.REQUEST, bytes(PacketID.POSITION))

    while True:

        # Send request packet
        serial_port.write(request_packet)

        position_responses = [None] * len(device_ids)
        # Read request packets

        start_time = time.time()
        while time.time() < start_time + 1/frequency:
            time.sleep(0.0001)
            try:
                serial_port.read()
            except
