# -*- coding: utf-8 -*-
"""
Программа сканирует определенные порты в диапазоне заданных ip-адресов.
В начале создается массив всех адресов (адрес * диапазон).
Затем три потока обрабатывают этот массив * порты.
Для открытых портов 80 и 433 программа получает request.headres(), содержащий информацию о сервере.
"""
import threading
import socket as soc
import re
import string


class WorkThread(threading.Thread):
    def __init__(self, addrs, addrs_lock):
        super(WorkThread, self).__init__()
        self.addrs = addrs
        self.addrs_lock = addrs_lock

    def run(self):
        """
        Основной метод класса
        """
        while(1):
            next_adrr = self.take_next_addr()
            if next_adrr is None:
                break
            self.check_domain(next_adrr)

    def take_next_addr(self):
        """
        Возвращает следующий адрес из списка заданных адресов
        """
        self.addrs_lock.acquire(1)
        if len(self.addrs) < 1:
            next_adrr = None
        else:
            next_adrr = self.addrs[0]
            del self.addrs[0]
        self.addrs_lock.release()
        return next_adrr

    def check_domain(self, next_addr):
        try:
            sock = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
            sock.settimeout(0.01)
            sock.gethostbyname(next_addr)
            print(self.name, next_addr, ' - is available')
            sock.close()
        except:
            pass


class Strategies():
    def __init__(self, domain, zone_list):
        self.domain = domain
        self.zone_list = zone_list

    def adding(self, alfabet):
        domain_add_list = []
        for letter in alfabet:
            domain_add_list.append(self.domain + letter)
        return domain_add_list

    def


if __name__ == "__main__":
    address = input('Enter address (0.0.0.): ')
    diap = int(input('Enter diap (0): '))
    ports = re.split(' ', input('Enter ports: (0 0 0))'))
    address_list = []
    for a in range(diap):
        address_list.append(address + str(a))
    # print("list: \n", address_list)
    addrs_lock = threading.Lock()
    for x in range(0, 3):
        newthread = WorkThread(address_list, ports, addrs_lock)
        newthread.start()
