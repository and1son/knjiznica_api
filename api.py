from flask import Flask, jsonify, request
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()


app.config['MYQSL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'andibasic'
app.config['MYSQL_DATABASE_DB'] = 'knjiznica'
app.config['MYASQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/knjiga', methods=["GET"])
def sve_knjige_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knjiga")
    knjiga = cursor.fetchall()
    conn.commit()
    return jsonify({'knjiga' : knjiga})

@app.route('/knjiga/<sifra>', methods=["GET"])
def jedna_knjiga_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    knjiga = cursor.execute("SELECT * FROM knjiga where sifra = %s", sifra)
    knjiga = cursor.fetchone()
    return jsonify({'knjiga' : knjiga})

@app.route('/knjiga', methods=["POST"])
def dodavanje_knjige():
    naslov = request.json.get('Naslov', None)
    zanr = request.json.get('Zanr', None)
    autor = request.json.get('Autor', None)
    nakladnik = request.json.get('nakladnik', None)
    izdavanje = request.json.get('izdavanje', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO knjiga (Naslov,Zanr,Autor,nakladnik,izdavanje) VALUES (%s,%s,%s,%s,%s)", (naslov,zanr,autor,nakladnik,izdavanje))
    conn.commit()
    return ("Nova knjiga dodana")

@app.route('/knjiga/<sifra>', methods=["PUT"])
def edit_knjige(sifra):
    naslov = request.json.get('Naslov', None)
    zanr = request.json.get('Zanr', None)
    autor = request.json.get('Autor', None)
    nakladnik = request.json.get('nakladnik', None)
    izdavanje = request.json.get('izdavanje', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE knjiga SET Naslov=%s, Zanr=%s, Autor=%s, nakladnik=%s, izdavanje=%s WHERE sifra =%s", (naslov, zanr, autor, nakladnik, izdavanje, sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify("Knjiga je uređena")

@app.route('/knjiga/<sifra>', methods=["DELETE"])
def brisanje_knjige(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM knjiga WHERE sifra=%s", sifra)
    conn.commit()
    return ("Knjiga je obrisana")

@app.route('/izdavatelj', methods=["GET"])
def svi_izdavatelji_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM izdavatelj")
    izdavatelj = cursor.fetchall()
    conn.commit()
    return jsonify({'izdavatelji' : izdavatelj})

@app.route('/izdavatelj/<sifra>', methods=["GET"])
def jedan_izdavatelj_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavatelj = cursor.execute("SELECT * FROM izdavatelj where sifra = %s", sifra)
    izdavatelj = cursor.fetchone()
    return jsonify({'izdavatelj' : izdavatelj})

@app.route('/izdavatelj', methods=["POST"])
def dodavanje_izdavitelj():
    ime = request.json.get('Ime', None)
    prezime = request.json.get('Prezime', None)
    adresa = request.json.get('Adresa', None)
    mjesto = request.json.get('Mjesto', None)
    postanski_broj = request.json.get('Postanski_broj', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO izdavatelj (Ime, Prezime, Adresa, Mjesto, Postanski_broj) VALUES (%s,%s,%s,%s,%s)", (ime,prezime,adresa,mjesto,postanski_broj))
    conn.commit()
    return ("Novi izdavatelj dodan")

@app.route('/izdavatelj/<sifra>', methods=["PUT"])
def edit_izdavatelj(sifra):
    ime = request.json.get('Ime', None)
    prezime = request.json.get('Prezime', None)
    adresa = request.json.get('Adresa', None)
    mjesto = request.json.get('Mjesto', None)
    postanski_broj = request.json.get('Postanski_broj', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE izdavatelj SET Ime=%s, Prezime=%s, Adresa=%s, Mjesto=%s, Postanski_broj=%s WHERE sifra =%s", (ime,prezime,adresa,mjesto,postanski_broj,sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify("Izdavatelj je uređen")

@app.route('/izdavatelj/<sifra>', methods=["DELETE"])
def brisanje_izdavatejl(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM izdavatelj WHERE sifra=%s", sifra)
    conn.commit()
    return ("Izdavatelj je obrisan")

@app.route('/nakladnik', methods=["GET"])
def svi_nakladnici_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nakladnik")
    nakladnik = cursor.fetchall()
    conn.commit()
    return jsonify({'nakladnici' : nakladnik})

@app.route('/nakladnik/<sifra>', methods=["GET"])
def jedan_nakladnik_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    nakladnik = cursor.execute("SELECT * FROM nakladnik where sifra = %s", sifra)
    nakladnik = cursor.fetchone()
    return jsonify({'nakladnici' : nakladnik})

@app.route('/nakladnik', methods=["POST"])
def dodavanje_nakladnik():
    naziv = request.json.get('Naziv', None)
    mjesto = request.json.get('Mjesto', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nakladnik (Naziv, Mjesto) VALUES (%s,%s)", (naziv,mjesto))
    conn.commit()
    return ("Novi nakladnik dodan")

@app.route('/nakladnik/<sifra>', methods=["PUT"])
def edit_nakladnik(sifra):
    naziv = request.json.get('Naziv', None)
    mjesto = request.json.get('Mjesto', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE nakladnik SET Naziv=%s, Mjesto=%s WHERE sifra =%s", (naziv,mjesto,sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify("Nakladnik je uređen")

@app.route('/nakladnik/<sifra>', methods=["DELETE"])
def brisanje_nakladnik(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nakladnik WHERE sifra=%s", sifra)
    conn.commit()
    return ("nakladnik je obrisan")

@app.route('/izdavanje', methods=["GET"])
def sva_izdavanja_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM izdavanje")
    izdavanje = cursor.fetchall()
    conn.commit()
    return jsonify({'nakladnici' : izdavanje})

@app.route('/izdavanje/<sifra>', methods=["GET"])
def jedno_izdavanje_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavanje = cursor.execute("SELECT * FROM izdavanje where sifra = %s", sifra)
    izdavanje = cursor.fetchone()
    return jsonify({'izdavanje' : izdavanje})

@app.route('/izdavanje', methods=["POST"])
def dodavanje_izdavanje():
    datum_izdavanja = request.json.get('datum_izdavanja', None)
    datum_povratka = request.json.get('datum_povratka', None)
    cijena = request.json.get('cijena', None)
    izdavatelj = request.json.get('izdavatelj', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO izdavanje (datum_izdavanja, datum_povratka, cijena, izdavatelj) VALUES (%s,%s,%s,%s)", (datum_izdavanja,datum_povratka,cijena,izdavatelj))
    conn.commit()
    return ("Novo izdavanje dodano")

@app.route('/izdavanje/<sifra>', methods=["PUT"])
def edit_izdavanje(sifra):
    datum_izdavanja = request.json.get('datum_izdavanja', None)
    datum_povratka = request.json.get('datum_povratka', None)
    cijena = request.json.get('cijena', None)
    izdavatelj = request.json.get('izdavatelj', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE izdavanje SET datum_izdavanja=%s, datum_povratka=%s cijena=%s, izdavatelj=%s WHERE sifra =%s", (datum_izdavanja,datum_povratka,cijena,izdavatelj,sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify("Nakladnik je uređen")

@app.route('/izdavanje/<sifra>', methods=["DELETE"])
def brisanje_izdavanje(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM izdavanje WHERE sifra=%s", sifra)
    conn.commit()
    return ("Izdavanje je obrisano")



if __name__ == '__main__':
    app.run(debug=True)