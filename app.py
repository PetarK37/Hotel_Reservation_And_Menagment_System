import usersIO
import HotelIO
import dataIO
import promenjive
import reservation
import datetime
import time
import random

print('Dobro dosli')


def prijava():
    while True:
        korisnicko_ime = input('korisnicko ime:')
        lozinka = input('lozinka:')
        korisnik = usersIO.login(korisnicko_ime,lozinka)
        while not  korisnik:
            print('\nNeispravni korisnicki podaci!')
            korisnicko_ime = input('korisnicko ime: ')
            lozinka = input('lozinka: ')
            korisnik = usersIO.login( korisnicko_ime , lozinka)
            break
        return korisnik

def main():
    while True:
        print("\nIzaberite opciju:")
        print('1. Registrujte se')
        print('2. Ulogujte se')
        print('0. Izadji')
        choice = input('> ')

        if choice == '1':
            korisnicko_ime = input('Unesite korisnicko ime: ')
            lozinka = input('Unesite lozinku: ')
            ime = input('Unesite vase ime: ')
            prezime = input('Unesite vase prezime: ')
            broj_telefona = input('Unesite broj telefona: ')
            e_mail = input('Unesite e-mail: ')
            lista_korisnika = usersIO.ucitavanje_korisnika()
            autentifikacija = dataIO.autentifikacija(korisnicko_ime,'korisnicko_ime',lista_korisnika)
            if (korisnicko_ime != '' and  lozinka != '' and  ime != '' and  ime != '' and  prezime != '' and  e_mail != '' and autentifikacija == True): 
                usersIO.register( korisnicko_ime , lozinka , ime, prezime, broj_telefona, e_mail)
            elif (korisnicko_ime != '' and  lozinka != '' and  ime != '' and  ime != '' and  prezime != '' and  e_mail != '' and autentifikacija == False): 
                print("Vec postoji korisnik sa tim korisnickim imenom")
            else:
                print('\nMorate uneti sve podatke!')
                pass
        elif choice == '2': 
            promenjive.korisnik = prijava()
            if promenjive.korisnik:
                if promenjive.korisnik['uloga'] == 'admin':
                    admin_menu()
                    break
                elif promenjive.korisnik['uloga'] == 'recepcioner':
                    recepcioner_menu()
                    break
                elif promenjive.korisnik['uloga'] == 'korisnik':
                    user_menu()
                    break 
        elif choice == '0':
            quit()
        else:
            print('Izabrali ste nepostojecu opciju')




def user_menu():
    
    print("\nIzaberite opciju:")
    print('1. Pregled hotela')
    print('2. Pretraga hotela')
    print('3. Prikaz najbolje ocenjenih hotela ')
    print('4. Kreiraj rezervaciju')
    print('5. Moje rezervacije')
    print('6. Oceni hotel')
    print('0. Odjavi se')

    choice = input('> ')
    while True:
        if choice == '1':
            zaglavlje_hotele()
            prikaz = HotelIO.ucitavanje_hotela()
            prikaz_hotela(prikaz)
            time.sleep(2) 
            user_menu()
        elif choice == '2':
            pretraga_hotela_menu()
        elif choice == '3':
            zaglavlje_hotele()
            prikaz = HotelIO.najbolje_ocenjeni()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '4':
            zaglavlje_hotele()
            prikaz = HotelIO.ucitavanje_hotela()
            prikaz_hotela(prikaz)
            print("\nIzaberite hotel:")
            choice = input('> ')
            id_hotela = dataIO.biranje_elemenata(prikaz, choice, 'id')
            if choice == '':
                user_menu()
            else:
                datum_prijave = input('Kada se prijavljjete(godina-mesec-dan):')
                nocenja = int(input("koliko noci ostajete:"))
                datum_odjave = datetime.datetime.strptime(datum_prijave, '%Y-%m-%d').date() + datetime.timedelta(days = nocenja)
                while True:
                    zaglavlje_sobe() 
                    prikaz = reservation.slobodne_sobe(id_hotela , str(datum_prijave) , str(datum_odjave))
                    prikaz_soba(prikaz)
                    print("\n Izaberite sobu po rednom broju(enter oznacava kraj):")
                    choice = input('> ')
                    if choice != '':
                        broj_sobe = dataIO.biranje_elemenata(prikaz, choice, 'Broj sobe')
                        promenjive.rezervisane_sobe.append(broj_sobe)
                        lista_soba = promenjive.rezervisane_sobe
                        rezervacije = reservation.rezervisanje_soba(lista_soba , datum_prijave , nocenja , promenjive.korisnik ,id_hotela) 
                    else:
                        dataIO.save(rezervacije , 'reservations.csv' , reservation.reservation_to_str)
                        promenjive.rezervisane_sobe = []
                        user_menu()                                   
        elif choice == '5':
            reservation.update_reservation_data_reservations()
            reservation_menu()
        elif choice == '6':
            reservation.update_reservation_data_reservations()
            zaglavlje_rezervacije()
            rezervacije = reservation.ucitavanje_rezervacija()
            prikaz = []
            for rezervacija in rezervacije:
                if rezervacija['Korisnik'] == promenjive.korisnik['korisnicko_ime']:
                    if rezervacija['Status rezervacije'] == 'Zavrsena' and rezervacija['Ocena'] == '0':
                        prikaz.append(rezervacija)
            prikaz_rezervacija(prikaz)
            choice = input('> ')
            if choice != '':
                sifra_rezervacije= str(dataIO.biranje_elemenata(prikaz, choice , 'id'))
                ocena = input('Koju ocenu dajete hotelu:')
                reservation.ocenjivanje_hotela(sifra_rezervacije,ocena)
                print('Uspesno izmenjeni podaci!')
                time.sleep(1) 
                user_menu()
            else:
                user_menu()



        elif choice == '0':
            promenjive.korisnik = {}
            main()
        else:
            print('nepostojeci izbor')
            user_menu()
        
            
