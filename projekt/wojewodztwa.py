from projekt.powiaty import *
import pandas as pd

wojewodztwa2019 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2019\20200214_Wojewodztwa_za_2019.xlsx'
wojewodztwa2020 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2020\20210211_Województwa_za_2020.xlsx'
wojewodztwa_ludnosc = r'C:\Users\jerzy\PycharmProjects\projekt_zal\Ludność.Stan i struktura_31.12.2020\tabela02.xls'

def lud_woj(path):
    lw = pd.read_excel(path, usecols = [0,1], skiprows = [0,1,2,3,4,6,7,8])
    lw.columns = ['wojewodztwo', 'populacja']
    lw['wojewodztwo'] = lw['wojewodztwo'].str.lower()

    return lw

def wojewodztwa(wj2019, wj2020, wj_lud, *args): #(parametry to ścieżki)
    woj2019 = filtr(wj2019, 'woj')
    woj2019.columns = ['id', 'wojewodztwo', 'dochod 2019']

    woj2020 = filtr(wj2020, 'woj')
    woj2020.columns = ['id', 'wojewodztwo', 'dochod 2020']
    woj2020 = woj2020.drop(labels='wojewodztwo', axis=1)

    woj = pd.merge(woj2019, woj2020, how='left', on='id')

    lw = lud_woj(wj_lud)
    woj2 = pd.merge(woj, lw, how='left', on='wojewodztwo')

    #sredni dochod
    woj2['średni dochód 2019'] = woj2.apply(sr_dochod, axis=1, dochodJST ='dochod 2019', udzialJST = 0.016, prog = 0.17, odsetek_pracujacych = 0.7)
    woj2['średni dochód 2020'] = woj2.apply(sr_dochod, axis=1, dochodJST ='dochod 2020', udzialJST = 0.016, prog = 0.17, odsetek_pracujacych = 0.7)

    woj2['średni dochód 2019'] = woj2['średni dochód 2019'].astype(int)
    woj2['średni dochód 2020'] = woj2['średni dochód 2020'].astype(int)

    #wariancja i średni dochód
    for tab in args: #dodatkowy argument - dzięki temu powstaje tabela z dodatkowymi kolumnami lub bez nich
        pw = tab
        pw['id2'] = pw.apply(kod, axis=1)

        woj2['wariancja 2019'] = woj2.apply(parametr, axis =1, co = 'wariancja', pod = pw, kolumna = 'średni dochód 2019')
        woj2['wariancja 2020'] = woj2.apply(parametr, axis =1, co = 'wariancja', pod = pw, kolumna = 'średni dochód 2020')

        woj2['sr wazona 2019'] = woj2.apply(parametr, axis =1, co = 'srednia wazona', pod = pw, kolumna = 'średni dochód 2019')
        woj2['sr wazona 2020'] = woj2.apply(parametr, axis =1, co = 'srednia wazona', pod = pw, kolumna = 'średni dochód 2020')

        #porównanie dochodu średniego z dochodem estymowanym przez gminy
        woj2['porównanie 2019'] = woj2['średni dochód 2019']/woj2['sr wazona 2019']
        woj2['porównanie 2020'] = woj2['średni dochód 2020']/woj2['sr wazona 2020']

    return woj2

#słabo bo, żeby stworzyć tabelę dla wojewodztw trzeba wczesniej stworzyc tabele powiatow, a wczesniej gmin
#już działa
'''gm = gminy(gm2019, gm2020, gm_ludnosc)
pow = powiaty(pow2019, pow2020, pow_ludnosc, gm)
woj = wojewodztwa(wojewodztwa2019, wojewodztwa2020, wojewodztwa_ludnosc, pow)
print(woj) #sredni dochód wojewodztw nie do konca sie zgadza z estymowanym przez powiaty

print(woj.shape, woj.dtypes)'''

