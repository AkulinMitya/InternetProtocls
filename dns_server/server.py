import socket
import struct
import time

import dnslib as dnslib
from _socket import gethostbyname

from DNSCache import DNSCache
from DNSMessage import DNSMessage


class DNSServer:
    def __init__(self, big_brother, port, cache_filename):
        self.big_brother = big_brother
        self.port = port
        self.cache = DNSCache(cache_filename, insertion_time_filename="rr_times.txt")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('', self.port))
            s.settimeout(2)
            data = " "
            while data:
                try:
                    data, address = s.recvfrom(1024)
                    print(f"Came from: {address}")
                    msg = DNSServer.parse_dns_packet(data)
                    raw_msg = dnslib.DNSRecord.parse(data)
                    print(msg)

                    # Check for expire records
                    self.cache.purge_expired_records()

                    # Check cache for existing record
                    msg_domain = msg.questions[0][0]
                    msg_type = msg.questions[0][1]
                    cache_result = self.cache.check_cache(msg_domain, msg_type)

                    if cache_result:
                        response = DNSServer.parse_dns_packet(cache_result)
                        print(f"Record found in cache:\n{response}")
                        response_record = dnslib.DNSRecord(header=raw_msg.header)
                        response_record.add_question(raw_msg.q)
                        response_record.rr = dnslib.DNSRecord.parse(cache_result).rr
                        s.sendto(response_record.pack(), address)
                        continue

                    # Send a query to big brother
                    print("Waiting for response from Big Brother")
                    raw_response_from_bb = raw_msg.send(self.big_brother, 53, timeout=5)
                    msg_from_bb = self.parse_dns_packet(raw_response_from_bb)
                    print(f"Received response:\n{msg_from_bb}")

                    # Save response to cache
                    self.cache.update_cache(msg_domain, msg_type, raw_response_from_bb)
                    self.cache.insertion_time[(msg_domain, msg_type)] = time.time()
                    # Send response to client
                    s.sendto(raw_response_from_bb, address)
                except socket.timeout:
                    continue

    @staticmethod
    def parse_dns_packet(packet: bytes) -> DNSMessage:
        parsed_packet = dnslib.DNSRecord.parse(packet)
        id = parsed_packet.header.id
        qr = parsed_packet.header.qr
        opcode = parsed_packet.header.opcode
        aa = parsed_packet.header.aa
        tc = parsed_packet.header.tc
        rd = parsed_packet.header.rd
        ra = parsed_packet.header.ra
        z = parsed_packet.header.z
        rcode = parsed_packet.header.rcode
        questions = [(q.get_qname().idna(), q.qtype) for q in parsed_packet.questions]
        answers = [(a.rname.idna(), a.rdata) for a in parsed_packet.rr]
        return DNSMessage(id, qr, opcode, aa, tc, rd, ra, z, rcode, questions, answers)


if __name__ == '__main__':
    server = DNSServer(big_brother='77.88.8.1', port=53, cache_filename="cache.txt")
    try:
        print("The server has started")
        server.cache.load_cache()
        server.cache.load_insertion_time()
        server.start()
    except KeyboardInterrupt:
        print("Внештатное выключение...")
        server.cache.save_cache()
        server.cache.save_insertion_time()
