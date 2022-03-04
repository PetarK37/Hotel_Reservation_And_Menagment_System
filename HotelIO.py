import dataIO
import reservation

def ucitavanje_hotela():
    return dataIO.load('hotels.csv' , hotel_to_dict)

def hotel_to_str(hotel):
    hotel_str = str(hotel['id']) +','+hotel['Naziv']+','+str(hotel['Adresa'])+','+hotel['Restoran']+','+hotel['Bazen']+','+str(hotel['Ocena']) + ',' + str(hotel['Obrisan']) + '\n'
    return hotel_str

def hotel_to_dict(hotel):
    red = hotel.rstrip().split(',')
    ret_val = {}
    ret_val['id'] = red[0]
    ret_val['Naziv'] = red[1]
    ret_val['Adresa'] = red[2]
    ret_val['Restoran'] = red[3]
    ret_val['Bazen'] = red[4]
    ret_val['Ocena'] = red[5]
    ret_val['Obrisan'] =  dataIO.str_to_bool(red[6])
    return ret_val

def pretraga_hotela_po_nazivu(naziv):
    lista = ucitavanje_hotela()
    return dataIO.pretraga_po_parametru(lista , 'Naziv' , naziv)

def pretraga_hotela_po_adresi(adresa):
    lista = ucitavanje_hotela()
    return dataIO.pretraga_po_parametru(lista , 'Adresa' , adresa) 

def pretraga_hotela_po_oceni(ocena):
    lista = ucitavanje_hotela()
    return dataIO.pretraga_po_parametru(lista , 'Ocena' , ocena)

def pretraga_hotela_po_restoranu(restoran):
    lista = ucitavanje_hotela()
    return dataIO.pretraga_po_parametru(lista , 'Restoran' , restoran)

def pretraga_hotela_po_bazenu(bazen):
    lista = ucitavanje_hotela()
    return dataIO.pretraga_po_parametru(lista , 'Bazen' , bazen)

def pretraga_hotela_po_vise_kriterijuma(naziv , adresa , restoran , bazen ,ocena):
    if ocena == '':
        ocena = '1' 
    hoteli = ucitavanje_hotela()
    hoteli_za_prikaz = []
    for hotel in hoteli:
        if naziv.lower() in hotel['Naziv'].lower(): 
            if adresa.lower() in hotel['Adresa'].lower():
                if restoran.lower() in hotel['Restoran'].lower():
                    if bazen.lower() in hotel['Bazen'].lower():
                         if eval(ocena.lower()) <= eval(hotel['Ocena'].lower()):
                            hoteli_za_prikaz.append(hotel)

    return hoteli_za_prikaz 

def dodaj_hotel(id , Naziv, Adresa, Restoran, Bazen):
    novi_hotel = {'id': id , 'Naziv': Naziv , 'Adresa': Adresa, 'Restoran': Restoran , 'Bazen': Bazen, 'Ocena': 0 ,'Obrisan': 'False'}
    hoteli = ucitavanje_hotela()
    hoteli.append(novi_hotel)
    dataIO.save(hoteli , 'hotels.csv' , hotel_to_str)



def azuriranje_hotela(id, Restoran, Bazen):
    hoteli = ucitavanje_hotela()
    for hotel in hoteli:
        if id == hotel['id']:
            hotel['Restoran'] = Restoran
            hotel['Bazen'] = Bazen    
    dataIO.save(hoteli , 'hotels.csv' , hotel_to_str)

def brisanje_hotela(id):
    hoteli = ucitavanje_hotela()
    sobe = reservation.ucitavanje_soba(id)
    for hotel in hoteli:
        if id == hotel['id']:
            hotel['Obrisan'] = True
    for soba in sobe:
        if str(soba['id'])[:3] == str(id)[:3]:
            soba['Obrisan']= True  
    dataIO.save(sobe , 'rooms.csv' , reservation.soba_to_str)              
    dataIO.save(hoteli , 'hotels.csv' , hotel_to_str)

def najbolje_ocenjeni():
    sortirano = sorted(ucitavanje_hotela(), key= lambda hotel: hotel['Ocena'] , reverse=True)
    return sortirano[:5]

