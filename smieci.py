def lg3(path): #do otwierania gmin - wszystkie skoroszyty excela w jednym dictionary

    '''xl_file = pd. ExcelFile("sample1.xls")
    sheet_names = xl_file. sheet_names.
    print(sheet_names)
    df = xl_file. parse("Sheet1")
    print(df)'''

    lg = pd.ExcelFile(path2)
    sheet_names = lg.sheet_names
    print(sheet_names)

    df = lg.parse('Kujawsko-pomorskie')
    print(df)

    #print(lg)

#tabela IV - id to float zamiast string
path3 = r'C:\Users\jerzy\PycharmProjects\projekt_zal\Ludność.Stan i struktura_31.12.2020\Tabela_IV.xls'

def lg2(path): #float
    lg = pd.read_excel(path, usecols = [0, 1, 2], skiprows = [0,1,2,4,5,6,7,8])
    lg.columns = ['gmina', 'id', 'populacja']

    return lg

def ludnosc_gminy(path, sheet): #pierwotna dla pojedynczego sheeta
    #lg = pd.read_excel(path,usecols = [0, 1, 2], skiprows = [0, 1, 2,3, 4, 6,7]) #sheet_name=None
    lg = pd.read_excel(path, sheet_name= sheet,usecols = [0, 1, 2], skiprows = [0, 1, 2,3, 4, 6,7]) #sheet_name=None
    lg.columns = ['gmina', 'id', 'mieszkancy']

    lg = lg[lg['id'] != '       ']

    return lg

def id(row): #tworzymy kolumnę z id takim, jak w ludnosc_gminy
    if len(row['WK']) == 1:
        val = '0' + row['WK']
        #row['WK'] = val
    else:
        val = row['WK']
    return val

def gminy(sciezka): #gminy2020
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

def gminy2():

    gm2020 = filtr(path, 'gminy')
    lg = ludnosc_gminy(path2)
    gm2019 = filtr(path3, 'gminy')

    df = pd.merge(gm2020, lg, how='left', on='id')

    #print(df.iloc[590:630])
    #print(df.shape)

    print(gm2020)
    print(gm2020.shape)
    print(lg)
    print(lg.shape)
    #print(lg[lg.gmina == 'Bełchatów']) #44338
    print(lg.iloc[2400:2430])
    print(gm2019)
    print(gm2019.shape)

def podrzedne(nadrzedna, podrzedna):
    id = nadrzedna.iloc[0,0]
    pod = podrzedna[podrzedna['id2'] == id]

    return pod

#trzyyyyy
