import sqlite3
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
        SELECT *
        FROM Tekmovanja
        ''')
    return cur.fetchall()

def vseKategorije():
    '''Vrne seznam kategorij.'''
    cur.execute('''
        SELECT *
        FROM Kategorije''')
    return cur.fetchall()


def vseSezone():
    '''Vrne seznam vseh sezon, ki so vodene v evidenci.'''
    cur.execute('''
        SELECT *
        FROM Sezona
        ''')
    return cur.fetchall()

def vseTekmeVSezoni(indeks):
    '''Vrne seznam vseh tekem v sezoni.'''
    cur.execute('''
        SELECT *
        FROM Tekmovanja 
        WHERE id_sezona = ?
        ''',
                (indeks,))
    return cur.fetchall()

##def vsiRezultati():
##    '''Vrne vse rezultate.'''
##    cur.execute('''
##        SELECT *
##        FROM Rezultati''')
##    return cur.fetchall()

def podatkiTekmovalec(ime, priimek):
    '''Za neko ime in priimek vrne podatke o tekmovalcu.'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci
        WHERE LOWER(ime) = LOWER(?) AND LOWER(priimek) = LOWER(?)''',
                (ime, priimek))
    return cur.fetchone()

def isciPodatkiTekmovalec(ime, priimek):
    '''Naredimo poizvedbo o tekmovalcih. Ne vemo točnega imena / priimka.'''
    ime = '%' + ime + '%'
    priimek = '%' + priimek + '%'
    cur.execute('''
        SELECT ime, priimek, rojstni
        FROM Tekmovalci
        WHERE ime LIKE ? AND priimek LIKE ?''',
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

def imeInPriimek(indeks):
    '''Za nek indeks vrne ime in priimek.'''
    cur.execute('''
        SELECT ime, priimek
        FROM Tekmovalci
        WHERE id = ?''',
                (indeks,))
    imepriimek = cur.fetchone()
    return str(imepriimek[0]) +" "+ str(imepriimek[1])

def rojstniDan(indeks):
    '''Za id tekmovalca vrne njegov rojstni datum.'''
    cur.execute('''
        SELECT rojstni
        FROM Tekmovalci
        WHERE id = ?''',
                (indeks,))
    return cur.fetchone()[0].split('-')

def isciIDTekme(kraj, dolzina, leto):
    '''Za podan kraj, dolžino in leto poiščemo ustrezen indeks tekme.'''
    # naredimo case insensitive poizvedbo z LOWER
    cur.execute('''
        SELECT Tekmovanja.id
        FROM Tekmovanja
        JOIN Sezona ON (Sezona.id = Tekmovanja.id_sezona)
        WHERE LOWER(Tekmovanja.kraj) = LOWER(?) AND Tekmovanja.dolzina = ? AND Sezona.leto = ?''',
                (kraj, dolzina, leto, ))
    vrni = cur.fetchone()
    if vrni == None:
        return None
    else:
        return vrni[0]


def vsiRezultatiTekmovanja(indeks):
    '''Poisce vse rezultate dosezene na tem tekmovanju'''
    cur.execute('''
      SELECT Lestvica.id_kategorija, Rezultati.čas, Tekmovalci.ime, Tekmovalci.priimek
      FROM Rezultati
      JOIN Tekmovanja ON (Tekmovanja.id = Rezultati.id_tekmovanje)
      JOIN Tekmovalci ON (Tekmovalci.id = Rezultati.id_tekmovalec)
      JOIN Lestvica ON (Lestvica.id_tekmovalec = Tekmovalci.id AND Lestvica.id_sezona = Tekmovanja.id_sezona)
      WHERE Rezultati.id_tekmovanje = ?
      ORDER BY Rezultati.čas''',
                (indeks,))
    return cur.fetchall()

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
    indeks = cur.fetchone()
    if indeks == None:
        return None
    else:
        return indeks[0]

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

def poisciTekmovalcaNaLestvici(id_sezona, id_tekmovalec):
    '''Poišče vse podatke o tekmovalcu na lestvici.'''
    cur.execute('''
        SELECT *
        FROM Lestvica
        WHERE id_sezona = ? AND id_tekmovalec = ?''',
                (id_sezona, id_tekmovalec))
    return cur.fetchone()

def poglejLestvicoVKategoriji(leto, id_kategorija):
    '''Za dano sezono in kategorijo nam vrne uvrstitve na lestvici v kategoriji.'''
    id_sezona = indeksSezone(leto)
    cur.execute('''
        SELECT Lestvica.uvrstitev_v_kategoriji, Tekmovalci.ime, Tekmovalci.priimek, Lestvica.st_tock_kategorija
        FROM Lestvica
        JOIN Tekmovalci ON (Tekmovalci.id = Lestvica.id_tekmovalec)
        WHERE Lestvica.id_sezona = ? AND Lestvica.id_kategorija = ?
        ORDER BY Lestvica.uvrstitev_v_kategoriji''',
                (id_sezona, id_kategorija))
    return cur.fetchall()

def poglejLestvicoSkupno(leto):
    '''Za dano sezono nam vrne lestvico.'''
    id_sezona = indeksSezone(leto)
    cur.execute('''
        SELECT Lestvica.uvrstitev_skupno, Tekmovalci.ime, Tekmovalci.priimek, Lestvica.st_tock_skupno
        FROM Lestvica
        JOIN Tekmovalci ON (Tekmovalci.id = Lestvica.id_tekmovalec)
        WHERE Lestvica.id_sezona = ?
        ORDER BY Lestvica.uvrstitev_skupno''',
                (id_sezona,))
    return cur.fetchall()

#uvrstitveTekmovalcaVSezoni(idTekmovalca,idSezone) + casiTekmovalca
def casiInUvrstitve(idTekmovalca, idSezone):
    casi = casiTekmovalca(idTekmovalca, idSezone)
    uvrstitve = uvrstitveTekmovalcaVSezoni(idTekmovalca,idSezone)
    vrni = []
    i = 0
    while i < len(casi):
        tekmovalec = []
        for j in casi[i]:
            tekmovalec.append(j)
        for j in uvrstitve[i]:
            tekmovalec.append(j)
        vrni.append(tekmovalec)
        i += 1
    return vrni

############ DODAJANJE ######################

def dodajTekmovalca(ime, priimek, rd, spol, klub):
    '''Dodamo tekmovalca v bazo.'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci
        WHERE ime = ? AND priimek = ? AND rojstni = ?''',
                (ime, priimek, rd))
    preveri = cur.fetchone()
    if preveri != None:
        return None
    else:
        cur.execute('''
            INSERT INTO Tekmovalci (ime, priimek, rojstni, spol, klub)
            VALUES (?, ?, ?, ?, ?)''', (ime, priimek, rd, spol, klub))
        con.commit()

