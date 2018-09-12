import sqlite3
import csv
import datetime

danes = datetime.datetime.now()

BAZA = "ppt.db"
con = sqlite3.connect(BAZA)
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")


########## POIZVEDBE ##################


def vsiTekmovalci():
    '''Vrne vse podatke o vseh tekmovalcih.'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci''')
    return cur.fetchall()

def vseTekme():
    '''Vrne seznam vseh tekem, ki so vodene v evidenci.'''
    cur.execute('''
        SELECT Tekmovanja.*, Sezona.leto
        FROM Tekmovanja
        JOIN Sezona ON (Sezona.id = Tekmovanja.id_sezona)
        ORDER BY Sezona.leto, Tekmovanja.kraj''')
    return cur.fetchall()

def vseKategorije():
    '''Vrne seznam kategorij.'''
    cur.execute('''
        SELECT *
        FROM Kategorije''')
    return cur.fetchall()

##def vsiRezultati():
##    '''Vrne vse rezultate.'''
##    cur.execute('''
##        SELECT *
##        FROM Rezultati''')
##    return cur.fetchall()

def podatkiTekmovalec(ime, priimek):
    '''Za neko ime in priimek vrne klub, v katerega je včlanjen tekmovalec'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci
        WHERE ime = ? AND PRIIMEK = ?''',
                (ime, priimek))
    return cur.fetchone()

def isciPodatkiTekmovalec(ime, priimek):
    '''Za neko ime in priimek vrne klub, v katerega je včlanjen tekmovalec'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci
        WHERE ime LIKE ? AND PRIIMEK LIKE ?''',
                (ime, priimek))
    return cur.fetchall()

def tekmovalec_indeks(indeks):
    '''Za nek indeks vrne vse poadtke o tekmovalcu.'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci
        WHERE id = ?''',
                (indeks,))
    return cur.fetchone()

def rojstniDan(indeks):
    '''Za id tekmovalca vrne njegov rojstni datum.'''
    cur.execute('''
        SELECT rojstni
        FROM Tekmovalci
        WHERE id = ?''',
                (indeks,))
    return cur.fetchone()[0].split('-')

##def datumTekme(indeks):
##    '''Za id tekme vrne [leto, mesec, dan] dogodka.'''
##    cur.execute('''
##        SELECT datum
##        FROM Tekmovanja
##        WHERE id = ?''',
##                (indeks,))
##    return cur.fetchone()[0].split('-')

def letoTekme(indeks):
    '''Vrne letnico sezone, v kateri poteka dano tekmovanje.'''
    cur.execute('''
        SELECT Sezona.leto
        FROM Tekmovanja
        JOIN Sezona ON (Sezona.id = Tekmovanja.id_sezona)
        WHERE Tekmovanja.id = ?''',
                (indeks,))
    return cur.fetchone()[0]

def letoSezone(indeks):
    '''Vrne letnico sezone, ki ustreza danemu indeksu.'''
    cur.execute('''
        SELECT leto
        FROM Sezona
        WHERE id = ?''',
                (indeks,))
    return cur.fetchone()[0]

def indeksSezone(letnica):
    '''Za letnico sezone nam vrne indeks, pod katerim to sezono vodimo v evidenci.'''
    cur.execute('''
        SELECT id
        FROM Sezona
        WHERE leto = ?''',
                (letnica,))
    return cur.fetchone()[0]

##def starostTekmovalca(idTekmovalca, idTekme):
##    '''Vrne starost tekmovalca na dan tekme.'''
##    datum = datumTekme(idTekme)
##    datum_leto = int(datum[0])
##    datum_mesec = int(datum[1])
##    datum_dan = int(datum[2])
##    rojstni = rojstniDan(idTekmovalca)
##    rojstni_leto = int(rojstni[0])
##    rojstni_mesec = int(rojstni[1])
##    rojstni_dan = int(rojstni[2])
##    return datum_leto - rojstni_leto - ((datum_mesec, datum_dan) < (rojstni_mesec, rojstni_dan))

def kategorijaTekmovalca(idTekmovalca, datum_leto):
    '''Vrne kategorijo, v kateri nastopa tekmovalec v dani sezoni.'''
    if datum_leto not in range(1900,2201):
            datum_leto = int(letoSezone(datum_leto))
    # datum_mesec = 1, datum_dan = 1 --> gledamo starost, ki jo ima tekmovalec na začetku leta
    rojstni = rojstniDan(idTekmovalca)
    rojstni_leto = int(rojstni[0])
    rojstni_mesec = int(rojstni[1])
    rojstni_dan = int(rojstni[2])
    starost = datum_leto - rojstni_leto - ((1, 1) < (rojstni_mesec, rojstni_dan))
    cur.execute('''
        SELECT spol
        FROM Tekmovalci
        WHERE id = ?''',
                (idTekmovalca,))
    spol = cur.fetchone()[0]
    kategorije = vseKategorije()
    for a,b,c,d,_ in vseKategorije():
        if b <= starost and starost <= c and d == spol:
            return a

