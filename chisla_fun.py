#!/usr/bin/env python
# -*- coding: utf-8 -*-

def sumchisl(tmp):
    tmp = sum([int(i) for i in tmp if i in '123456789'])
    if tmp > 9:
        return sumchisl(str(tmp))
    else:
        return tmp

def sumfi(tmp):
    #print(tmp)
    tmp = sum([int(i) for i in tmp if i in '123456789']) // 3
    #print(tmp)
    if tmp > 9:
        return sumchisl(str(tmp))
    else:
        return tmp


def strtochislo(tmp0):
    tmp = tmp0.replace('а', '1').replace('и', '1').replace('с', '1').replace('ъ', '1')
    tmp = tmp.replace('б', '2').replace('й', '2').replace('т', '2').replace('ы', '2')
    tmp = tmp.replace('в', '3').replace('к', '3').replace('у', '3').replace('ь', '3')
    tmp = tmp.replace('г', '4').replace('л', '4').replace('ф', '4').replace('э', '4')
    tmp = tmp.replace('д', '5').replace('м', '5').replace('х', '5').replace('ю', '5')
    tmp = tmp.replace('е', '6').replace('н', '6').replace('ц', '6').replace('я', '6')
    tmp = tmp.replace('ё', '7').replace('о', '7').replace('ч', '7')
    tmp = tmp.replace('ж', '8').replace('п', '8').replace('ш', '8')
    tmp = tmp.replace('з', '9').replace('р', '9').replace('щ', '9')
    return tmp


def date(message):
    date_tmp = message.text.replace(' ','').replace(':','').replace('.','').replace(',','')
    #print('tmp = {}'.format(date_tmp))
    return sumchisl(date_tmp)

def fio(message):
    date_tmp = message.text.replace(' ','').replace(':','').replace('.','').replace(',','').lower()
    #print('tmp = {}'.format(date_tmp))
    chislo_tmp = sumfi(strtochislo(date_tmp))
    return chislo_tmp

