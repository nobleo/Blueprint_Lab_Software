import re
import socket
import struct
from typing import Union, Tuple, List, Optional
from cobs import cobs
import serial
import time
from crcmod import crcmod
import logging

from BPL_serial_protocol.RS1_SDK_v4.RS1_SDK.Examples.RS1_hardware import PacketID

logging.basicConfig()
logger = logging.getLogger(__name__)

CRC8_FUNC = crcmod.mkCrcFun(0x14D, initCrc=0xFF, xorOut=0xFF)

SERIAL_PORT = "COM12"  # Serial port in your computer.
BAUDRATE = 115200

UDP_IP_ADDRESS = "192.168.1.221"
UDP_PORT = 6789

DEVICE_ID = 0x04

TIMEOUT = 1.0  # seconds


def packet_splitter(buff: bytes) -> Tuple[List[bytes], Optional[bytes]]:
    """
    Split packet using BPL serial protocol
    """
    incomplete_packet = None
    packets = re.split(b'\x00', buff)

    if buff[-1] != b'0x00':
        incomplete_packet = packets.pop()

    packets = [x for x in packets if x != b'']
    return packets, incomplete_packet


def parse_packet(packet_in: Union[bytes, bytearray]) -> Tuple[int, int, bytes]:
    """
    Parse the packet returning a tuple of [int, int, bytes].
     If unable to parse the packet, then return 0,0,b''.
    """

    packet_in = bytearray(packet_in)

    if packet_in and len(packet_in) > 3:
        try:
            decoded_packet: bytes = cobs.decode(packet_in)
        except cobs.DecodeError as e:
            logger.warning(f"parse_packet(): Cobs Decoding Error, {e}")
            return 0, 0, b''

        if decoded_packet[-2] != len(decoded_packet):
            logger.warning(f"parse_packet(): Incorrect length: length is {len(decoded_packet)} "
                           f"in {[hex(x) for x in list(decoded_packet)]}")
            return 0, 0, b''
        else:
            if CRC8_FUNC(decoded_packet[:-1]) == decoded_packet[-1]:
                rx_data = decoded_packet[:-4]

                device_id = decoded_packet[-3]
                packet_id = decoded_packet[-4]
                rx_data = rx_data
                return device_id, packet_id, rx_data
            else:
                logger.warning(f"parse_packet(): CRC error in {[hex(x) for x in list(decoded_packet)]} ")
                return 0, 0, b''

    logger.warning(f"packet_length is too short")
    return 0, 0, b''


def encode_packet(device_id: int, packet_id: int, data: Union[bytes, bytearray]):
    tx_packet = bytes(data)
    tx_packet += bytes([packet_id, device_id, len(tx_packet)+4])
    tx_packet += bytes([CRC8_FUNC(tx_packet)])
    packet: bytes = cobs.encode(tx_packet) + b'\x00'
    return packet


def decode_floats(data: Union[bytes, bytearray]) -> List[float]:
    list_data = list(struct.unpack(str(int(len(data)/4)) + "f", data))
    return list_data


def request_serial(packet_id: int):
    serial_device = serial.Serial(SERIAL_PORT,
                                  baudrate=BAUDRATE,
                                  stopbits=serial.STOPBITS_ONE,
                                  parity=serial.PARITY_NONE,
                                  bytesize=serial.EIGHTBITS)
    serial_device.timeout = 0.00
    data = encode_packet(DEVICE_ID, PacketID.REQUEST_PACKET, bytes([packet_id]))
    start_time = time.perf_counter()
    serial_device.write(data)

    read_data = b''
    packets = []
    while not packets:
        read_data += serial_device.read(128)
        if read_data:
            packets, _ = packet_splitter(read_data)
            if packets:
                break
        if time.perf_counter() - start_time > TIMEOUT:
            print(f"Did not receive response")
            return

    for packet in packets:
        read_device_id, read_packet_id, data_bytes = parse_packet(packet)
        if read_device_id == DEVICE_ID and read_packet_id == packet_id:
            value = decode_floats(data_bytes)[0]
            print(f"Received position packet (Value: {value}) in {(time.perf_counter() - start_time)*1000:.2f} ms")
            break


def request_udp(device_ids: List[int], packet_id: int, request_period):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = encode_packet(0xFF, PacketID.REQUEST_PACKET, bytes([packet_id]))
    udp.setblocking(False)





    response_times: list = [None] * len(device_ids)
    average_response_times = [0.0] * len(device_ids)
    received_responses = [0] * len(device_ids)
    missed_packets = [-1] * len(device_ids)

    while True:
        start_time = time.perf_counter()
        for idx, d in enumerate(device_ids):
            if response_times[idx] is None:
                missed_packets[idx] += 1
            else:
                average_response_times[idx] \
                    = (average_response_times[idx] * received_responses[idx] + response_times[idx] )\
                      / (received_responses[idx] +1)
                received_responses[idx] += 1

        print_strings = [f"{x * 1000:.1f}" for x in average_response_times]
        dev_id_string = ""
        resp_time_string = ""
        avg_response_time_string = ""
        missing_string = ""
        for idx, d in enumerate(device_ids):
            dev_id_string += hex(d) + " \t"
            a = response_times[idx]
            if a is not None:
                resp_time_string += f"{a * 1000:.1f}" + "\t"
            else:
                resp_time_string += "--  \t"
            avg_response_time_string += print_strings[idx] + " \t"
            missing_string += f"{missed_packets[idx]}" + "   \t"

        strings = "Device_ID    \t " + dev_id_string + " \n" + "Response time  \t" + resp_time_string + "\n" + "Response_avg ms\t" + avg_response_time_string + " \n" + "Missing     \t" + missing_string + " \n"
        print(strings)



        udp.sendto(data, (UDP_IP_ADDRESS, UDP_PORT))

        incomplete_packets = b''
        while time.perf_counter() - start_time < request_period:
            try:
                read_data = udp.recv(128)
            except:
                read_data = b''
            if read_data:
                packets, incomplete_packets = packet_splitter(incomplete_packets+read_data)
                if packets:
                    for packet in packets:
                        read_device_id, read_packet_id, data_bytes = parse_packet(packet)
                        if read_device_id in device_ids:
                            idx = device_ids.index(read_device_id)
                            response_times[idx] = time.perf_counter() - start_time






if __name__ == '__main__':

    device_ids = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7]

    request_period = 0.5  # seconds

    packet_id = PacketID.POSITION  # packet to request

    # request_serial(PacketID.Position)
    request_udp(device_ids, packet_id, request_period)