def casiTekmovalca(idTekmovalca, idSezone = None):
    '''Vrne vse rezultate tekmovalca ali pa vse rezultate tekmovalca v dani sezoni, če je ta podana.'''
    if idSezone:
        # Funkcijo napišemo tako, da lahko namesto idSezone vstavimo tudi letnico.
        # Predvidevamo, da naše tekmovanje poteka med letoma 1900 in 2200
        # Predvidevamo, da noben indeks nobene sezone ni med 1900 in 2200.
        if idSezone >= 1900 and idSezone <= 2200:
            idSezone = indeksSezone(idSezone)
        cur.execute('''
            SELECT Tekmovanja.datum, Tekmovanja.kraj, Tekmovanja.dolzina, Rezultati.čas
            FROM Rezultati
            JOIN Tekmovanja ON (Tekmovanja.id = Rezultati.id_tekmovanje)
            JOIN Tekmovalci ON (Tekmovalci.id = Rezultati.id_tekmovalec)
            WHERE Rezultati.id_tekmovalec = ? AND Tekmovanja.id_sezona = ?
            ORDER BY Tekmovanja.datum''',
                    (idTekmovalca, idSezone,))
        return cur.fetchall()
    else:
        cur.execute('''
            SELECT Tekmovanja.datum, Tekmovanja.kraj, Tekmovanja.dolzina, Rezultati.čas
            FROM Rezultati
            JOIN Tekmovanja ON (Tekmovanja.id = Rezultati.id_tekmovanje)
            WHERE Rezultati.id_tekmovalec = ?
            ORDER BY Tekmovanja.datum''',
                    (idTekmovalca,))
        return cur.fetchall()

# definiramo funkcijo, ki bo v urejenem seznamu vrnila naso uvrstitev
def dosezeno_mesto(seznam, indeks):
    if indeks == 0:
        return 1
    elif seznam[indeks - 1][1] != seznam[indeks][1]:
        return indeks + 1
    else:
        return dosezeno_mesto(seznam, indeks-1)

def uvrstitevNaTekmi(idTekme):
    '''Vrne seznam tuplov, kjer je prva vrednost uvrstitev, druga pa id tekmovalca.'''
    cur.execute('''
        SELECT id_tekmovalec, čas
        FROM Rezultati
        WHERE id_tekmovanje = ?
        ORDER BY čas''',
                (idTekme,))
    vsi_casi = cur.fetchall()
    print(vsi_casi)
    for i in range(len(vsi_casi)):
        if vsi_casi[i][-1] != vsi_casi[i-1][-1]:
            vsi_casi[i] = (i+1,vsi_casi[i][0],vsi_casi[i][1])
        else:
            vsi_casi[i] = (vsi_casi[i-1][0],vsi_casi[i][0],vsi_casi[i][1])
    for i in range(len(vsi_casi)):
        vsi_casi[i] = (vsi_casi[i][0], vsi_casi[i][1])
    return vsi_casi


def uvrstitevPoKategoriji(idTekme,idKategorije):
    '''Vrne tuple, kjer je prva vrednost id tekmovalca, druga pa njegova uvrstitev'''
    cur.execute('''
        SELECT id_sezona
        FROM Tekmovanja
        WHERE id = ?''',
                (idTekme,))
    id_sezone = cur.fetchone()[0] #id sezone, ki ga rabimo za dolocitev leta tekme
    cur.execute('''
        SELECT leto
        FROM Sezona
        WHERE id = ?''',
                (id_sezone,))
    leto = cur.fetchone()[0] # leto tekme, ki ga rabimo za dolocitev kategorije, v kateri se nahajajo tekmovalci
    cur.execute('''
        SELECT id_tekmovalec, čas
        FROM Rezultati
        WHERE id_tekmovanje = ?
        ORDER BY čas''',
                (idTekme,))
    rezult_tekme = cur.fetchall() # vsi temovalci in njihovi časi v dani tekmi
    i = 0
    while i < len(rezult_tekme):
        if kategorijaTekmovalca(rezult_tekme[i][0],leto) != idKategorije:
            rezult_tekme.remove(rezult_tekme[i])
            i-=1
        i+=1
    # moramo preveriti, da nima 'višje uvrščeni' tekmovalec enakega časa kot mi
    # sicer bi lahko uporabili kar enumerate
    for i in range(len(rezult_tekme)):
        if rezult_tekme[i][-1] != rezult_tekme[i-1][-1]:
            rezult_tekme[i] = (i+1,rezult_tekme[i][0],rezult_tekme[i][1])
        else:
            rezult_tekme[i] = (rezult_tekme[i-1][0],rezult_tekme[i][0],rezult_tekme[i][1])
    for i in range(len(rezult_tekme)):
        rezult_tekme[i] = (rezult_tekme[i][0], rezult_tekme[i][1])
    return rezult_tekme

