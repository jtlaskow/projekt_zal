import pandas as pd
import os

path = r"/dane2020/20210215_Gminy_2_za_2020.xlsx"

def gminy2020(sciezka): #gminy2020
    gm2020 = pd.read_excel(sciezka, usecols = [0, 1, 2, 3, 4, 11], skiprows = [0, 1, 2, 4, 5, 6])

    gm2020 = gm2020.rename({"Dochody wykonane\n(wpłaty minus zwroty)" : 'dochody'}, axis ='columns')

    #tworzymy kolumnę z wlasciwym kodem id
    gm2020.WK = gm2020.WK.astype(str) #zmiana typu danych na string
    gm2020['WK'] = gm2020.apply(id, axis=1, column ='WK') #ewentualne dodanie 0

    gm2020.PK = gm2020.PK.astype(str)
    gm2020['PK'] = gm2020.apply(id, axis=1, column ='PK')

    gm2020.GK = gm2020.GK.astype(str)
    gm2020['GK'] = gm2020.apply(id, axis=1, column ='GK')

    gm2020.GT = gm2020.GT.astype(str)

    #kolumna id
    gm2020['id'] = gm2020['WK'] + gm2020['PK'] + gm2020['GK'] + gm2020['GT']

    gm2020 = gm2020[['id', 'Nazwa JST', 'dochody']]

    return gm2020


def id(row, column): #funkca dodaje zero przed liczbą jedno-cyfrową, dwucyfrową zostawia bez zmian
    if len(row[column]) == 1:
        val = '0' + row[column]
        #row['WK'] = val
    else:
        val = row[column]
    return val




path2 =  r"C:\Users\jerzy\PycharmProjects\projekt_zal\Ludność.Stan i struktura_31.12.2020\tabela12.xls"

def ludnosc_gminy(path):
    lg = pd.concat(pd.read_excel(path, sheet_name=None, usecols = [0, 1, 2], skiprows = [0, 1, 2,3, 4, 6,7]), ignore_index=True)

    lg.columns = ['gmina', 'id', 'populacja']

    lg = lg[lg['id'] != '       ']

    return lg




def main():
    gm2020 = gminy2020(path)

    lg = ludnosc_gminy(path2)

    gminy = pd.merge(gm2020, lg, how='left', on='id')

    print(gminy.head(20))

    print(gm2020.shape, lg.shape, gminy.shape)

    #print(gm2020.shape, lg.shape)




main()
#a tu co?
