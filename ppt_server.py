import modeli
from bottle import *


# Naložimo CSS datoteko
@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')


# Glavni meni
@get('/')
def glavniMenu():
    return template('glavna.html')

@get('/admin')
def glavniMenu():
    return template('admin.html')


#Tekmovalci
@get('/izpis_tekmovalcev')
def izpisTekmovalcev():
    tekmovalci = modeli.vsiTekmovalci()
    return template('izpisTekmovalcev.html', tekmovalci=tekmovalci)

@get('/admin/dodaj_tekmovalca')
def stranDodajTekmovalca():
    '''Prikaže stran za dodajanje novih tekmovalcev.'''
    return template('dodaj_tekmovalca.html')

@post('/admin/nov_tekmovalec')
def dodajTekmovalca():
    ime = request.forms.ime
    priimek = request.forms.priimek
    spol = request.forms.spol
    rojstni = request.forms.rojstni
    klub = request.forms.klub
    try:
        modeli.dodajTekmovalca(ime, priimek, rojstni, spol, klub)
        print(f'Tekmovalec {ime} {priimek} dodan. :)')
    except Exception as e:
        print("Napaka!!!")
        print(e)

@get('/admin/popravi_tekmovalca')
def stranUrediTekmovalca():
    '''Prikaže stran za urejanje podatkov o tekmovalcu.'''
    return template('popravi_tekmovalca.html')

@post('/admin/uredi_tekmovalca')
def posodobiTekmovalca():
    indeks = request.forms.indeks
    ime = request.forms.ime
    priimek = request.forms.priimek
    rojstni = request.forms.rojstni
    spol = request.forms.spol
    klub = request.forms.klub
    try:
        modeli.posodobiTekmovalca(indeks, ime, priimek, rojstni, spol, klub)
        print(f'Tekmovalec {indeks} {ime} {priimek} urejen. :)')
    except Exception as e:
        print("Napaka!!!")
        print(e)


#Tekmovanja
@get('/izpis_tekmovanj')
def izpisTekmovanj():
    tekmovanja = modeli.vseTekme()
    return template('izpis_tekmovanj.html', tekmovanja=tekmovanja)

@get('/admin/dodaj_tekmovanje')
def stranDodajTekmovanje():
    '''Prikaže stran za dodajanje novih tekmovanj.'''
    return template('dodaj_tekmovanje.html')

@post('/admin/novo_tekmovanje')
def dodajTekmovanje():
    kraj = request.forms.kraj
    datum = request.forms.datum
    dolzina = request.forms.dolzina
    try:
        modeli.dodajTekmovanje(kraj, datum, dolzina)
        print(f'Tekmovanje {kraj} {datum} {dolzina} dodano. :)')
    except Exception as e:
        print("Napaka!!!")
        print(e)

@get('/admin/popravi_tekmovanje')
def stranUrediTekmovanje():
    '''Prikaže stran za popravljanje podatkov o tekmovanjih.'''
    return template('popravi_tekmovanje.html')

@post('/admin/uredi_tekmovanje')
def posodobiTekmovanje():
    indeks = request.forms.indeks
    kraj = request.forms.kraj
    datum = request.forms.datum
    dolzina = request.forms.dolzina
    try:
        modeli.posodobiTekmovanje(indeks, kraj, datum, dolzina)
        print(f'Tekmovanje {kraj} {datum} {dolzina} urejeno. :)')
    except Exception as e:
        print("Napaka!!!")
        print(e)


#Rezultati
@get('/admin/dodaj_rezultat')
def stranDodajRezultat():
    '''Prikaže stran za dodajanje novih rezultatov.'''
    return template('dodaj_rezultat.html')

@post('/admin/nov_rezultat')
def dodaj_rezultat():
    id_tekmovalca = request.forms.id_tekmovalca
    id_tekmovanja = request.forms.id_tekmovanja
    cas = request.forms.cas
    try:
        modeli.dodajRezultatID(id_tekmovalca, id_tekmovanja, cas)
        print(f'Rezultat tekmovalca {id_tekmovalca} na tekmi {id_tekmovanja} dodan. :)')
    except Exception as e:
        print("Napaka!!!")
        print(e)

@get('/poisci_rezultat_tekmovalca')
def stranPoisciRezultat():
    tekmovalci = modeli.vsiTekmovalci()
    sezone = modeli.vseSezone()
    return template('poisci_rezultat_tekmovalca.html', sezone=sezone, tekmovalci=tekmovalci)


@post('/poisci_rezultat_tekmovalca/<sezona>')
def stranPoisciRezultat(sezona):
    ''''''
    id_sezone = int(request.forms.leto_sezone)
    id_tekmovalca = int(request.forms.id_tekmovalca)
#    tekme = modeli.vseTekmeVSezoni(id_sezone)
    ime = modeli.imeInPriimek(id_tekmovalca)
    letnica = modeli.letoSezone(id_sezone)
    udelezba = modeli.casiInUvrstitve(id_tekmovalca, id_sezone)
    uvrstitev = modeli.poisciTekmovalcaNaLestvici(id_sezone, id_tekmovalca)
    return template('poisci_rezultat_sezone.html', udelezba=udelezba, id_sezone=id_sezone, uvrstitev=uvrstitev, letnica=letnica, ime=ime)#, tekme=tekme)

@get('/rezultati_tekmovanja')
def stranIzberiRezultatTekmovanj():
    tekme = modeli.vseTekme()
    return template('izberi_rezultat_tekmovanja.html', tekme=tekme)

@post('/rezultati_tekmovanja/<sezona>')
def stranRezultatiTekmovanja(sezona):
    ''''''
    id_tekme = int(request.forms.id_tekmovanja)
    rezultati = modeli.vsiRezultatiTekmovanja(id_tekme)
    return template('rezultati_tekmovanja.html', rezultati=rezultati)

@get('/rezultati_tekmovanja_kategorija')
def stranIzberiRezultateTekmovanjeKategorija():
    tekme = modeli.vseTekme()
    kategorije = modeli.vseKategorije()
    return template('izberi_rezultat_tekmovanja_kategorija.html', tekme=tekme, kategorije=kategorije)

@post('/rezultati_tekmovanja_kategorija/<sezona>')
def stranRezultatiTekmovanja(sezona):
    ''''''
    id_tekme = int(request.forms.id_tekmovanja)
    id_kategorije = int(request.forms.id_kategorije)
    rezultati = modeli.rezultatiTekmovanjaKategorija(id_tekme, id_kategorije)
    return template('rezultati_tekmovanja_kategorija.html', rezultati=rezultati)

# Poženemo strežnik na vhodu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True, debug=True)