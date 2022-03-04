import datetime
import dataIO
import random

def dodaj_rezervaciju(id , lista_soba , datum_kreiranja, datum_prijave, datum_odjave , korisnik , ocena):
    nova_rezervacija = {'id': id , 'Lista rezervisanih soba': lista_soba , 'Datum kreiranja': datum_kreiranja, 'Datum prijave': datum_prijave , 'Datum odjave': datum_odjave,'Korisnik': korisnik ,'Ocena': 0, 'Status rezervacije':'nije zapoceta' , 'Obrisan': "False"}
    rezervacije = ucitavanje_rezervacija()
    rezervacije.append(nova_rezervacija)
    return rezervacije

def ucitavanje_rezervacija():
    return dataIO.load('reservations.csv' , reservation_to_dict)

def reservation_to_dict(reservations):
    row = reservations.rstrip().split(',')
    ret_val = {}
    ret_val['id'] = row[0]
    ret_val['Lista rezervisanih soba'] = row[1]
    ret_val['Datum kreiranja'] = row[2]
    ret_val['Datum prijave'] = row[3]
    ret_val['Datum odjave'] = row[4]
    ret_val['Korisnik'] = row[5]
    ret_val['Ocena'] = row[6]
    ret_val['Status rezervacije'] = row[7]
    ret_val['Obrisan'] = dataIO.str_to_bool(row[8])
    return ret_val

def reservation_to_str(reservation):
    reservation_str = str(reservation['id']) + ',' +str(reservation['Lista rezervisanih soba'])+ ',' + str(reservation['Datum kreiranja']) + ',' + str(reservation['Datum prijave']) + ',' + str(reservation['Datum odjave']) + ',' + str(reservation['Korisnik']) + ',' + str(reservation['Ocena']) + ','+ str(reservation['Status rezervacije']) + ',' + str(reservation['Obrisan']) +'\n'
    return reservation_str


def rezervisanje_soba(lista_soba , datum_prijave , nocenja ,korisnik ,id_hotela):
    datum_kreiranja = datetime.datetime.now()
    datum_odjave = datetime.datetime.strptime(datum_prijave, '%Y-%m-%d').date() + datetime.timedelta(days = nocenja)
    korisnik = korisnik['korisnicko_ime']
    id = id_hotela[:3] + str(random.randrange(100, 999))
    ocena = ''
    rezervacija = dodaj_rezervaciju(id , dataIO.list_to_str(lista_soba) , datum_kreiranja, datum_prijave, datum_odjave , korisnik , ocena)
    return rezervacija

def dodaj_sobu(id , Broj_sobe , Broj_kreveta , Klima, TV, tip_sobe, Cena):
    nova_soba = {'id': id , 'Broj sobe': Broj_sobe , 'Broj kreveta': Broj_kreveta, 'Klima': Klima , 'TV': TV, 'Tip': tip_sobe ,'Cena': Cena, 'Obrisan': 'False', 'Rezervisana od' : '', 'Rezervisana do' : ''}
    sobe = dataIO.load('rooms.csv' , soba_to_dict)
    sobe.append(nova_soba)
    dataIO.save(sobe , 'rooms.csv' , soba_to_str)

def ucitavanje_soba(id):
    sobe = dataIO.load('rooms.csv' , soba_to_dict)
    sobe_za_prikaz = []
    for soba in sobe:
        if id[:3] == soba['id'][:3]:
            sobe_za_prikaz.append(soba)
    return sobe_za_prikaz

