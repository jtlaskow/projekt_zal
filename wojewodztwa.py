from gminy import filtr, sr_dochod
import pandas as pd

path = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2019\20200214_Wojewodztwa_za_2019.xlsx'
path2 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2020\20210211_Województwa_za_2020.xlsx'
path3 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\Ludność.Stan i struktura_31.12.2020\tabela02.xls'


def lud_powiaty(path):
    lp = pd.read_excel(path, usecols = [0,1,2], skiprows = [0,1,2,3,4,6,7,8,9])
    lp.columns = ['powiaty', 'id', 'populacja']

    lp = lp[lp['id'] > 0]   #biorę pod uwagę tylko powiaty, inne wiersze z pustymi wartościami wyrzucam
    lp.id = lp.id.astype(str)

    lp['id'] = lp.apply(id_pw, axis=1)

    return lp

def lud_woj(path):
    lw = pd.read_excel(path, usecols = [0,1], skiprows = [0,1,2,3,4,6,7,8])
    lw.columns = ['wojewodztwo', 'populacja']
    lw['wojewodztwo'] = lw['wojewodztwo'].str.lower()

    return lw


def wojewodztwa():
    woj2019 = filtr(path ,'woj')
    woj2019.columns = ['id', 'wojewodztwo', 'dochod 2019']

    woj2020 = filtr(path2, 'woj')
    woj2020.columns = ['id', 'wojewodztwo', 'dochod 2020']
    woj2020 = woj2020.drop(labels='wojewodztwo', axis=1)

    woj = pd.merge(woj2019, woj2020, how='left', on='id')

    lw = lud_woj(path3)
    woj2 = pd.merge(woj, lw, how='left', on='wojewodztwo')

    #sredni dochod
    woj2['średni dochód 2019'] = woj2.apply(sr_dochod, axis=1, dochodJST ='dochod 2019', udzialJST = 0.016, prog = 0.17, odsetek_pracujacych = 0.7)
    woj2['średni dochód 2020'] = woj2.apply(sr_dochod, axis=1, dochodJST ='dochod 2020', udzialJST = 0.016, prog = 0.17, odsetek_pracujacych = 0.7)

    woj2['średni dochód 2019'] = woj2['średni dochód 2019'].astype(int)
    woj2['średni dochód 2020'] = woj2['średni dochód 2020'].astype(int)



    print(woj2)

wojewodztwa()
