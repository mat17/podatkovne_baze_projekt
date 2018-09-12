import sqlite3
import csv
import datetime

danes = datetime.datetime.now()

BAZA = "ppt.db"
con = sqlite3.connect(BAZA)
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")


############### POIZVEDBE ################


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

def podatki_ime_priimek(ime, priimek):
    '''Za neko ime in priimek vrne klub, v katerega je včlanjen tekmovalec'''
    cur.execute('''
        SELECT *
        FROM Tekmovalci
        WHERE ime = ? AND PRIIMEK = ?''',
                (ime, priimek))
    return cur.fetchone()

def isci_podatki_ime_priimek(ime, priimek):
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
        Select klub
        FROM Tekmovalci
        WHERE ime = ? AND PRIIMEK = ?''',
                (ime, priimek))
    return cur.fetchone()

def rojstniDan(indeks):
    '''Za id tekmovalca vrne njegov rojstni datum.'''
    cur.execute('''
        SELECT rojstni
        FROM Tekmovalci
        WHERE id = ?''',
                (indeks,))
    return cur.fetchone()[0].split('-')

def datumTekme(indeks):
    '''Za id tekme vrne [leto, mesec, dan] dogodka.'''
    cur.execute('''
        SELECT datum
        FROM Tekmovanja
        WHERE id = ?''',
                (indeks,))
    return cur.fetchone()[0].split('-')

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

def kategorijaTekmovalca(idTekmovalca, idSezone):
    '''Vrne kategorijo, v kateri nastopa tekmovalec v dani sezoni.'''
    datum_leto = int(letoSezone(idSezone))
# datum_mesec = 1, datum_dan = 1 --> gledamo starost, ki jo ima tekmovalec na začetku leta
    rojstni = rojstniDan(idTekmovalca)
    rojstni_leto = int(rojstni[0])
    rojstni_mesec = int(rojstni[1])
    rojstni_dan = int(rojstni[2])
    starost = datum_leto - rojstni_leto - ((1, 1) < (rojstni_mesec, rojstni_dan))
    kategorije = vseKategorije()
    for a,b,c,_ in vseKategorije():
        if b <= starost and starost <= c:
            return a

def indeksSezone(letnica):
    '''Za letnico sezone nam vrne indeks, pod katerim to sezono vodimo v evidenci.'''
    cur.execute('''
        SELECT id
        FROM Sezona
        WHERE leto = ?''',
                (letnica,))
    return cur.fetchone()[0]

def rezultatiTekmovalca(idTekmovalca, idSezone = None):
    '''Vrne vse rezultate tekmovalca ali pa vse rezultate tekmovalca v dani sezoni, če je ta podana.'''
    if idSezone:
        # Funkcijo napišemo tako, da lahko namesto idSezone vstavimo tudi letnico.
        # Predvidevamo, da naše tekmovanje poteka med letoma 1900 in 2200
        # Predvidevamo, da noben indeks nobene sezone ni med 1900 in 2200.
        if idSezone >= 1900 and idSezone <= 2200:
            idSezone = indeksSezone(idSezone)
        cur.execute('''
            SELECT Tekmovanja.datum, Tekmovanja.kraj, Tekmovanja.dolzina, Rezultati.čas, Rezultati.uvrstitev, Rezultati.uvrstitev_kategorija
            FROM Rezultati
            JOIN Tekmovanja ON (Tekmovanja.id = Rezultati.id_tekmovanje)
            JOIN Tekmovalci ON (Tekmovalci.id = Rezultati.id_tekmovalec)
            WHERE Rezultati.id_tekmovalec = ? AND Tekmovanja.id_sezona = ?
            ORDER BY Tekmovanja.datum''',
                    (idTekmovalca, idSezone,))
        return cur.fetchall()
    else:
        cur.execute('''
            SELECT Tekmovanja.datum, Tekmovanja.kraj, Tekmovanja.dolzina, Rezultati.čas, Rezultati.uvrstitev, rezultati.uvrstitev_kategorija
            FROM Rezultati
            JOIN Tekmovanja ON (Tekmovanja.id = Rezultati.id_tekmovanje)
            WHERE Rezultati.id_tekmovalec = ?
            ORDER BY Tekmovanja.datum''',
                    (idTekmovalca,))
        return cur.fetchall()

def uvrstitveTekmovalca(idTekmovalca, idSezone = None):
    '''Vrne vse uvrstitve tekmovalca ali pa vse uvrstitve tekmovalca v dani sezoni, če je ta podana.'''
    


################ DODAJANJE #####################