def slobodne_sobe(id, prijava, odjava):
    prikaz = ucitavanje_soba(id)
    rezervacije = ucitavanje_rezervacija()
    for rezervacija in rezervacije:
        if rezervacija['id'][:3] == id[:3]:
            lista_soba = dataIO.list_strip(rezervacija['Lista rezervisanih soba'])
            if  datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() >= datetime.datetime.strptime(prijava, '%Y-%m-%d').date() and datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date() >= datetime.datetime.strptime(odjava, '%Y-%m-%d').date() and datetime.datetime.strptime(odjava, '%Y-%m-%d').date() >  datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date():
                sobe = lista_soba[0]
                for soba in sobe:
                    if soba != '':
                        for i in  prikaz:
                            if i['Broj sobe'] == soba:
                                prikaz.remove(i)
            elif  datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() <= datetime.datetime.strptime(prijava, '%Y-%m-%d').date() and datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date() >= datetime.datetime.strptime(prijava, '%Y-%m-%d').date() and datetime.datetime.strptime(odjava, '%Y-%m-%d').date() >  datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() and datetime.datetime.strptime(odjava, '%Y-%m-%d').date() <  datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date():
                sobe = lista_soba[0]
                for soba in sobe:
                    if soba != '':
                        for i in  prikaz:
                            if i['Broj sobe'] == soba:
                                prikaz.remove(i)
            elif  datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() <= datetime.datetime.strptime(prijava, '%Y-%m-%d').date() and datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date() >= datetime.datetime.strptime(prijava, '%Y-%m-%d').date() and datetime.datetime.strptime(odjava, '%Y-%m-%d').date() >  datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date():
                sobe = lista_soba[0]
                for soba in sobe:
                    if soba != '':
                        for i in  prikaz:
                            if i['Broj sobe'] == soba:
                                prikaz.remove(i)
            elif  datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() <= datetime.datetime.strptime(prijava, '%Y-%m-%d').date() and datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() < datetime.datetime.strptime(odjava, '%Y-%m-%d').date() and datetime.datetime.strptime(odjava, '%Y-%m-%d').date() >  datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date():
                sobe = lista_soba[0]
                for soba in sobe:
                    if soba != '':
                        for i in  prikaz:
                            if i['Broj sobe'] == soba:
                                prikaz.remove(i)                     
    return prikaz

def soba_to_str(soba_str):
    soba_str_str = str(soba_str['id']) +','+soba_str['Broj sobe']+','+str(soba_str['Broj kreveta'])+','+soba_str['Klima']+','+soba_str['TV']+','+ soba_str['Tip'] + ',' +str(soba_str['Cena']) + ',' + str(soba_str['Obrisan']) + '\n'
    return soba_str_str

def soba_to_dict(soba):
    red = soba.rstrip().split(',')
    ret_val = {}
    ret_val['id'] = red[0]
    ret_val['Broj sobe'] = red[1]
    ret_val['Broj kreveta'] = red[2]
    ret_val['Klima'] = red[3]
    ret_val['TV'] = red[4]
    ret_val['Tip'] = red[5]
    ret_val['Cena'] = red[6]
    ret_val['Obrisan'] = dataIO.str_to_bool(red[7])
    return ret_val

def pretraga_soba_po_broju(broj,id):
    lista = ucitavanje_soba(id)
    return dataIO.pretraga_po_parametru(lista , 'Broj sobe' , broj)

def pretraga_soba_po_broju_kreveta(kreveti,id):
    lista = ucitavanje_soba(id)
    return dataIO.pretraga_po_parametru(lista , 'Broj kreveta' , kreveti)

def pretraga_soba_po_tipu(tip,id):
    lista = ucitavanje_soba(id)
    return dataIO.pretraga_po_parametru(lista , 'Tip' , tip)

def pretraga_soba_po_klimi(Klima,id):
    lista = ucitavanje_soba(id)
    return dataIO.pretraga_po_parametru(lista , 'Klima' , Klima)

def pretraga_soba_po_tv(tv,id):
    lista = ucitavanje_soba(id)
    return dataIO.pretraga_po_parametru(lista , 'TV' , tv)

def pretraga_soba_po_ceni(Cena ,id):
    lista = ucitavanje_soba(id)
    return dataIO.pretraga_po_parametru(lista , 'Cena' , Cena)

def pretraga_soba_po_vise_kriterijuma( datum_odjave,datum_prijave,broj_sobe , kreveti , tip , klima ,tv , cena, id  ):
    if cena == '':
        cena = '1' 
    if datum_odjave == '' or datum_prijave == '':
        sobe = ucitavanje_soba(id)
    else:
        sobe = slobodne_sobe(id, datum_prijave, datum_odjave)
    sobe_za_prikaz = []
    for soba in sobe:
        if broj_sobe.lower() in soba['Broj sobe'].lower(): 
            if kreveti.lower() in soba['Broj kreveta'].lower():
                if tip.lower() in soba['Tip'].lower():
                    if klima.lower() in soba['Klima'].lower():
                        if tv.lower() in soba['TV'].lower():
                         if eval(cena.lower()) <= eval(soba['Cena'].lower()):
                            sobe_za_prikaz.append(soba)

    return sobe_za_prikaz 

