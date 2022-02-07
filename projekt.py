import gminy as gm
import powiaty as pw
import pandas as pd
import math

def kod(row): #funkcja skraca kod terytorialny gminy do kodu powiatu
   x = row['id']
   x = x[:-3]
   return x

def parametr(row, co, pod, kolumna): #funkcja licząca wariancję średniego dochodu jednostek podległych jednoste nadrzędnej lub ich średni dochód
    id = row['id'] #kod terytorialny jednostki nadrzędnej
    podrzedne = pod[pod['id2'] == id] #tabela jednostek podrzędnych

    if co == 'wariancja':
        dochody = podrzedne[kolumna]
        var = dochody.var()
        return math.floor(var)

    elif co == 'srednia wazona':
        #spopulacja podrzednych
        suma = podrzedne['populacja'].sum()

        #dodajemy kolumnę z odsetkiem populacji
        podrzedne['waga'] = podrzedne['populacja']/suma

        #mnożymy dochod sredni razy odsetek populacji
        podrzedne['dochod wazony'] = podrzedne[kolumna]*podrzedne['waga']

        #srednia wazona dochodów w jednostkach podległych to suma dochodów wazonych
        sr_wazona = podrzedne['dochod wazony'].sum()

        return math.floor(sr_wazona)


def main():
    powiaty = pw.powiaty()

    gminy = gm.gminy()
    gminy['id2'] = gminy.apply(kod, axis=1)

    #powiaty['wariancja 2019'] = powiaty.apply(wariancja, axis =1, pod = gminy, kolumna = 'średni dochód 2019')
    powiaty['wariancja 2019'] = powiaty.apply(parametr, axis =1, co = 'wariancja', pod = gminy, kolumna = 'średni dochód 2019')
    powiaty['wariancja 2020'] = powiaty.apply(parametr, axis =1, co = 'wariancja', pod = gminy, kolumna = 'średni dochód 2020')

    #test
    powiaty['sr wazona 2019'] = powiaty.apply(parametr, axis =1, co = 'srednia wazona', pod = gminy, kolumna = 'średni dochód 2019')
    powiaty['sr wazona 2020'] = powiaty.apply(parametr, axis =1, co = 'srednia wazona', pod = gminy, kolumna = 'średni dochód 2020')

    return powiaty
