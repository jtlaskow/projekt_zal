import pandas as pd

from gminy import filtr, sr_dochod

path1 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2019\20200214_Powiaty_za_2019.xlsx'
path2 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2020\20210211_Powiaty_za_2020.xlsx'
path3 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\Ludność.Stan i struktura_31.12.2020\tabela05.xls'


def lud_powiaty(path):
    lp = pd.read_excel(path, usecols = [0,1,2], skiprows = [0,1,2,3,4,6,7,8,9])
    lp.columns = ['powiaty', 'id', 'populacja']

    lp = lp[lp['id'] > 0]   #biorę pod uwagę tylko powiaty, inne wiersze z pustymi wartościami wyrzucam
    lp.id = lp.id.astype(str)

    lp['id'] = lp.apply(id_pw, axis=1)

    return lp

def id_pw(row): #funkcja poprawia kod terytorialny na właściwy
    x = row['id']
    x = x[:-2]   #usuwam 2 ostatnie znaki, ponieważ były to zawsze '.' i '0' (wcześniej to był float)
    if len(x) == 3: #jeśli kod zaczynał się od 0, 0 znikało i trzeba dodać
        val = '0' + x
    else:
        val = x
    return val

def powiaty():
    pow2019 = filtr(path1, 'powiaty')
    pow2019.columns = ['id', 'powiat', 'dochod 2019']

    pow2020 = filtr(path2, 'powiaty')
    pow2020.columns = ['id', 'powiat2', 'dochod 2020']

    powiaty = pd.merge(pow2019, pow2020, how='left', on='id')
    powiaty = powiaty.drop(labels='powiat2', axis=1)

    lp = lud_powiaty(path3)
    powiaty2 = pd.merge(powiaty, lp, how='left', on='id')

    powiaty2 = powiaty2.drop(labels='powiaty', axis=1)

    #dodaję kolumny ze średnim dochodem
    powiaty2['średni dochód 2019'] = powiaty2.apply(sr_dochod, axis=1, dochodJST ='dochod 2019', udzialJST = 0.1025, prog = 0.17, odsetek_pracujacych = 0.7)
    powiaty2['średni dochód 2020'] = powiaty2.apply(sr_dochod, axis=1, dochodJST ='dochod 2020', udzialJST = 0.1025, prog = 0.17, odsetek_pracujacych = 0.7)

    powiaty2['średni dochód 2019'] = powiaty2['średni dochód 2019'].astype(int)
    powiaty2['średni dochód 2020'] = powiaty2['średni dochód 2020'].astype(int)

    return powiaty2









