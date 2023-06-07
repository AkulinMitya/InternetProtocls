import json
import socket
import math
import time

from sntp.SntpPacket import SntpPacket


def create_ntp_response(ntp_request: SntpPacket):
    ntp_response = ntp_request
    ntp_response.mode = 4  # режим сервера
    ntp_response.stratum = 1  # первичный сервер
    current_time = get_current_time()
    frac, whole = math.modf(current_time)
    whole = int(whole)
    frac = int(str(frac)[2:11])
    time_timestamp = (whole << 32) | frac
    ntp_response.reference_timestamp = time_timestamp
    ntp_response.receive_timestamp = time_timestamp
    ntp_response.transmit_timestamp = time_timestamp
    return ntp_response.pack()


# Функция для получения текущего времени с учетом смещения
def get_current_time():
    # время отсчитывается с полуночи 1 января 1900 года, а не с 1970, поэтому прибавляем 70 лет
    return time.time() + offset_seconds + 2208988800


if __name__ == '__main__':
    with open('sntp_config.json') as file:
        config = json.load(file)
        offset_seconds = config["seconds"]

    # Создаем сокет UDP
    sock = socket.socket(socket.AF_INET, socket .SOCK_DGRAM)
    sock.bind(('127.0.0.1', 123))  # Слушаем 123 порт
    print("Сервер запущен!")

    while True:
        data, address = sock.recvfrom(1024)
        print(f"Получен запрос от {address}")

        try:
            request = SntpPacket.unpack(data)
            ntp_packet = create_ntp_response(request)
            # Отправляем пакет с точным временем обратно клиенту
            sock.sendto(ntp_packet, address)
            print(f"Ответ {address} отправлен")
        except Exception:
            pass


