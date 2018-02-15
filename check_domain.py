# -*- coding: utf-8 -*-
"""
Программа осуществляет поиск доменов, схожих с заданным, используя несколько стратегий.
Проверка домена осуществляется путем попытки получить ip-адрес функцией socket.gethostbyname()
"""
import threading
import socket as soc
import re
import string
import itertools


class WorkThread(threading.Thread):
    def __init__(self, addrs, addrs_lock):
        super(WorkThread, self).__init__()
        self.addrs = addrs
        self.addrs_lock = addrs_lock

    def run(self):
        """
        Основной метод класса
        """
        while 1:
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
        """
        проверка домена 
        :param next_addr: следущий адрес из списка 
        """
        try:
            soc.gethostbyname(next_addr)
            print(self.name, next_addr, ' - is available')
        except:
            # print(self.name, next_addr, ' - isnt available')
            pass


class Strategies:
    def __init__(self, domain):
        self.domain = domain

    def adding(self, alphabet):
        """
        Добавляет в список доменов для проверки домены, которые получаются при добавлении одного символа в конец строки.
        Можно выбрать, какие символы добавлять
        :param alphabet: выбор добавляемых символом. дефолт - все буквы английского алфавита в лоукэйс
        :return: список доменов для проверки
        """
        domain_add_list = []
        for letter in alphabet:
            domain_add_list.append(self.domain + letter)
        return domain_add_list

    def subdomain(self):
        """
        Добавляет в список доменов для проверки поддомены, получающиеся при подставлении точки в изначальный домен.
        :return: список доменов для проверки
        """
        domain_sub_list = []
        i = 0
        while i < len(self.domain):
            domain_sub_list.append(self.domain[0:i] + '.' + self.domain[i:])
            i += 1
        return domain_sub_list

    def deleting(self):
        """
        Добавляет в список доменов для проверки домены,
        которые получаются путем удаления одного символа из изначального домена.
        :return: список доменов для проверки
        """
        domain_del_list = []
        i = 0
        while i < len(self.domain):
            domain_del_list.append(self.domain[:i] + self.domain[i+1:])
            i += 1
        return domain_del_list

    def homoglyphs(self, h_list):
        """
        Добавляет в список доменов для проверки домены-омоглифы.
        :param h_list: список омоглифов - похожих букв. В интернете есть библиотека - confusable-homoglyphs,
        но она отражает только разницу в языке: (i - l,1) не будет распознаваться в этой библиотеке.
        Поэтому вводим вручную.
        :return: список доменов для проверки
        """
        dom_h_list = [h_list[letter] for letter in self.domain]
        return list(''.join(u) for u in [element for element in itertools.product(*dom_h_list)])


if __name__ == "__main__":
    domain = input('Enter domain: ')
    choose = input('Choose strategy: \n 1.Adding \n 2.Subdomain \n 3.Deleting \n 4.Homoglyphs \n ')
    zone_list = ['com', 'ru', 'net', 'org', 'info', 'cn', 'es', 'top', 'au', 'pl', 'it', 'uk', 'tk', 'ml', 'ga', 'cf',
                 'us', 'xyz', 'top', 'site', 'win', 'bid']
    homoglyph_list = {'a': ['a', 'o'], 'b': ['b', 'ь'], 'c': ['c', 'с', 'e'], 'd': ['d', 'b', 'ь'],
                      'e': ['e', 'е', 'ё', 'o', 'c'], 'f': ['f', 't'], 'g': ['g', 'j'], 'h': ['h', 'b'],
                      'i': ['i', '1', 'l'], 'j': ['j', 'g'], 'k': ['k', 'к'], 'l': ['l', 'i', '1'], 'm': ['m', 'n'],
                      'n': ['n', 'm'], 'o': ['o', '0', 'о'], 'p': ['p', 'р'], 'q': ['q', 'p', 'р'], 'r': ['r'],
                      's': ['s', 'c'], 't': ['t', 'f'], 'u': ['u', 'и', 'v'], 'v': ['v', 'u'], 'w': ['w', 'vv'],
                      'x': ['x', 'х'], 'y': ['y', 'g', 'j'], 'z': ['z', 's'], '-': ['-', '--'], '_': ['_', '__']}
    domain_list = []
    if choose == '1':
        s = Strategies(domain)
        domain_list = s.adding(string.ascii_lowercase)
    elif choose == '2':
        s = Strategies(domain)
        domain_list = s.subdomain()
    elif choose == '3':
        s = Strategies(domain)
        domain_list = s.deleting()
    elif choose == '4':
        s = Strategies(domain)
        domain_list = s.homoglyphs(homoglyph_list)
    address_list = [dom + '.' + zone for zone in zone_list for dom in domain_list]
    # print(address_list)
    print('Total - ', len(address_list))
    addrs_lock = threading.Lock()
    for x in range(0, 3):
        newthread = WorkThread(address_list, addrs_lock)
        newthread.start()
