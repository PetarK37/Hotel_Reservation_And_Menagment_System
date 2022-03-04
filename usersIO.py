import dataIO


def ucitavanje_korisnika():
    return dataIO.load('users.csv' , user_to_dict)

def ucitavanje_recepcionera():
    recepcioneri = dataIO.load('users.csv' , user_to_dict)
    ret_val = []
    for recepcioner in recepcioneri:
        if recepcioner['uloga'] == 'recepcioner':
            ret_val.append(recepcioner)
    return ret_val 

   
def user_to_str(user):
    user_str = str(user['korisnicko_ime']) + ',' +str(user['lozinka'])+ ',' + str(user['ime']) + ',' + str(user['prezime']) + ',' + str(user['broj_telefona']) + ',' + str(user['email']) + ',' + str(user['uloga']) + ','+ str(user['sifra_hotela']) + ',' + str(user['Obrisan']) + '\n'
    return user_str

def user_to_dict(users):
    row = users.rstrip().split(',')
    ret_val = {}
    ret_val['korisnicko_ime'] = row[0]
    ret_val['lozinka'] = row[1]
    ret_val['ime'] = row[2]
    ret_val['prezime'] = row[3]
    ret_val['broj_telefona'] = row[4]
    ret_val['email'] = row[5]
    ret_val['uloga'] = row[6]
    ret_val['sifra_hotela'] = row[7]
    ret_val['Obrisan'] = dataIO.str_to_bool(row[8])
    return ret_val

def dodaj_recepcionera( korisnicko_ime , lozinka , ime, prezime, broj_telefona, e_mail, sifra_hotela):
    novi_recepcioner = {'korisnicko_ime': korisnicko_ime , 'lozinka': lozinka , 'ime': ime, 'prezime': prezime , 'broj_telefona': broj_telefona, 'email': e_mail , 'uloga' : 'recepcioner', 'sifra_hotela': sifra_hotela,  'Obrisan': 'False'}
    korisnici = ucitavanje_korisnika()
    korisnici.append(novi_recepcioner)
    dataIO.save(korisnici , 'users.csv' , user_to_str)

def register( korisnicko_ime , lozinka , ime, prezime, broj_telefona, e_mail):
    novi_korisnik = {'korisnicko_ime': korisnicko_ime , 'lozinka': lozinka , 'ime': ime, 'prezime': prezime , 'broj_telefona': broj_telefona, 'email': e_mail , 'uloga' : 'korisnik', 'sifra_hotela':'',  'Obrisan': 'False'}
    korisnici = ucitavanje_korisnika()
    korisnici.append(novi_korisnik)
    dataIO.save(korisnici , 'users.csv' , user_to_str)

def brisanje_recepcionera(korisnicko_ime):
    recepcioneri = ucitavanje_korisnika()
    for korisnik in recepcioneri:
        if korisnik['uloga'] == 'recepcioner':
            if korisnicko_ime == korisnik['korisnicko_ime']:
                korisnik['Obrisan'] = True
    dataIO.save(recepcioneri , 'users.csv' , user_to_str)

def pretraga_recepcionera_po_imenu(ime):
    lista = ucitavanje_recepcionera()
    return dataIO.pretraga_po_parametru(lista, 'ime' , ime)

def pretraga_recepcionera_po_prezimenu(prezime):
    lista = ucitavanje_recepcionera()
    return dataIO.pretraga_po_parametru(lista, 'prezime' , prezime)

def pretraga_recepcionera_po_korisinickom_imenu(kor_ime):
    lista = ucitavanje_recepcionera()
    return dataIO.pretraga_po_parametru(lista, 'korisnicko_ime' , kor_ime)

def pretraga_recepcionera_po_email(email):
    lista = ucitavanje_recepcionera()
    return dataIO.pretraga_po_parametru(lista, 'email' , email)

def pretraga_recepcionera_po_hotelu(hotel):
    lista = ucitavanje_recepcionera()
    return dataIO.pretraga_po_parametru(lista, 'sifra_hotela' , hotel)

def pretraga_recepcionera_po_vise_kriterijuma(ime,prezime,kor_ime,email,hotel):
    recepcioneri = ucitavanje_recepcionera()
    recepcioneri_za_prikaz = []
    for recepcioner in recepcioneri:
        if recepcioner['uloga'] == 'recepcioner':
            if ime.lower() in recepcioner['ime'].lower():
                if prezime.lower() in recepcioner['prezime'].lower():
                    if kor_ime.lower() in recepcioner['korisnicko_ime'].lower():
                        if email.lower() in recepcioner['email'].lower():
                             if hotel.lower() in recepcioner['sifra_hotela'].lower():
                                recepcioneri_za_prikaz.append(recepcioner)
    return recepcioneri_za_prikaz

def login(korisnicko_ime , lozinka):
    lista_korisnika = ucitavanje_korisnika()
    for korisnik in lista_korisnika:
        if korisnicko_ime == korisnik['korisnicko_ime'] and lozinka == korisnik['lozinka']:
            return korisnik
    return None