def reservation_menu():
    print("\nIzaberite opciju:")
    print('1. Prethodne rezervacije')
    print('2. Rezervacije u toku')
    print('3. Buduce rezervacije')
    print('0. Nazad')
    choice = input('> ')

    rezervacije = reservation.ucitavanje_rezervacija()

    while True:
        if choice == '1':
            prikaz = []
            for rezervacija in rezervacije:
                if rezervacija['Status rezervacije'] == 'Zavrsena' and rezervacija['Korisnik'] == promenjive.korisnik['korisnicko_ime']:
                    prikaz.append(rezervacija)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1) 
            break
        elif choice == '2':
            prikaz = []
            for rezervacija in rezervacije:
                if rezervacija['Status rezervacije'] == 'U toku'and rezervacija['Korisnik'] == promenjive.korisnik['korisnicko_ime']:
                    prikaz.append(rezervacija)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1) 
            break
        elif choice == '3':
            prikaz = []
            for rezervacija in rezervacije:
                if rezervacija['Status rezervacije'] == 'Jos nije zapocela'and rezervacija['Korisnik'] == promenjive.korisnik['korisnicko_ime']:
                    prikaz.append(rezervacija)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1) 
            break
        elif choice == '0':
            user_menu()
        else:
            print('nepostojeci izbor')
            break
        


def pretraga_hotela_menu():
    print("\nIzaberite opciju:")
    print('1. Pretraga po jednom kriterijumu')
    print('2. Pretraga po vise kriterijuma')
    print('0. Nazad')
    choice = input('> ')
    
    while True:
        if choice == '1':
            pretraga_po_kriterijumu_meni()
        elif choice == '2':
            naziv = input('Unesite naziv hotela:')
            adresa = input('Unesite adresu:')
            restoran = input('Da li ima restoran:')
            bazen = input('Da li ima bazen:')
            ocena = input('Koja je minimalna ocena:')
            
            prikaz = HotelIO.pretraga_hotela_po_vise_kriterijuma(naziv , adresa , restoran , bazen ,ocena)

            zaglavlje_hotele()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '0':
           user_menu()
        else:
            print('nepostojeci izbor')
            break

