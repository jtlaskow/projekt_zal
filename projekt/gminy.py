import pandas as pd
import math
import os

def filtr(sciezka, jst): #funkcja uniwersalna dla gmin, powiatów - tworzy ramkę potrzebnych danych, twotzy kolumnę z kodem id
    df = pd.read_excel(sciezka, usecols = [0, 1, 2, 3, 4, 11], skiprows = [0, 1, 2, 4, 5, 6])

    df = df.rename({"Dochody wykonane\n(wpłaty minus zwroty)" : 'dochody'}, axis ='columns')

    #tworzymy kolumnę z wlasciwym kodem id
    df.WK = df.WK.astype(str) #zmiana typu danych na string
    df['WK'] = df.apply(id, axis=1, column ='WK') #ewentualne dodanie 0

    df.PK = df.PK.astype(str)
    df['PK'] = df.apply(id, axis=1, column ='PK')

    df.GK = df.GK.astype(str)
    df['GK'] = df.apply(id, axis=1, column ='GK')

    df.GT = df.GT.astype(str)

    #kolumna id dla gmin
    if jst == 'gminy':
        df['id'] = df['WK'] + df['PK'] + df['GK'] + df['GT']

    elif jst == 'powiaty':
        df['id'] = df['WK'] + df['PK']

    elif jst == 'woj':
        df['id'] = df['WK']

    df = df[['id', 'Nazwa JST', 'dochody']]

    return df

def id(row, column): #funkca dodaje zero przed liczbą jedno-cyfrową, dwucyfrową zostawia bez zmian
    if len(row[column]) == 1:
        val = '0' + row[column]
    else:
        val = row[column]
    return val


def ludnosc_gminy(path):
    lg = pd.concat(pd.read_excel(path, sheet_name=None, usecols = [0, 1, 2], skiprows = [0, 1, 2,3, 4, 6,7]), ignore_index=True)

    lg.columns = ['gmina', 'id', 'populacja']

    lg = lg[lg['id'] != '       ']
    lg = lg.dropna(axis = 0)  #usuwam wiersze, w których id = NaN
    lg.id = lg.id.astype(str) #część wartości była int

    return lg

def sr_dochod(row, dochodJST, udzialJST, prog, odsetek_pracujacych): #średni dochód miaszkańca danej JST administracyjnej
    '''
    1. żeby policzyć całość podatku odprowadzanego przez mieszkańców dzielę dochód JST przez procent jej udziału.
    2. Następnię wartość dzielę przez liczbę mieszkańców odprowadzających podatki (odsetek pracujących wyznaczam arbitralnie)
    3. Uzyskaną wartość dzielę przez 1 próg podatkowy
    4. otrzymuję średni ROCZNY dochód mieszkańca danej JST'''

    sr_dochod = row[dochodJST]/(udzialJST * prog * row['populacja'] * odsetek_pracujacych)
    #sr_dochod = math.floor(sr_dochod)

    return sr_dochod

def gminy(gminy2019, gminy2020, ludnosc): #funkcja tworzy pełną tabelę dla gmin (parametry to ścieżki)
    gm2020 = filtr(gminy2020, 'gminy')
    lg = ludnosc_gminy(ludnosc)
    gm2019 = filtr(gminy2019, 'gminy')

    #łączę tabele dochody 2020 i ludność
    df = pd.merge(gm2020, lg, how='left', on='id')
    df = df[['id', 'gmina', 'dochody', 'populacja']]
    df.columns = ['id', 'gmina', 'dochody 2020', 'populacja']

    #łączę df i dochody 2019
    df = pd.merge(df, gm2019, how='left', on='id')
    df = df[['id', 'gmina', 'dochody', 'dochody 2020', 'populacja']]
    df.columns = ['id', 'gmina', 'dochody 2019', 'dochody 2020', 'populacja']

    #średni dochód
    df['średni dochód 2019'] = df.apply(sr_dochod, axis=1, dochodJST ='dochody 2019', udzialJST = 0.3816, prog = 0.17, odsetek_pracujacych = 0.7)
    df['średni dochód 2020'] = df.apply(sr_dochod, axis=1, dochodJST ='dochody 2020', udzialJST = 0.3816, prog = 0.17, odsetek_pracujacych = 0.7)

    df = df.dropna(axis=0) #usuwa kilkanaście wierszy z wartością NaN
    df['średni dochód 2019'] = df['średni dochód 2019'].astype(int)
    df['średni dochód 2020'] = df['średni dochód 2020'].astype(int)

    return df

'''gm = gminy(gm2019, gm2020, gm_ludnosc)
print(gm)
print(gm.dtypes, gm.shape)'''
