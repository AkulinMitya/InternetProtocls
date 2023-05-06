import pickle
import time

import dnslib


class DNSCache:
    def __init__(self, filename, insertion_time_filename):
        self.cache = {}
        self.filename = filename
        self.insertion_time = {}
        self.insertion_time_filename = insertion_time_filename

    def load_cache(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    key = (parts[0], int(parts[1]))
                    value = bytes.fromhex(parts[2])
                    self.cache[key] = value
        except FileNotFoundError:
            pass

    def save_cache(self):
        with open(self.filename, "w") as f:
            for key, value in self.cache.items():
                f.write(f"{key[0]}\t{key[1]}\t{value.hex()}\n")

    def load_insertion_time(self):
        try:
            with open(self.insertion_time_filename, "rb") as f:
                self.insertion_time = pickle.load(f)
        except (FileNotFoundError, EOFError):
            # Обработка исключения EOFError, если файл пустой
            self.insertion_time = {}

    def save_insertion_time(self):
        with open(self.insertion_time_filename, "wb") as f:
            pickle.dump(self.insertion_time, f)

    def check_cache(self, domain, rtype):
        key = (domain, rtype)
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def update_cache(self, qname, qtype, response_data):
        key = (qname, qtype)
        self.cache[key] = response_data

    def purge_expired_records(self):
        current_time = time.time()
        keys_to_delete = []

        for key in self.insertion_time:
            packet_data = self.cache[key]
            packet = dnslib.DNSRecord.parse(packet_data)
            new_packet = dnslib.DNSRecord(header=packet.header)
            new_packet.add_question(packet.questions[0])

            for rr in packet.rr:
                ttl = rr.ttl
                time_diff = current_time - self.insertion_time[key]
                print(f"TTL: {ttl}, DIFF: {time_diff}, QUERY: {rr}")

                if time_diff < ttl:
                    new_packet.add_answer(rr)

            if len(new_packet.rr) > 0:
                self.cache[key] = new_packet.pack()
            else:
                print(key)
                keys_to_delete.append(key)

        for key in keys_to_delete:
            print(f"Время жизни ресурсных записей для {key} истекло. Запрос удален из кэша")
            del self.cache[key]
            del self.insertion_time[key]