def posodobiTekmovalca(indeks, ime, priimek, rd, spol, klub):
    '''Popravimo podatke o tekmovalcu'''
    cur.execute('''
        UPDATE Tekmovalci
        SET ime = ?, priimek = ?, rojstni = ?, spol = ?, klub = ?
        WHERE id = ?''',
                (ime, priimek, rd, spol, klub, indeks))
    con.commit()

def dodajTekmovanje(kraj, datum, dolzina):
    '''Dodamo tekmovanje v bazo. Datum naj bo oblike 'leto-mm-dd'.'''
    leto = datum.split('-')[0]
    id_sezone = indeksSezone(leto)
    cur.execute('''
        INSERT INTO Tekmovanja (id_sezona, kraj, datum, dolzina)
        VALUES (?, ?, ?, ?)''',
                (id_sezone, kraj, datum, dolzina))
    con.commit()

def posodobiTekmovanje(indeks, kraj, datum, dolzina):
    '''Popravimo podatke o tekmovanju.'''
    cur.execute('''
        UPDATE Tekmovanja
        SET kraj = ?, datum = ?, dolzina = ?
        WHERE id = ?''',
                (kraj, datum, dolzina, indeks))
    con.commit()

def dodajRezultatID(id_tekmovalec, id_tekmovanje, cas):
    '''Dodamo dosežek nekega tekmovalca na neki tekmi v bazo. Vemo ID tekme in ID tekmovalca'''
    cur.execute('''
        INSERT INTO Rezultati (id_tekmovalec, id_tekmovanje, čas)
        VALUES (?, ?, ?)''',
                (id_tekmovalec, id_tekmovanje, cas))
    con.commit()

def dodajRezultatOpisno(ime, priimek, kraj, dolzina, leto, cas):
    id_tekmovalec = podatkiTekmovalec(ime, priimek)
    idTekmovanje = isciIDTekme(kraj, dolzina, leto)
    dodajRezultatID(id_tekmovalec, idTekmovanje, cas)

def dodajSezono(leto):
    '''Dodamo novo sezono.'''
    if indeksSezone(leto) == None:
        cur.execute('''
            INSERT INTO Sezona (leto)
            VALUES (?)''',
                    (leto,))
        con.commit()

def dodajTekmovalcaNaLestvico(id_sezona, id_tekmovalec):
    '''Dodamo novega tekmovalca na lestvico.'''
    if poisciTekmovalcaNaLestvici(id_sezona, id_tekmovalec) == None:
        id_kategorija = kategorijaTekmovalca(id_tekmovalec, id_sezona)
        cur.execute('''
            INSERT INTO Lestvica (id_sezona, id_tekmovalec, id_kategorija, st_tock_skupno, st_tock_kategorija)
            VALUES (?, ?, ?, ?, ?)''',
                    (id_sezona, id_tekmovalec, id_kategorija, 0, 0))
        con.commit()