def uvrstitviTekmovalca(idTekmovalca, idTekme):
    '''Vrne uvrstitev v skupnem seštevku ter uvrstitev v kategoriji nekega tekmovalca.'''
    cur.execute('''
        SELECT id_tekmovalec, čas
        FROM Rezultati
        WHERE id_tekmovanje = ?
        ORDER BY čas''',
                (idTekme,))
    vsi_casi = cur.fetchall()    # seznam vseh tekmovalcev in njihovih casov na tekmi
    # poiscemo naso uvrstitev
    for i in range(len(vsi_casi)):
        if vsi_casi[i][0] == idTekmovalca:
            v_skupnem = dosezeno_mesto(vsi_casi, i) #nasa uvrstitev
            vsi_casi = vsi_casi[:i+1] #skrajsamo seznam, saj nas nadaljevanje ne zanima
            break
    cur.execute('''
        SELECT id_sezona
        FROM Tekmovanja
        WHERE id = ?''',
                (idTekme,))
    id_sezone = cur.fetchone()[0] #id sezone, ki ga rabimo za dolocitev leta tekme
    cur.execute('''
        SELECT leto
        FROM Sezona
        WHERE id = ?''',
                (id_sezone,))
    leto = cur.fetchone()[0] # leto tekme, ki ga rabimo za dolocitev kategorije, v kateri se nahajajo tekmovalci
    idKategorije = kategorijaTekmovalca(vsi_casi[-1][0],leto)
    i = 0
    while i < len(vsi_casi):
        if kategorijaTekmovalca(vsi_casi[i][0],leto) != idKategorije:
            vsi_casi.remove(vsi_casi[i])
            i-=1
        i+=1
    v_kategoriji = dosezeno_mesto(vsi_casi,len(vsi_casi)-1)
    return v_skupnem, v_kategoriji

def uvrstitveTekmovalcaVSezoni(idTekmovalca, idSezone):
    cur.execute('''
        SELECT Tekmovanja.id
        FROM Rezultati
        JOIN Tekmovanja ON (Tekmovanja.id = Rezultati.id_tekmovanje)
        WHERE Tekmovanja.id_sezona = ? AND Rezultati.id_tekmovalec = ?
        ORDER BY datum''',
                (idSezone, idTekmovalca))
    vse_tekme = cur.fetchall()
    for i in range(len(vse_tekme)):
        vse_tekme[i]=vse_tekme[i][0]
    vse_uvrstitve = []
    for indeks in vse_tekme:
        vse_uvrstitve.append(uvrstitviTekmovalca(idTekmovalca, indeks))
    return vse_uvrstitve

def dosezeneTockeTekmovalcaVSezoni(idTekmovalca, idSezone):
    '''Vrne stevilo tock v skupnem sestevku ter v kategoriji v dani sezoni.'''
    tocke_skupno = []
    tocke_kategorija = []
    uvrstitve = uvrstitveTekmovalcaVSezoni(idTekmovalca, idSezone)
    for a,b in uvrstitve:
        cur.execute('''
            SELECT st_tock
            FROM Točkovanje
            WHERE uvrstitev = ?''',
                    (a,))
        tocke = cur.fetchone()
        if tocke == None:
            tocke_skupno.append(0)
        else:
            tocke_skupno.append(tocke[0])
        cur.execute('''
            SELECT st_tock
            FROM Točkovanje
            WHERE uvrstitev = ?''',
                    (b,))
        tocke = cur.fetchone()
        if tocke == None:
            tocke_kategorija.append(0)
        else:
            tocke_kategorija.append(tocke[0])
    return sum(tocke_skupno), sum(tocke_kategorija)

    

############ DODAJANJE ######################

#def dodaj