def pretraga_po_kriterijumu_meni():
    print("\nIzaberite opciju:")
    print('1. Pretraga po nazivu')
    print('2. Pretraga po adresi')
    print('3. Pretraga po restoranu')
    print('4. Pretraga po baeznu')
    print('5. Pretraga po oceni')
    print('0. Nazad')

    choice = input('> ')

    while True:
        if choice == '1':
            naziv = input('Unesite naziv hotela:')
            prikaz = HotelIO.pretraga_hotela_po_nazivu(naziv)
            zaglavlje_hotele()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '2':
            adresa = input('Unesite adresu hotela:')
            prikaz = HotelIO.pretraga_hotela_po_adresi(adresa)
            zaglavlje_hotele()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '3':
            restoran = input('Da li ima restoran:')
            prikaz = HotelIO.pretraga_hotela_po_restoranu(restoran)
            zaglavlje_hotele()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '4':
            bazen = input('Da li ima bazen:')
            prikaz = HotelIO.pretraga_hotela_po_bazenu(bazen)
            zaglavlje_hotele()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '5':
            ocena = input('Unesite minimalnu ocenu:')
            prikaz = HotelIO.pretraga_hotela_po_oceni(ocena)
            zaglavlje_hotele()
            prikaz_hotela(prikaz)
            time.sleep(1) 
            break
        elif choice == '0':
            pretraga_hotela_menu()
        else:
            break
     

def admin_menu():
    print("\nIzaberite opciju:")
    print('1. Ažuriranje hotela')
    print('2. Dodavanje novih hotela ')
    print('3. Brisanje hotela')
    print('4. Pretraga recepcionera ')
    print('5. Dodavanje recepcionera ')
    print('6. Brisanje recepcionera') 
    print('0. Odjavi se')
     
    choice = input('> ')
    while True:
        if choice == '1':
            azuriranje_hotela_menu()
        elif choice == '2':
            id = str(random.randrange(100000, 999999))
            Naziv = input('Unesite naziv hotela:')
            Adresa = input('Unesite adresu hotela:')
            Restoran = input('Da li ima resotran:')
            Bazen = input('Da li ima bazen:')
            lista_hotela = HotelIO.ucitavanje_hotela()
            autentifikacija = dataIO.autentifikacija(id,'id',lista_hotela)
            if autentifikacija:
                HotelIO.dodaj_hotel(id , Naziv, Adresa, Restoran, Bazen)
            else:
                print('Vec postoji hotel sa tim ID-jem')
            while True:
                potvrda = input('Da li dodajte jos jedna sobu(enter oznacava kraj):')
                if potvrda == '':
                    print('Uspesno ste dodali sobe!')
                    time.sleep(1)
                    admin_menu()
                else:
                    id_input = input('Unesite id sobe:')
                    id_sobe = id[:3] + id_input
                    Broj_sobe = input('Unesite broj sobe')
                    Broj_kreveta = input('Unesite broj kreveta')
                    Klima = input('Da li ima klimu:')
                    TV = input('Da li ima Tv:')
                    tip_sobe = input('Koji je tip sobe:')
                    Cena = input('Cena po nocenju je:')

                    reservation.dodaj_sobu(id_sobe , Broj_sobe , Broj_kreveta , Klima, TV, tip_sobe, Cena)
                
        elif choice == '3':
            brisanje_hotela_menu()
        elif choice == '4':
            pretraga_recepcionera_menu() 
        elif choice == '5':
            zaglavlje_hotele()
            prikaz = HotelIO.ucitavanje_hotela()
            prikaz_hotela(prikaz)
            print("\nIzaberite kom hotelu dodajete radnika:")
            choice = input('> ')

            while True:
                if choice == '':
                    admin_menu()
                else:
                    korisnicko_ime = input('Unesite korisnicko ime:')
                    lozinka = input('Unesite lozinku:')
                    ime = input('Unesite ime:')
                    prezime = input('Unesite prezime:')
                    broj_telefona = input('Unesite broj telefona:')
                    e_mail = input('Unesite e-mail:')
                    sifra_hotela = dataIO.biranje_elemenata(prikaz, choice , 'id')

                    usersIO.dodaj_recepcionera( korisnicko_ime , lozinka , ime, prezime, broj_telefona, e_mail, sifra_hotela)
                    print("Recepcioner uspesno dodat")
                    time.sleep(1)
                    admin_menu()
        elif choice == '6':
            zaglavlje_recepcioneri()
            prikaz = usersIO.ucitavanje_recepcionera()
            prikaz_recepcionera(prikaz)
            print("\nIzaberite kog recepcionera brisemo:")
            choice = input('> ')
            while True:
                if choice == '':
                    admin_menu()
                else:
                    korisnik = dataIO.biranje_elemenata(prikaz , choice , 'korisnicko_ime')
                    usersIO.brisanje_recepcionera(korisnik)
                    admin_menu()
        elif choice == '0':
            promenjive.korisnik = {}
            main()
        else:
            print('nepostojeci izbor')
            admin_menu()

