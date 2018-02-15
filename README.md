# Поиск фишинговых доменов

## О программе
Программа представляет собой средство для посика фишинговых доменов.

По заданному ключевому слову(домену), строится список доменов, которые могут быть потенциально фишинговыми.

При завершении работы программы выводится список тех доменов, которые являются зарегестрированными в Интернете.

В программе также реализована многопоточность с помощью модуля threading и метода Lock.

## Как работает
В основе работы программы лежат 4 стратегии:
1. Стратегия добавления - в конец домена добавляется символ.
2. Стратегия поддоменов - домен разделяется точкой.
3. Стратегия омоглифов - символов, похожих по написанию (о - 0, i - 1 и т.д.)
4. Стратегия удаления - из изначального домена удаляется один символ.

Проверка работы домена осуществляется с помощью команды gethostbyname.

В случае успешного получения ip-адреса, программа выводит сообщение о доступности домена.

##Инструкция

###Требования
Для того, чтобы можно было запустить программу потребуется Python 3.x

###Использование
После запуска программы нужно ввести изначальный домен.

Затем выбрать одну из 4-х стратегий. 

Перед запуском можно вручную изменить список добавляемых букв и омоглифов.

###Пример

    Enter domain: y
    Choose strategy: 
     1.Adding 
     2.Subdomain 
     3.Deleting 
     4.Homoglyphs 
     1
    Total -  572
    Thread-1 ya.com  - is available
    Thread-2 yb.com  - is available
    Thread-3 yc.com  - is available
    Thread-1 yd.com  - is available
    Thread-2 ye.com  - is available
    Thread-3 yf.com  - is available
    Thread-1 yg.com  - is available
    Thread-2 yh.com  - is available
    Thread-3 yi.com  - is available
    Thread-1 yj.com  - is available
    Thread-3 yl.com  - is available
    Thread-1 ym.com  - is available
    Thread-2 yn.com  - is available
    Thread-3 yo.com  - is available
    Thread-1 yp.com  - is available
    Thread-2 yq.com  - is available
    Thread-3 yr.com  - is available
    Thread-1 ys.com  - is available
    Thread-3 yu.com  - is available
    Thread-1 yv.com  - is available
    Thread-2 yw.com  - is available
    Thread-3 yx.com  - is available
    Thread-1 yy.com  - is available
    Thread-3 ya.ru  - is available
    ...
