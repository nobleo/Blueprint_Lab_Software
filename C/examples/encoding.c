
#include <stdio.h>
#include "../bplprotocol.h"

void main(void){

    // // create a buffer of bytes for your packet to be filled in with.
    // uint8_t packet[MAX_PACKET_LENGTH];
    // memset(packet, 0, MAX_PACKET_LENGTH);   // Set data to zeros

    // uint8_t deviceID = 0x01;
    // uint8_t packetID = MODE;
    // uint8_t data[1] = {0};

    // printf("Encoding Packet\n");

    // int packetLength = encodePacketBare(packet, deviceID, packetID, data, 1);

    // printf("Encoded packet: \n");

    // for (int i = 0; i<=packetLength; i++){
    //     printf(" %d", packet[i]);
    // }


    // printf("\n Encode Floats \n");
    // uint8_t floatBytes[12];
    // encodeFloat(floatBytes, 12.34);
    // // printf(" %d\n", intBuffer[1]);
    // for (int i = 0; i<4; i++){
    //     printf(" %d", floatBytes[i]);
    // }

    // printf("\n Encode Floats List \n");

    // float floatsList[3] = {1.1, 2.2, 3.0};
    // encodeFloats(floatBytes, floatsList, 3);

    // for (int i = 0; i<(3*4); i++){
    //     printf(" %d", floatBytes[i]);
    // }


    uint8_t buff[64];
    memset(buff, 0, 64);
    uint8_t data[4];
    encodeFloat(data, 3.123);
    struct Packet packet2;
    packet2.deviceID = 0x01;
    packet2.packetID = 0x02;
    packet2.data = data;
    packet2.data_length = 4;

    encodePacket(buff, &packet2);

    for (int i = 0; i<10; i++){
        printf(" %d", buff[i]);
    }
}