def azuriranje_hotela_menu():
    zaglavlje_hotele()
    prikaz = HotelIO.ucitavanje_hotela()
    prikaz_hotela(prikaz)
    print("\nIzaberite hotel(0):")
    choice = input('> ')
    while True:
        if choice == '':
            admin_menu()
        else:
            hotel = dataIO.biranje_elemenata(prikaz, choice , 'id')
            azuriranje_hotela_sub(hotel)
    
def azuriranje_hotela_sub(hotel):
    print("\nIzaberite opciju:")
    print('1. Izmena podataka')
    print('2. Dodavanje soba')
    print('0. Nazad')
    choice = input('> ')
   
    while True:
        if choice == '1':
            restoran = input('Da li ima restoran:')
            bazen = input('Da li ima bazen:')
            HotelIO.azuriranje_hotela(hotel ,restoran , bazen)
            print('Uspesno izmenjeni podaci!')
            time.sleep(1) 
            break
        elif choice == '2':
            potvrda = input('Da li dodajte jos jedna sobu(enter oznacava kraj):')
            if potvrda == '':
                print('Uspesno ste promenili podatke!')
                time.sleep(1)
                admin_menu()
            else:
                id_input = input('Unesite id sobe(3 cifre):')
                id = hotel[:3] + id_input
                Broj_sobe = input('Unesite broj sobe')
                Broj_kreveta = input('Unesite broj kreveta')
                Klima = input('Da li ima klimu:')
                TV = input('Da li ima Tv:')
                tip_sobe = input('Koji je tip sobe:')
                Cena = input('Cena po nocenju je:')
                
                reservation.dodaj_sobu(id, Broj_sobe , Broj_kreveta , Klima, TV, tip_sobe, Cena)
        elif choice =='0':
            azuriranje_hotela_menu()
        else:
            print('nepostojeci izbor')
            break            
def brisanje_hotela_menu():
    zaglavlje_hotele()
    prikaz = HotelIO.ucitavanje_hotela()
    prikaz_hotela(prikaz)
    print("\nIzaberite hotel:")
    choice = input('> ')

    while True:
        if choice == '':
            admin_menu()
        else:
            hotel = dataIO.biranje_elemenata(prikaz, choice , 'id')
            HotelIO.brisanje_hotela(hotel)
            print('Hotel uspesno obrisan')
            time.sleep(1)
            break

def pretraga_recepcionera_menu():
    print("\nIzaberite opciju:")
    print('1. Pretraga po jednom kriterijumu')
    print('2. Pretraga po vise kriterijuma')
    print('0. Nazad')
    choice = input('> ')
    
    while True:
        if choice == '1':
            pretraga_po_kriterijumu_recepcioneri_menu()
        elif choice == '2':
            ime = input('Unesite ime:')
            prezime = input('Unesite prezime:')
            kor_ime = input('Unesite korisnicko ime:')
            email = input('Unesite e-mail:')
            sifra_hotela = input('Sifra hotela u kome radi:')
            
            prikaz = usersIO.pretraga_recepcionera_po_vise_kriterijuma(ime , prezime , kor_ime , email ,sifra_hotela)

            zaglavlje_recepcioneri()
            prikaz_recepcionera(prikaz)
            time.sleep(1) 
            break
        elif choice == '0':
            admin_menu()
        else:
            print('nepostojeci izbor')
            break