def ocenjivanje_hotela(id,ocena):
    lista = ucitavanje_rezervacija()
    for rezervacija in lista:
        if rezervacija['id'] == id:
            rezervacija['Ocena'] = ocena
    dataIO.save(lista ,'reservations.csv', reservation_to_str)

        
def update_reservation_data_reservations():
    rezervacije = dataIO.load('reservations.csv' , reservation_to_dict)
    for rezervacija in rezervacije:
            if datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() > datetime.datetime.now().date() and datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date() > datetime.datetime.now().date():
                rezervacija['Status rezervacije'] = 'Jos nije zapocela'
            elif datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date() < datetime.datetime.now().date() and datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() < datetime.datetime.now().date():
                rezervacija['Status rezervacije'] = 'Zavrsena'
            elif datetime.datetime.strptime(rezervacija['Datum prijave'], '%Y-%m-%d').date() < datetime.datetime.now().date() and datetime.datetime.strptime(rezervacija['Datum odjave'], '%Y-%m-%d').date() > datetime.datetime.now().date():
                rezervacija['Status rezervacije'] = 'U toku' 
    dataIO.save(rezervacije , 'reservations.csv' , reservation_to_str)

def pretraga_po_datumu_kreiranja(id,datum):
    lista = ucitavanje_rezervacija()
    hotel_list = []
    for item in lista:
        if item['id'][:3] == id[:3]:
            hotel_list.append(item)
    return dataIO.pretraga_po_parametru(hotel_list,'Datum kreiranja',datum)

def pretraga_po_datumu_prijave(id,datum):
    lista = ucitavanje_rezervacija()
    hotel_list = []
    for item in lista:
        if item['id'][:3] == id[:3]:
            hotel_list.append(item)
    return dataIO.pretraga_po_parametru(hotel_list,'Datum prijave',datum)

def pretraga_po_datumu_odjave(id,datum):
    lista = ucitavanje_rezervacija()
    hotel_list = []
    for item in lista:
        if item['id'][:3] == id[:3]:
            hotel_list.append(item)
    return dataIO.pretraga_po_parametru(hotel_list,'Datum odjave',datum)

def pretraga_po_korinsiku(id,korisnik):
    lista = ucitavanje_rezervacija()
    hotel_list = []
    for item in lista:
        if item['id'][:3] == id[:3]:
            hotel_list.append(item)
    return dataIO.pretraga_po_parametru(hotel_list,'Korisnik',korisnik)

def pretraga_po_statusu(id,status):
    lista = ucitavanje_rezervacija()
    hotel_list = []
    for item in lista:
        if item['id'][:3] == id[:3]:
            hotel_list.append(item)
    return dataIO.pretraga_po_parametru(hotel_list,'Status rezervacije',status)

def pretraga_po_vise_kriterijuma_rezervacije(id,datum_kreiranja , datum_prijave,datum_odjave,korisnik,stauts):
    lista = ucitavanje_rezervacija()
    hotel_list = []
    lista_za_prikaz = []
    for item in lista:
        if item['id'][:3] == id[:3]:
            hotel_list.append(item)
    for item in hotel_list:
        if datum_kreiranja.lower() in item['Datum kreiranja'].lower(): 
            if datum_prijave.lower() in item['Datum prijave'].lower():
                if datum_odjave.lower() in item['Datum odjave'].lower():
                    if korisnik.lower() in item['Korisnik'].lower():
                        if stauts.lower() in item['Status rezervacije'].lower():
                            lista_za_prikaz.append(item) 
    return lista_za_prikaz

def dnevni_izvestaj(id_hotela):
    izvestaj = {'Lista rezervisanih soba': '','Prosecna ocena': '','Ukupna zarada': '','Broj izdatih soba': '' ,'Broj rezervacija': ''}
    lista_rezervacija = []
    lista = ucitavanje_rezervacija()
    soba_list = ucitavanje_soba(id_hotela)
    prosecna_ocena = 0
    zarada = 0
    sobe = []
    sobe_za_prikaz = []
    for rezervacija in lista:
        if rezervacija['id'][:3] == id_hotela[:3] and datetime.datetime.now().date() == datetime.datetime.strptime(rezervacija['Datum kreiranja'], '%Y-%m-%d %H:%M:%S.%f').date():
            lista_soba = dataIO.list_strip(rezervacija['Lista rezervisanih soba'])
            for broj_sobe in lista_soba:
                    sobe.extend(broj_sobe)
            while '' in sobe:
                sobe.remove('')
            prosecna_ocena += int(rezervacija['Ocena']) / len(sobe)
            lista_rezervacija.append(rezervacija)
    for soba in soba_list:
        if soba['Broj sobe'] in sobe:
            zarada += int(soba['Cena'])
            sobe_za_prikaz.append(soba)

    izvestaj['Lista rezervisanih soba'] = sobe_za_prikaz
    izvestaj['Broj izdatih soba'] = len(sobe)
    izvestaj['Broj rezervacija'] = len(lista_rezervacija)
    izvestaj['Prosecna ocena'] = prosecna_ocena
    izvestaj['Ukupna zarada'] = zarada
    

    return izvestaj  