def dodajVseTekmovalceNaLestvico():
    '''Doda vse tekmovalce iz baze tekmovalci v tabelo lestvica.'''
    # To bomo potrebovali samo 'prvič', ker je naša tabela 'lestvica' še prazna
    sezone = []
    cur.execute('''
        SELECT id
        FROM Sezona''')
    for i in cur.fetchall():
        sezone.append(i[0])
    indeksi = []
    cur.execute('''
        SELECT id
        FROM Tekmovalci''')
    for i in cur.fetchall():
        indeksi.append(i[0])
    for j in sezone:
        for i in indeksi:
            dodajTekmovalcaNaLestvico(j,i)

def posodobiTocke(id_tekmovalca, id_sezone):
    '''Posodobimo število točk nekega tekmovalca na lestvici.'''
    tocke_v_sezoni = dosezeneTockeTekmovalcaVSezoni(id_tekmovalca, id_sezone)
    cur.execute('''
        UPDATE Lestvica
        SET st_tock_skupno = ?, st_tock_kategorija = ?
        WHERE id_sezona = ? AND id_tekmovalec = ?''',
                (tocke_v_sezoni[0],tocke_v_sezoni[1],id_sezone,id_tekmovalca))
    con.commit()

# ta ukaz lahko zaženemo po vsaki tekmi.
# bolje bi bilo, da bi imeli v tabeli še stolpec 'zadnja posodobitev'
# in bi tako vedeli, da moramo od določene tekme naprej le dodati rezultate
# prednost našega načina pa je ta, da so vsi podatki v sezoni zagotovo posodobljeni
def posodobiVseTockeVSezoni(leto):
    id_sezona = indeksSezone(leto)
    tekmovalci = []
    cur.execute('''
        SELECT id_tekmovalec
        FROM Lestvica
        WHERE id_sezona = ?''',
                (id_sezona,))
    for i in cur.fetchall():
        tekmovalci.append(i[0])
    for i in tekmovalci:
        posodobiTocke(i, id_sezona)

def posodobiUvrstitveKategorija(leto):
    id_sezona = indeksSezone(leto)
    kategorije = []
    cur.execute('''
        SELECT id_kategorija
        FROM Lestvica
        WHERE id_sezona = ?''',
                (id_sezona,))
    for i in cur.fetchall():
        kategorije.append(i[0])
    kategorije = list(set(kategorije))
    for kat in kategorije:
        cur.execute('''
            SELECT id_tekmovalec, st_tock_kategorija
            FROM Lestvica
            WHERE id_sezona = ? AND id_kategorija = ?
            ORDER BY st_tock_kategorija DESC''',
                    (id_sezona, kat))
        tekmovalci = cur.fetchall()
        i = 0
        for (indeks,_) in tekmovalci:
            uvrstitev_kat = dosezeno_mesto(tekmovalci, i)
            cur.execute('''
                UPDATE Lestvica
                SET uvrstitev_v_kategoriji = ?
                WHERE id_sezona = ? AND id_tekmovalec = ?''',
                        (uvrstitev_kat, id_sezona, indeks))
            con.commit()
            i += 1

def posodobiUvrstitveSkupno(leto):
    id_sezona = indeksSezone(leto)
    cur.execute('''
        SELECT id_tekmovalec, st_tock_skupno
        FROM Lestvica
        WHERE id_sezona = ?
        ORDER BY st_tock_skupno DESC''',
                (id_sezona,))
    tekmovalci = cur.fetchall()
    i = 0
    for (indeks,_) in tekmovalci:
        uvrstitev_skupno = dosezeno_mesto(tekmovalci, i)
        cur.execute('''
            UPDATE Lestvica
            SET uvrstitev_skupno = ?
            WHERE id_sezona = ? AND id_tekmovalec = ?''',
                    (uvrstitev_skupno, id_sezona, indeks))
        con.commit()
        i += 1

# ta ukaz lahko zaženemo po vsaki tekmi.
def posodobiUvrstitve(leto):
    posodobiUvrstitveKategorija(leto)
    posodobiUvrstitveSkupno(leto)


# mogoče bi bilo celo bolj pametno voditi moške in ženske rezultate ločeno
# tako bi bilo lažje narediti skupno točkovanje po spolih
# pa tudi skupno skupno ne bi bilo pretežko
# tudi starostne kategorije ne bi bile odvisne od spolov

# še ena možna rešitev je, da bi tekmovalcu avtomatsko priredil dve kategorije
# pri čemer bi moral ustvarit še dve kategoriji - skupno moško in skupno žensko