def pretraga_po_kriterijumu_recepcioneri_menu():
    print("\nIzaberite opciju:")
    print('1. Pretraga po imenu')
    print('2. Pretraga po prezimenu')
    print('3. Pretraga po korisnickom imenu')
    print('4. Pretraga po e-mail adresi')
    print('5. Pretraga po radnom mestu')
    print('0. Nazad')

    choice = input('> ')

    while True:
        if choice == '1':
            ime = input('Unesite ime:')
            prikaz = usersIO.pretraga_recepcionera_po_imenu(ime)
            zaglavlje_recepcioneri()
            prikaz_recepcionera(prikaz)
            time.sleep(1) 
            break
        elif choice == '2':
            prezime = input('Unesite prezime:')
            prikaz = usersIO.pretraga_recepcionera_po_prezimenu(prezime)
            zaglavlje_recepcioneri()
            prikaz_recepcionera(prikaz)
            time.sleep(1) 
            break
        elif choice == '3':
            kor_ime = input('Unesite korisnicko ime:')
            prikaz = usersIO.pretraga_recepcionera_po_korisinickom_imenu(kor_ime)
            zaglavlje_recepcioneri()
            prikaz_recepcionera(prikaz)
            time.sleep(1) 
            break
        elif choice == '4':
            emai = input('Unesite e-mail:')
            prikaz = usersIO.pretraga_recepcionera_po_email(emai)
            zaglavlje_recepcioneri()
            prikaz_recepcionera(prikaz)
            time.sleep(1) 
            break
        elif choice == '5':
            id_hotela = input('Sifra hotela u kojem radi:')
            prikaz = usersIO.pretraga_recepcionera_po_hotelu(id_hotela)
            zaglavlje_recepcioneri()
            prikaz_recepcionera(prikaz)
            time.sleep(1) 
            break
        elif choice == '0':
            pretraga_recepcionera_menu()


def recepcioner_menu():
    print("\nIzaberite opciju:")
    print('1. Pretraga soba')
    print('2. Pretraga rezervacija ')
    print('3. Izveštaj')
    print('0. Odjavi se')

    choice = input('> ')
    while  True:
        if choice == '1':
            pretraga_soba_menu()
        elif choice == '2':
            pretraga_rezervacija_menu()
        elif choice == '3':
            izvestaj_menu()
        elif choice == '0':
            promenjive.korisnik = {}
            main()


def pretraga_soba_menu():
    print("\nIzaberite opciju:")
    print('1. Pretraga jednom kriterijumu ')
    print('2. Pretraga vise kriterijuma ')
    print('0. Nazad')

    choice = input('> ')
    while True:
        if choice == '1':
            pretraga_po_kriterijumu_soba()
        elif choice == '2':
            datum_prijave = input("Od kog datuma vam treba soba:")
            datum_odjave = input("Do kog datuma vam treba soba:")
            id = promenjive.korisnik['sifra_hotela']  
            broj_sobe = input("Unesite broj sobe:")
            broj_kreveta = input("Unesite broj kreveta:")
            tip = input("Unesite tip sobe:")
            tv = input("Da li ima TV:")
            klima = input("Da li ima klimu:")
            cena = input("Unesite minimalnu cenu:")
            prikaz = reservation.pretraga_soba_po_vise_kriterijuma(datum_odjave,datum_prijave,broj_sobe , broj_kreveta , tip , klima ,tv , cena, id )
            zaglavlje_sobe()
            prikaz_soba(prikaz)
            time.sleep(1) 
            break        
        elif choice == '0':
            recepcioner_menu()

def pretraga_po_kriterijumu_soba():
    id_hotela = promenjive.korisnik['sifra_hotela']
    print("\nIzaberite opciju:")
    print('1. Pretraga po broju sobe')
    print('2. Pretraga po broju kreveta')
    print('3. Pretraga po tipu')
    print('4. Da li ima TV')
    print('5. Da li ima Klimu')
    print('6. Pretraga po ceni')
    print('7. Pretraga po dostupnosti:')
    print('0. Nazad')

    choice = input('> ')
    while True:
        if choice == '1':
            broj_sobe = input("Unesite broj sobe:")
            zaglavlje_sobe()
            prikaz = reservation.pretraga_soba_po_broju(broj_sobe,id_hotela)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice =='2':
            broj_kreveta = input("Unesite broj kreveta:")
            zaglavlje_sobe()
            prikaz = reservation.pretraga_soba_po_broju_kreveta(broj_kreveta,id_hotela)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice == '3':
            tip = input("Unesite tip sobe:")
            zaglavlje_sobe()
            prikaz = reservation.pretraga_soba_po_tipu(tip,id_hotela)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice == '4':
            tv = input("Da li ima TV:")
            zaglavlje_sobe()
            prikaz = reservation.pretraga_soba_po_broju(tv,id_hotela)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice == '5':
            klima = input("Da li ima klimu:")
            zaglavlje_sobe()
            prikaz = reservation.pretraga_soba_po_broju(klima,id_hotela)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice == '6':
            cena = input("Unesite minimalnu cenu:")
            zaglavlje_sobe()
            prikaz = reservation.pretraga_soba_po_broju(cena,id_hotela)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice == '7':
            datum_prijave = input("Od kog datuma vam treba soba:")
            datum_odjave = input("Do kog datuma vam treba soba:")
            id = promenjive.korisnik['sifra_hotela']
            zaglavlje_sobe()
            prikaz = reservation.slobodne_sobe(id,datum_prijave,datum_odjave)
            prikaz_soba(prikaz)
            time.sleep(1) 
            break
        elif choice =='0':
            pretraga_soba_menu()
   

