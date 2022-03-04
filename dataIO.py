import datetime

def save(lista , naziv_fajla , konverter):
    file_out = open(naziv_fajla , 'w' , encoding="utf8")
    for entitet in lista:
        file_out.write(konverter(entitet))
    file_out.close()

def load(naziv_fajla , konverter):
    ret_val = []
    f = open( naziv_fajla, 'r', encoding="utf8")
    redovi = f.readlines()
    f.close()
    for row in redovi:
        value_dict = konverter(row.strip())
        if value_dict['Obrisan'] == False:
            ret_val.append(value_dict)
    return ret_val 

def str_to_bool(x):
    if x == 'True':
        return True
    else:
        return False

def list_to_str(x):
    str = ''
    for entitet in x:
        str = str  + entitet + ')'  
    return str

def list_strip(lista):
    ret_val = []
    ret_val.append(lista.rstrip().split(')'))
    return ret_val

def pretraga_po_parametru(lista , parametar , input ):
    lista_za_prikaz = []
    for entitet in lista:
        if parametar == 'Ocena' or parametar == 'Cena':
            if input == '':
                input = '1'
            if eval(input.lower()) <= eval(entitet[parametar].lower()):
                lista_za_prikaz.append(entitet)
        else:   
            if input.lower() in entitet[parametar].lower():
                lista_za_prikaz.append(entitet)
    return lista_za_prikaz 

def biranje_elemenata(lista , input , entitet):
    ret_val = ''
    if eval(input) <= len(lista):
        for ret_val in lista:
            ret_val = lista[eval(input)- 1][entitet]
    else:
        print('neispravan izbor')
    return ret_val

def autentifikacija(entitet , parametar ,lista):
    for data in lista:
        if entitet == data[parametar]:
            return False
    return True
