import time


class SntpPacket:
    def __init__(self):
        self.leap_id = 0
        self.version = 4
        self.mode = None
        self.stratum = 0
        self.poll = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0
        self.ref_id = b'\x00\x00\x00\x00'
        self.reference_timestamp = 0
        self.origin_timestamp = 0
        self.receive_timestamp = 0
        self.transmit_timestamp = 0

    def pack(self):
        byte_str = b''
        byte_str += ((self.leap_id << 6) | (self.version << 3) | self.mode).to_bytes(1, signed=False,
                                                                                     byteorder="little")
        byte_str += self.stratum.to_bytes(1, signed=False, byteorder="little")
        byte_str += self.poll.to_bytes(1, signed=True, byteorder="little")
        byte_str += self.precision.to_bytes(1, signed=True, byteorder="little")
        byte_str += self.root_delay.to_bytes(4, signed=True, byteorder="little")
        byte_str += self.root_dispersion.to_bytes(4, signed=False, byteorder="little")
        byte_str += self.ref_id
        byte_str += self.reference_timestamp.to_bytes(8, signed=False, byteorder="little")
        byte_str += self.origin_timestamp.to_bytes(8, signed=False, byteorder="little")
        byte_str += self.receive_timestamp.to_bytes(8, signed=False, byteorder="little")
        byte_str += self.transmit_timestamp.to_bytes(8, signed=False, byteorder="little")
        return byte_str

    @staticmethod
    def unpack(byte_string):
        packet = SntpPacket()
        packet.LI = (byte_string[0] & 0b11000000) >> 6
        packet.VN = (byte_string[0] & 0b111000) >> 3
        packet.mode = (byte_string[0] & 0b111)
        packet.stratum = int(byte_string[1])
        packet.poll = int.from_bytes(byte_string[2:3], "little", signed=True)
        packet.precision = int.from_bytes(byte_string[3:4], "little", signed=True)
        packet.root_delay = int.from_bytes(byte_string[4:8], "little", signed=True)
        packet.root_dispersion = int.from_bytes(byte_string[8:12], "little", signed=False)
        packet.reference_id = byte_string[12:16]
        packet.reference_timestamp = int.from_bytes(byte_string[16:24], "little", signed=False)
        packet.origin_timestamp = int.from_bytes(byte_string[24:32], "little", signed=False)
        packet.receive_timestamp = int.from_bytes(byte_string[32:40], "little", signed=False)
        packet.transmit_timestamp = int.from_bytes(byte_string[40:48], "little", signed=False)
        return packet

    @staticmethod
    def to_time_from_ntp(timestamp):
        # Получение времени в привычном формате, без долей секунд
        timestamp = timestamp.to_bytes(8, "little")
        sec = int.from_bytes(timestamp[4:8], "little")
        sec -= 2208988800
        return time.ctime(sec)

    def __str__(self):
        return f"SNTP Packet:\n" \
               f"  Leap ID: {self.leap_id}\n" \
               f"  Version: {self.version}\n" \
               f"  Mode: {self.mode}\n" \
               f"  Stratum: {self.stratum}\n" \
               f"  Poll: {self.poll}\n" \
               f"  Precision: {self.precision}\n" \
               f"  Root Delay: {self.root_delay}\n" \
               f"  Root Dispersion: {self.root_dispersion}\n" \
               f"  Reference ID: {self.ref_id}\n" \
               f"  Reference Timestamp: {self.reference_timestamp}\n" \
               f"  Origin Timestamp: {self.origin_timestamp}\n" \
               f"  Receive Timestamp: {self.receive_timestamp}\n" \
               f"  Transmit Timestamp: {self.transmit_timestamp}\n" \
               f"  Normal form Transmit Timestamp: {SntpPacket.to_time_from_ntp(self.transmit_timestamp)}"


if __name__ == '__main__':
    print(SntpPacket.to_time_from_ntp(16728691129149554089))