def pretraga_rezervacija_menu():
    print("\nIzaberite opciju:")
    print('1. Pretraga jednom kriterijumu ')
    print('2. Pretraga vise kriterijuma ')
    print('0. Nazad')

    choice = input('> ')
    id = promenjive.korisnik['sifra_hotela']

    while True:
        if choice == '1':
            pretraga_po_kriterijumu_rezervacija()
        elif choice == '2':
            datum_kreiranja = input('Unesite datum kreiranja:')
            datum_prijave = input('Unesite datum prijave:')
            datum_odjave = input('Unesite datum odjave:')
            korisnik = input('Unesite korisnika:')
            status = input('Unesite stauts:')
            prikaz = reservation.pretraga_po_vise_kriterijuma_rezervacije(id,datum_kreiranja , datum_prijave,datum_odjave,korisnik,status)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1)
            break
        elif choice == '0':
            recepcioner_menu()

def pretraga_po_kriterijumu_rezervacija():
    print("\nIzaberite opciju:")
    print('1. Pretraga po datumu kreiranja rezervacije')
    print('2. Pretraga po datumu prijave')
    print('3. Pretraga po datumu odjave')
    print('4. Pretraga po korisniku')
    print('5. Pretraga po statusu rezervacije')
    print('0. Nazad')

    choice = input('> ')
    id = promenjive.korisnik['sifra_hotela']
    while True:
        if choice == '1':
            datum = input('Unesite datum kreiranja:')
            prikaz = reservation. pretraga_po_datumu_kreiranja(id,datum)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1)
            break
        elif choice =='2':
            datum = input('Unesite datum prijave:')
            prikaz = reservation. pretraga_po_datumu_prijave(id,datum)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1)
            break
        elif choice == '3':
            datum = input('Unesite datum odjave:')
            prikaz = reservation. pretraga_po_datumu_odjave(id,datum)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1)
            break
        elif choice == '4':
            korisnik = input('Unesite korisnika:')
            prikaz = reservation. pretraga_po_korinsiku(id,korisnik)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1)
            break
        elif choice == '5':
            status = input('Unesite stauts:')
            prikaz = reservation. pretraga_po_statusu(id,status)
            zaglavlje_rezervacije()
            prikaz_rezervacija(prikaz)
            time.sleep(1)
            break
        elif choice =='0':
            pretraga_rezervacija_menu()

            
def izvestaj_menu():
    print("\nIzaberite opciju:")
    print('1. Dnevni izvestaj')
    print('2. Nedeljni izvestaj')
    print('3. Mesecni izvestaj')
    print('0. Nazad')

    choice = input('> ')
    id_hotela = promenjive.korisnik['sifra_hotela']
    while True:
        if choice == '1':
                prikaz = reservation.dnevni_izvestaj(id_hotela)
                print('Lista rezervisanih soba:')
                zaglavlje_sobe()
                prikaz_soba(prikaz['Lista rezervisanih soba'])
                zagalvlje_izvestaj()
                prikaz_izvestaja(prikaz)
                time.sleep(1)
                break
        elif choice =='2':
                prikaz = reservation.nedeljni_izvestaj(id_hotela)
                print('Lista rezervisanih soba:')
                zaglavlje_sobe()
                prikaz_soba(prikaz['Lista rezervisanih soba'])
                zagalvlje_izvestaj()
                prikaz_izvestaja(prikaz)
                time.sleep(1)
                break
        elif choice == '3':
                prikaz = reservation.mesecni_izvestaj(id_hotela)
                print('Lista rezervisanih soba:')
                zaglavlje_sobe()
                prikaz_soba(prikaz['Lista rezervisanih soba'])
                zagalvlje_izvestaj()
                prikaz_izvestaja(prikaz)
                time.sleep(1)
                break
        elif choice == '0':
                admin_menu()
        else:
                print("neispravan izbor!")
                admin_menu()

