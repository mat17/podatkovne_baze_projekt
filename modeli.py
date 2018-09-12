import sqlite3
import csv
import datetime

danes = datetime.datetime.now()

BAZA = "ppt.db"
con = sqlite3.connect(BAZA)
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")



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
        JOIN Sezona ON (Sezona.id = Tekmovanja.id_sezona)
        ORDER BY Sezona.leto, Tekmovanja.kraj''')
    return cur.fetchall()

def vseKategorije():
    '''Vrne seznam kategorij.'''
    cur.execute('''
        SELECT *
        FROM Kategorije''')
    return cur.fetchall()

def podatki_ime_priimek(ime, priimek):
    '''Za neko ime in priimek vrne klub, v katerega je včlanjen tekmovalec'''
    cur.execute('''
        SELECT id,
        FROM Tekmovalci
        WHERE ime = ? AND PRIIMEK = ?''',
                (ime, priimek))
    return cur.fetchone()

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
    

def starostTekmovalca(idTekmovalca, idTekme):
    '''Vrne starost tekmovalca na dan tekme.'''
    datum = datumTekme(idTekme)
    datum_leto = int(datum[0])
    datum_mesec = int(datum[1])
    datum_dan = int(datum[2])
    rojstni = rojstniDan(idTekmovalca)
    rojstni_leto = int(rojstni[0])
    rojstni_mesec = int(rojstni[1])
    rojstni_dan = int(rojstni[2])
    return datum_leto - rojstni_leto - ((datum_mesec, datum_dan) < (rojstni_mesec, rojstni_dan))

def kategorijaTekmovalca(idTekmovalca, idTekme):
    '''Vrne kategorijo, v kateri nastopa tekmovalec glede na svojo starost na dan tekme.'''
    starost = starostTekmovalca(idTekmovalca, idTekme)
    kategorije = vseKategorije()
    for a,b,c in vseKategorije():
        if b <= starost and starost <= c:
            return a
    



    
