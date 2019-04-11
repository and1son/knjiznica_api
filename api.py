from flask import Flask, jsonify, request, url_for, render_template, json, jsonify
from flaskext.mysql import MySQL
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

app = Flask(__name__)

app.config['MYQSL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'andibasic'
app.config['MYSQL_DATABASE_DB'] = 'knjiznica'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

mysql.init_app(app)

@app.route('/users/register', methods=['POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor()
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    cursor.execute("INSERT INTO users(first_name,last_name,email,password,created) VALUES ('" + 
    str(first_name) + "','" +
    str(last_name) + "','" +
    str(email) + "','" +
    str(password) + "','" +
    str(created) + "')")

    conn.commit()

    result = {
        "first_name" : first_name,
        "last_name" : last_name,
        "email" : email,
        "password" : password,
        "created" : created
    }

    return jsonify({"result" : result})

@app.route('/users/login', methods=['POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""
    
    cursor.execute("SELECT * FROM users where email = '" + str(email) + "'")
    row = cursor.fetchone()

    if bcrypt.check_password_hash(row[4], password):
        access_token = create_access_token(identity = {'first_name': row[1],'last_name': row[2],'email': row[3]})
        result = jsonify({"token": access_token})
    else:
        result = jsonify({"error":"Invalid username and password"})

    return result

@app.route('/')
def home(): 
    #return render_template("index.html", token="Hello Flask+React")
    return jsonify({'poruka' : 'Dobrodosli na pocetnu stranicu'},{'sve knjige' : "http://localhost:5000/knjiga", 'dodaj knjigu[POST]' : "http://localhost:5000/knjiga", 'dodaj izdavatelja[POST]' : "http://localhost:5000/izdavatelj", 'svi izdavatelji' : "http://localhost:5000/izdavatelj", 'dodaj nakladnika[POST]' : "http://localhost:5000/nakladnik", 'svi nakladnici[GET]' : "http://localhost:5000/nakladnik", 'dodaj izdavanje[POST]' : "http://localhost:5000/izdavanje", 'sva izdavanja' : "http://localhost:5000/izdavanje"  })


@app.route('/knjiga', methods=["GET"])
def sve_knjige_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knjiga")
    knjiga = cursor.fetchall()
    conn.commit()
    payload = []
    content = {}
    for result in knjiga:
       content = {'sifra': result[0], 'Naslov': result[1], 'Zanr': result[2], 'Autor' : result[3], 'nakladnik' : result[4]}
       payload.append(content)
       content = {}
    return jsonify(payload)
    #return render_template("index.html", knjiga=knjiga)
    #return jsonify({'knjiga' : knjiga})


    #return jsoify(json.dumps(listKnjiga))
    #return jsonify({'knjiga' : knjiga})

'''@app.route('/knjiga/<sifra>', methods=["GET"])
def jedna_knjiga_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    knjiga = cursor.execute("SELECT * FROM knjiga where sifra = %s", sifra)
    knjiga = cursor.fetchone()
    return render_template("knjigasifra.html", knjiga=knjiga)

@app.route('/knjiga', methods=["GET"])
def sve_knjige_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knjiga")
    knjiga = cursor.fetchall()
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'dodaj knjigu[POST]' : "http://localhost:5000/knjiga"}, {'knjiga' : knjiga})
'''
@app.route('/knjiga/<sifra>', methods=["GET"])
def jedna_knjiga_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knjiga where sifra = %s", sifra)
    knjiga = cursor.fetchall()
    conn.commit()
    payload = []
    content = {}
    for result in knjiga:
       content = {'sifra': result[0], 'Naslov': result[1], 'Zanr': result[2], 'Autor' : result[3], 'nakladnik' : result[4]}
       payload.append(content)
       content = {}
    return jsonify(payload)



@app.route('/knjiga', methods=["POST"])
def dodavanje_knjige():
    naslov = request.json.get('Naslov', None)
    zanr = request.json.get('Zanr', None)
    autor = request.json.get('Autor', None)
    nakladnik = request.json.get('nakladnik', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO knjiga (Naslov,Zanr,Autor,nakladnik) VALUES (%s,%s,%s,%s)", (naslov,zanr,autor,nakladnik))
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'sve knjige[GET]' : "http://localhost:5000/knjiga"},{'obavijest' : "Nova knjiga dodana"})

@app.route('/knjiga/<sifra>', methods=["PUT"])
def edit_knjige(sifra):
    naslov = request.json.get('Naslov', None)
    zanr = request.json.get('Zanr', None)
    autor = request.json.get('Autor', None)
    nakladnik = request.json.get('nakladnik', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE knjiga SET Naslov=%s, Zanr=%s, Autor=%s, nakladnik=%s WHERE sifra =%s", (naslov, zanr, autor, nakladnik, sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'sve knjige[GET]' : "http://localhost:5000/knjiga"},{'obavijest' : "Knjiga je uredena"})

'''@app.route('/knjiga/<sifra>', methods=["DELETE"])
def brisanje_knjige(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM knjiga WHERE sifra=%s", sifra)
    conn.commit()
    return ("Knjiga je obrisana")
'''

@app.route('/izdavatelj', methods=["GET"])
def svi_izdavatelji_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM izdavatelj")
    payload = []
    content = {}
    izdavatelj = cursor.fetchall()
    conn.commit()
    for result in izdavatelj:
        content = {'sifra': result[0], 'Ime': result[1], 'Prezime': result[2], 'Adresa': result[3], 'Mjesto' : result[4], 'Postanski_broj' : result[5]}
        payload.append(content)
        content = {}
    return jsonify(payload)
    #return jsonify({ 'home' : "http://localhost:5000", 'dodaj izdavatelja[POST]' : "http://localhost:5000/izdavatelj"}, {'izdavatelji' : izdavatelj})

@app.route('/izdavatelj/<sifra>', methods=["GET"])
def jedan_izdavatelj_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavatelj = cursor.execute("SELECT * FROM izdavatelj where sifra = %s", sifra)
    payload = []
    content = {}
    izdavatelj = cursor.fetchall()
    conn.commit()
    for result in izdavatelj:
        content = {'sifra': result[0], 'Ime': result[1], 'Prezime': result[2], 'Adresa': result[3], 'Mjesto' : result[4], 'Postanski_broj' : result[5]}
        payload.append(content)
        content = {}
    return jsonify(payload)
    #return jsonify({ 'home' : "http://localhost:5000", 'svi izdavatelji' : "http://localhost:5000/izdavatelj"}, {'izdavatelj' : izdavatelj})

@app.route('/izdavatelj/<sifra>/knjiga', methods=["GET"])
def popis_posudenih_knjiga_za_izdavatelja(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavatelj_knjiga = cursor.execute("select c.naslov, c.zanr, c.autor from izdavatelj a inner join izdavanje b on b.izdavatelj = a.sifra inner join knjiga c on c.sifra = b.knjiga where a.sifra = %s", sifra)
    izdavatelj_knjiga = cursor.fetchall()
    return jsonify({ 'home' : "http://localhost:5000", 'svi izdavatelji' : "http://localhost:5000/izdavatelj"},{'izdavatelj_knjiga' : izdavatelj_knjiga})

@app.route('/izdavatelj/<sifra>/knjiga/<sifra1>', methods=["GET"])
def popis_konkretne_knjige_za_izdavatelja(sifra,sifra1):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavatelj_knjiga_id = cursor.execute("select c.naslov, c.zanr, c.autor from izdavatelj a inner join izdavanje b on b.izdavatelj = a.sifra inner join knjiga c on c.sifra = b.knjiga where a.sifra = %s and c.sifra=%s", (sifra,sifra1))
    izdavatelj_knjiga_id = cursor.fetchall()
    return jsonify({ 'home' : "http://localhost:5000", 'izdavatelj/<sifra>/knjiga' : "http://localhost:5000/izdavatelj/sifra/knjiga"},{'izdavatelj_knjiga' : izdavatelj_knjiga_id})

@app.route('/izdavatelj/<sifra>/izdavanje', methods=["GET"])
def popis_svih_izdavanja_izdavatelja(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavatelj_sva_izdavanja = cursor.execute("select b.sifra, b.datum_izdavanja, b.datum_povratka, cijena from izdavatelj a inner join izdavanje b on b.izdavatelj = a.sifra where a.sifra = %s", (sifra))
    izdavatelj_sva_izdavanja = cursor.fetchall()
    return jsonify({ 'home' : "http://localhost:5000", 'svi izdavatelji' : "http://localhost:5000/izdavatelj"},{'izdavatelj_sva_izdavanja' : izdavatelj_sva_izdavanja})

@app.route('/izdavatelj/<sifra>/izdavanje/<sifra1>', methods=["GET"])
def popis_konkretnog_izdavanja_izdavatelja(sifra,sifra1):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavatelj_konkretno_izdavanje = cursor.execute("select b.sifra, b.datum_izdavanja, b.datum_povratka, b.cijena from izdavatelj a inner join izdavanje b on b.izdavatelj = a.sifra where a.sifra = %s and b.sifra = %s", (sifra,sifra1))
    izdavatelj_konkretno_izdavanje = cursor.fetchall()
    return jsonify({ 'home' : "http://localhost:5000", 'izdavatelj/<sifra>/izdavanje' : "http://localhost:5000/izdavatelj/sifra/izdavanje"},{'izdavatelj_konkretno_izdavanje' : izdavatelj_konkretno_izdavanje})

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
    return jsonify({ 'home' : "http://localhost:5000", 'svi izdavatelji[GET]' : "http://localhost:5000/izdavatelj"},{'obavijest' : "Novi izdavatelj dodan"})

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
    return jsonify({ 'home' : "http://localhost:5000", 'svi izdavatelji[GET]' : "http://localhost:5000/izdavatelj"},{'obavijest' : "Izdavatelj je ureden"})

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
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    payload = []
    content = {}
    nakladnik = cursor.fetchall()
    conn.commit()
    for result in nakladnik:
        content = {'sifra': result[0], 'Naziv': result[1], 'Mjesto': result[2]}
        payload.append(content)
        content = {}
    return jsonify(payload)
    #return jsonify({ 'home' : "http://localhost:5000", 'dodaj nakladnika[POST]' : "http://localhost:5000/nakladnik"}, {'nakladnici' : nakladnik})

@app.route('/nakladnik/<sifra>', methods=["GET"])
def jedan_nakladnik_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    nakladnik = cursor.execute("SELECT * FROM nakladnik where sifra = %s", sifra)
    payload = []
    content = {}
    nakladnik = cursor.fetchall()
    conn.commit()
    for result in nakladnik:
        content = {'sifra': result[0], 'Naziv': result[1], 'Mjesto': result[2]}
        payload.append(content)
        content = {}
    return jsonify(payload)
    #nakladnici = []
    #for nakladnik in nakladnik.query.all():
    #    nakladnici.append({
    #        'sifra': nakladnik.sifra,
    #        'Naziv': nakladnik.Naziv,
    #        'Mjesto': nakladnik.Mjesto
    #    })

    #return jsonify({"sifra": nakladnik[0], "Naziv" : nakladnik[1], "Mjesto" : nakladnik[2]})
    
    #return json.dumps(nakladnik)

@app.route('/nakladnik', methods=["POST"])
def dodavanje_nakladnik():
    naziv = request.json.get('Naziv', None)
    mjesto = request.json.get('Mjesto', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nakladnik (Naziv, Mjesto) VALUES (%s,%s)", (naziv,mjesto))
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'svi nakladnici[GET]' : "http://localhost:5000/nakladnik"}, {'obavijest' : 'Novi nakladnik dodan'})

@app.route('/nakladnik/<sifra>', methods=["PUT"])
def edit_nakladnik(sifra):
    naziv = request.json.get('Naziv', None)
    mjesto = request.json.get('Mjesto', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE nakladnik SET Naziv=%s, Mjesto=%s WHERE sifra =%s", (naziv,mjesto,sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'svi nakladnici[GET]' : "http://localhost:5000/nakladnik"}, {'obavijest' : 'Nakladnik je ureden'})
'''
@app.route('/nakladnik/<sifra>', methods=["DELETE"])
def brisanje_nakladnik(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nakladnik WHERE sifra=%s", sifra)
    conn.commit()
    return ("nakladnik je obrisan")
'''
@app.route('/izdavanje', methods=["GET"])
def sva_izdavanja_prikaz():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM izdavanje")
    izdavanje = cursor.fetchall()
    conn.commit()
    payload = []
    content = {}
    for result in izdavanje:
       content = {'sifra': result[0], 'datum_izdavanja': result[1], 'datum_povratka': result[2], 'cijena' : result[3], 'izdavatelj' : result[4], 'knjiga' :result[5]}
       payload.append(content)
       content = {}
    return jsonify(payload)
    #return jsonify({ 'home' : "http://localhost:5000", 'dodaj izdavanje[POST]' : "http://localhost:5000/izdavanje"}, {'izdavanje' : izdavanje})

@app.route('/izdavanje/<sifra>', methods=["GET"])
def jedno_izdavanje_prikaz(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    izdavanje = cursor.execute("SELECT * FROM izdavanje where sifra = %s", sifra)
    izdavanje = cursor.fetchall()
    conn.commit()
    payload = []
    content = {}
    for result in izdavanje:
       content = {'sifra': result[0], 'datum_izdavanja': result[1], 'datum_povratka': result[2], 'cijena' : result[3], 'izdavatelj' : result[4], 'knjiga' :result[5]}
       payload.append(content)
       content = {}
    return jsonify(payload)
    #return jsonify({ 'home' : "http://localhost:5000", 'sva izdavanja' : "http://localhost:5000/izdavanje"}, {'izdavanje' : izdavanje})

@app.route('/izdavanje', methods=["POST"])
def dodavanje_izdavanje():
    datum_izdavanja = request.json.get('datum_izdavanja', None)
    datum_povratka = request.json.get('datum_povratka', None)
    cijena = request.json.get('cijena', None)
    izdavatelj = request.json.get('izdavatelj', None)
    knjiga = request.json.get('knjiga', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO izdavanje (datum_izdavanja, datum_povratka, cijena, izdavatelj, knjiga) VALUES (%s,%s,%s,%s,%s)", (datum_izdavanja,datum_povratka,cijena,izdavatelj,knjiga))
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'sva izdavanja[GET]' : "http://localhost:5000/izdavanje"}, {'obavijest' : 'Novo izdavanje je dodano'})

@app.route('/izdavanje/<sifra>', methods=["PUT"])
def edit_izdavanje(sifra):
    datum_izdavanja = request.json.get('datum_izdavanja', None)
    datum_povratka = request.json.get('datum_povratka', None)
    cijena = request.json.get('cijena', None)
    izdavatelj = request.json.get('izdavatelj', None)
    knjiga = request.json.get('knjiga', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE izdavanje SET datum_izdavanja=%s, datum_povratka=%s, cijena=%s, izdavatelj=%s, knjiga=%s WHERE sifra=%s", (datum_izdavanja,datum_povratka,cijena,izdavatelj,knjiga,sifra))
    cursor.fetchone()
    conn.commit()
    return jsonify({ 'home' : "http://localhost:5000", 'sva izdavanja[GET]' : "http://localhost:5000/izdavanje"}, {'obavijest' : 'Izdavanje je ureddeno'})
'''
@app.route('/izdavanje/<sifra>', methods=["DELETE"])
def brisanje_izdavanje(sifra):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM izdavanje WHERE sifra=%s", sifra)
    conn.commit()
    return ("Izdavanje je obrisano")
'''


if __name__ == '__main__':
    app.run(debug=True)