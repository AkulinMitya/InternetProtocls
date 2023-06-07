import socket
import struct
import time

from sntp.SntpPacket import SntpPacket


def create_ntp_request() -> SntpPacket:
    response_packet = SntpPacket()
    response_packet.mode = 3  # Устанавливаем режим клиента

    return response_packet.pack()


if __name__ == '__main__':
    # IP-адрес и порт сервера точного времени
    ntp_server = '127.0.0.1'
    ntp_port = 123

    # Создаем сокет UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    # Отправляем пустой пакет запроса времени на сервер
    ntp_request_packet = create_ntp_request()
    sock.sendto(ntp_request_packet, (ntp_server, ntp_port))
    try:
        # Получаем ответ от сервера
        data, address = sock.recvfrom(1024)

        # Разбираем пакет ответа
        ntp_time = SntpPacket.unpack(data)

        # Выводим полученное время
        print(ntp_time)
    except TimeoutError:
        print("Время ожидания ответа истекло. Возможно формат отправленного пакета некорректный.")
