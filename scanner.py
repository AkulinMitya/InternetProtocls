import struct
from socket import *
import sys
import threading


def scan_tcp_ports(ip, port_from, port_to):
    for port in range(port_from, port_to + 1):
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(0.5)
        code = s.connect_ex((ip, port))
        if code == 0:
            print(f"TCP порт {port} доступен")
        s.close()


def scan_udp_ports(ip, port_from, port_to):
    for port in range(port_from, port_to + 1):
        icmp_socket = socket(AF_INET, SOCK_DGRAM)
        icmp_socket.settimeout(1)
        try:
            icmp_socket.sendto(b'Data', (ip, port))
            try:
                icmp_data, _ = icmp_socket.recvfrom(1024)
            except timeout:
                print(f"UDP порт {port} открыт")
                pass
        except error:
            pass

        icmp_socket.close()


def main():
    target = sys.argv[1]
    port_from = int(sys.argv[2])
    port_to = int(sys.argv[3])
    ip = gethostbyname(target)
    print(f"Сканирую порты хоста: {ip}")

    num_threads = 16
    num_ports = port_to - port_from + 1
    if num_ports <= 16:
        num_threads = num_ports
    threads = []
    step = num_ports // num_threads

    for i in range(num_threads):
        start_port = port_from + i * step
        end_port = start_port + step - 1 if i != num_threads - 1 else port_to
        t_tcp = threading.Thread(target=scan_tcp_ports, args=(ip, start_port, end_port))
        t_udp = threading.Thread(target=scan_udp_ports, args=(ip, start_port, end_port))
        threads.append(t_tcp)
        threads.append(t_udp)
        t_tcp.start()
        t_udp.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