def zaglavlje_hotele():
    print('\n')
    print('  Naziv hotela:           | Adresa:                     | Da li ima restoran: | Da li ima bazen: | Prosečna ocena:')
    print('--------------------------+-----------------------------+---------------------+------------------+----------------')

def prikaz_hotela(hoteli):
    red_broj = 0
    for hotel in hoteli:
        if hotel:
            red_broj += 1
            print(str(red_broj) + ')' + hotel['Naziv'].rjust(24)+'|'+hotel['Adresa'][:29].ljust(29)+'|'+hotel['Restoran'][:21].ljust(21)+'|'+hotel['Bazen'][:18].ljust(18)+'|'+hotel['Ocena'])

def zaglavlje_recepcioneri():
    print('\n')
    print('Ime:            | Prezime:           | Korisnicko ime: | E-mail adresa:    | Hotel u kome je zaposlen:')
    print('----------------+--------------------+-----------------+-------------------+--------------------------')

def prikaz_recepcionera(recepcioneri):
    red_broj = 0
    for recepcioner in recepcioneri:
        if recepcioner:
            red_broj += 1
            print(str(red_broj) + ')' + recepcioner['ime'].rjust(14) + '|' + recepcioner['prezime'][:20].ljust(20)+ '|' + recepcioner['korisnicko_ime'][:17].ljust(17) + '|'  + recepcioner['email'][:19].ljust(19) + '|' + recepcioner['sifra_hotela'][:26].ljust(26))

def zaglavlje_sobe():
    print('\n')
    print('Red. broj:  Id sobe:| Broj sobe:     | Broj kreveta:  | Da li ima klimu: | Da li ima TV: |  Tip sobe:     | Cena za nocenje: ')
    print('--------------------+----------------+----------------+------------------+---------------+----------------+------------------')

def prikaz_soba(sobe):
    red_broj = 0
    for soba in sobe:
        red_broj += 1
        if red_broj < 10:
            print(str(red_broj) + ')' + soba['id'].rjust(18) + '|' + soba['Broj sobe'][:16].ljust(16)+ '|' + soba['Broj kreveta'][:16].ljust(16) + '|'  + soba['Klima'][:18].ljust(18) + '|' + soba['TV'][:15].ljust(15)+ '|'  + soba['Tip'][:16].ljust(16) + '|'  + soba['Cena'][:17].ljust(17))
        else:
            print(str(red_broj) + ')' + soba['id'].rjust(17) + '|' + soba['Broj sobe'][:16].ljust(16)+ '|' + soba['Broj kreveta'][:16].ljust(16) + '|'  + soba['Klima'][:18].ljust(18) + '|' + soba['TV'][:15].ljust(15)+ '|'  + soba['Tip'][:16].ljust(16) + '|'  + soba['Cena'][:17].ljust(17))

def zaglavlje_rezervacije():
    print('\n')
    print('Id rezervacije: | Rezervisane sobe:  | Datum  kreiranja:          | Datum prijave:   | Datum odjave:    |  Korisnik:     | Status rezervacije: ')
    print('----------------+--------------------+----------------------------+------------------+------------------+----------------+---------------------')

def prikaz_rezervacija(lista):
    for rezervacija in lista:
        print(rezervacija['id'].rjust(16) + '|' + rezervacija['Lista rezervisanih soba'][:20].ljust(20)+ '|' + rezervacija['Datum kreiranja'][:28].ljust(28)+ '|' + rezervacija['Datum prijave'][:18].ljust(18)+ '|' + rezervacija['Datum odjave'][:18].ljust(18)+ '|' + rezervacija['Korisnik'][:16].ljust(16)+ '|' + rezervacija['Status rezervacije'][:21].ljust(21))

def zagalvlje_izvestaj():
    print('\n')
    print('  Broj realizovanih rezervacija:| Broj izdatih soba: | Ukupna zarada:  | Prosecna ocena: ')
    print('--------------------------------+--------------------+-----------------+-----------------')

def prikaz_izvestaja(izvestaj):
    print(str(izvestaj['Broj rezervacija']).rjust(16) +'                '+ '|' + str(izvestaj['Broj izdatih soba'])[:20].ljust(20)+ '|' +str(izvestaj['Ukupna zarada'])[:17].ljust(17)+ '|' + str(izvestaj['Prosecna ocena'])[:17].ljust(17))

main()