def nedeljni_izvestaj(id_hotela):
    izvestaj = {'Lista rezervisanih soba': '','Prosecna ocena': '','Ukupna zarada': '','Broj izdatih soba': '' ,'Broj rezervacija': ''}
    lista_rezervacija = []
    lista = ucitavanje_rezervacija()
    soba_list = ucitavanje_soba(id_hotela)
    prosecna_ocena = 0
    zarada = 0
    pocetak_nedelje = datetime.datetime.now().date() - datetime.timedelta(days = datetime.datetime.now().weekday())
    kraj_nedelje = pocetak_nedelje + datetime.timedelta(days = 6)

    sobe = []
    sobe_za_prikaz = []
    for rezervacija in lista:
        if rezervacija['id'][:3] == id_hotela[:3] and pocetak_nedelje <= datetime.datetime.strptime(rezervacija['Datum kreiranja'], '%Y-%m-%d %H:%M:%S.%f').date() and datetime.datetime.strptime(rezervacija['Datum kreiranja'], '%Y-%m-%d %H:%M:%S.%f').date() < kraj_nedelje:
            lista_soba = dataIO.list_strip(rezervacija['Lista rezervisanih soba'])
            for broj_sobe in lista_soba:
                    sobe.extend(broj_sobe)
            while '' in sobe:
                sobe.remove('')
            prosecna_ocena += int(rezervacija['Ocena']) / len(sobe)
            lista_rezervacija.append(rezervacija)
    for soba in soba_list:
        if soba['Broj sobe'] in sobe:
            zarada += int(soba['Cena'])
            sobe_za_prikaz.append(soba)
            
    izvestaj['Broj izdatih soba'] = len(sobe)
    izvestaj['Broj rezervacija'] = len(lista_rezervacija)
    izvestaj['Prosecna ocena'] = prosecna_ocena
    izvestaj['Ukupna zarada'] = zarada
    izvestaj['Lista rezervisanih soba'] = sobe_za_prikaz

    return izvestaj  

def mesecni_izvestaj(id_hotela):
    izvestaj = {'Lista rezervisanih soba': '','Prosecna ocena': '','Ukupna zarada': '','Broj izdatih soba': '' ,'Broj rezervacija': ''}
    lista_rezervacija = []
    lista = ucitavanje_rezervacija()
    soba_list = ucitavanje_soba(id_hotela)
    prosecna_ocena = 0
    zarada = 0
    mesec = datetime.datetime.now().strftime('%Y-%m')
    sobe = []
    sobe_za_prikaz = []
    for rezervacija in lista:
        if rezervacija['id'][:3] == id_hotela[:3] and mesec == datetime.datetime.strptime(rezervacija['Datum kreiranja'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m'):
            lista_soba = dataIO.list_strip(rezervacija['Lista rezervisanih soba'])
            for broj_sobe in lista_soba:
                    sobe.extend(broj_sobe)
            while '' in sobe:
                sobe.remove('')
            prosecna_ocena += int(rezervacija['Ocena']) / len(sobe)
            lista_rezervacija.append(rezervacija)
    for soba in soba_list:
        if soba['Broj sobe'] in sobe:
            zarada += int(soba['Cena'])
            sobe_za_prikaz.append(soba)

    izvestaj['Broj izdatih soba'] = len(sobe)
    izvestaj['Broj rezervacija'] = len(lista_rezervacija)
    izvestaj['Prosecna ocena'] = prosecna_ocena
    izvestaj['Ukupna zarada'] = zarada
    izvestaj['Lista rezervisanih soba'] = sobe_za_prikaz

    return izvestaj  