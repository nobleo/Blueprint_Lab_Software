import re
import struct
from typing import Union, Tuple, List, Optional
from cobs import cobs
from crcmod import crcmod
import logging

logger = logging.getLogger(__name__)


class PacketID:
    """
    Mock class holding relevant packet Ids for this script.
    Look in The Serial Protocol Document for a comprehensive list of packet ids.
    """
    MODE = 0x01
    VELOCITY = 0x02
    POSITION = 0x03
    CURRENT = 0x05
    RELATIVE_POSITION = 0x0E
    INDEXED_POSITION = 0x0D
    REQUEST = 0x60
    SERIAL_NUMBER = 0x61
    MODEL_NUMBER = 0x62
    TEMPERATURE = 0x66
    SOFTWARE_VERSION = 0x6C
    KM_END_POS = 0xA1
    KM_END_VEL = 0xA2
    KM_BOX_OBSTACLE_02 = 0xA5
    KM_BOX_OBSTACLE_03 = 0xA6
    KM_BOX_OBSTACLE_04 = 0xA7
    KM_BOX_OBSTACLE_05 = 0xA8
    KM_CYLINDER_OBSTACLE_02 = 0xAB
    KM_CYLINDER_OBSTACLE_03 = 0xAC
    KM_CYLINDER_OBSTACLE_04 = 0xAD
    KM_CYLINDER_OBSTACLE_05 = 0xAE
    KM_END_VEL_LOCAL = 0xCB
    VOLTAGE = 0x90
    SAVE = 0x50
    HEARTBEAT_FREQUENCY = 0x92
    HEARTBEAT_SET = 0x91
    POSITION_LIMITS = 0x10
    VELOCITY_LIMITS = 0x11
    CURRENT_LIMITS = 0x12
    BOOTLOADER = 0xFF


class BPLProtocol:
    """ Helper class used to encode and decode BPL packets."""
    CRC8_FUNC = crcmod.mkCrcFun(0x14D, initCrc=0xFF, xorOut=0xFF)

    @staticmethod
    def packet_splitter(buff: bytes) -> Tuple[List[bytes], Optional[bytes]]:
        """
        Split packets coming in along bpl protocol, Packets are split via 0x00.
        """
        incomplete_packet = None
        packets = re.split(b'\x00', buff)
        if buff[-1] != b'0x00':
            incomplete_packet = packets.pop()
        return packets, incomplete_packet

    @staticmethod
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
                if BPLProtocol.CRC8_FUNC(decoded_packet[:-1]) == decoded_packet[-1]:
                    rx_data = decoded_packet[:-4]

                    device_id = decoded_packet[-3]
                    packet_id = decoded_packet[-4]
                    rx_data = rx_data
                    return device_id, packet_id, rx_data
                else:
                    logger.warning(f"parse_packet(): CRC error in {[hex(x) for x in list(decoded_packet)]} ")
                    return 0, 0, b''
        return 0, 0, b''

    @staticmethod
    def encode_packet(device_id: int, packet_id: int, data: Union[bytes, bytearray]):
        """ Encode the packet using the bpl protocol."""
        tx_packet = bytes(data)
        tx_packet += bytes([packet_id, device_id, len(tx_packet)+4])
        tx_packet += bytes([BPLProtocol.CRC8_FUNC(tx_packet)])
        packet: bytes = cobs.encode(tx_packet) + b'\x00'
        return packet

    @staticmethod
    def decode_floats(data: Union[bytes, bytearray]) -> List[float]:
        """ Decode a received byte list, into a float list as specified by the bpl protocol"""
        list_data = list(struct.unpack(str(int(len(data)/4)) + "f", data))
        return list_data

    @staticmethod
    def encode_floats(float_list: List[float]) -> bytes:
        """ Decode a received byte list, into a float list as specified by the bpl protocol"""
        data = struct.pack('%sf' % len(float_list), *float_list)
        return data


class PacketReader:
    """
    Packet Reader
    Helper class to read bytes, account for the possibility of incomplete packets on arrival.

    Usage:

    packet_reader = PacketReader()


    data == .... receive data here as bytes ...

    packets = packet_reader.receive_bytes()
    """
    incomplete_packets = b''

    def receive_bytes(self, data: bytes) -> List[Tuple[int, int, bytes]]:
        # Receive data, and return a decoded packet
        packet_list = []
        encoded_packets, self.incomplete_packets = BPLProtocol.packet_splitter(self.incomplete_packets + data)
        if encoded_packets:
            for encoded_packet in encoded_packets:
                if not encoded_packet:
                    continue
                decoded_packet = BPLProtocol.parse_packet(encoded_packet)
                packet_list.append(decoded_packet)
        return packet_list
