from projekt.gminy import *
import math

pow2019 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2019\20200214_Powiaty_za_2019.xlsx'
pow2020 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\dane2020\20210211_Powiaty_za_2020.xlsx'
pow_ludnosc = r'C:\Users\jerzy\PycharmProjects\projekt_zal\Ludność.Stan i struktura_31.12.2020\tabela05.xls'

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

def kod(row): #funkcja skraca kod terytorialny gminy do kodu powiatu, lub kod powiatu do kodu województwa
   x = row['id']
   if len(x) == 7: #skraca kod gmin
       x = x[:-3]

   elif len(x) ==4: #skraca kod powiatów
       x = x[:2]

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

def powiaty(powiaty2019, powiaty2020, ludnosc, *args): #(parametry to ścieżki)
    pow2019 = filtr(powiaty2019, 'powiaty')
    pow2019.columns = ['id', 'powiat', 'dochod 2019']

    pow2020 = filtr(powiaty2020, 'powiaty')
    pow2020.columns = ['id', 'powiat2', 'dochod 2020']

    powiaty = pd.merge(pow2019, pow2020, how='left', on='id')
    powiaty = powiaty.drop(labels='powiat2', axis=1)

    lp = lud_powiaty(ludnosc)
    powiaty2 = pd.merge(powiaty, lp, how='left', on='id')

    powiaty2 = powiaty2.drop(labels='powiaty', axis=1)

    #dodaję kolumny ze średnim dochodem
    powiaty2['średni dochód 2019'] = powiaty2.apply(sr_dochod, axis=1, dochodJST ='dochod 2019', udzialJST = 0.1025, prog = 0.17, odsetek_pracujacych = 0.7)
    powiaty2['średni dochód 2020'] = powiaty2.apply(sr_dochod, axis=1, dochodJST ='dochod 2020', udzialJST = 0.1025, prog = 0.17, odsetek_pracujacych = 0.7)

    powiaty2['średni dochód 2019'] = powiaty2['średni dochód 2019'].astype(int)
    powiaty2['średni dochód 2020'] = powiaty2['średni dochód 2020'].astype(int)

    #wariancja i dochód ważony gmin
    for tabela in args:
        gm = tabela
        gm['id2'] = gm.apply(kod, axis=1)

        powiaty2['wariancja 2019'] = powiaty2.apply(parametr, axis =1, co = 'wariancja', pod = gm, kolumna = 'średni dochód 2019')
        powiaty2['wariancja 2020'] = powiaty2.apply(parametr, axis =1, co = 'wariancja', pod = gm, kolumna = 'średni dochód 2020')

        powiaty2['sr wazona 2019'] = powiaty2.apply(parametr, axis =1, co = 'srednia wazona', pod = gm, kolumna = 'średni dochód 2019')
        powiaty2['sr wazona 2020'] = powiaty2.apply(parametr, axis =1, co = 'srednia wazona', pod = gm, kolumna = 'średni dochód 2020')

    return powiaty2

'''gm = gminy(gm2019, gm2020, gm_ludnosc)
pw = powiaty(pow2019, pow2020, pow_ludnosc) #działa z dodadtowym argumentem - tabelą gmin, lub bez niego
print(pw)
print(pw.shape)
print(pw.dtypes)'''








