from flask import Flask, jsonify, request
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()


app.config['MYQSL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'andibasic'
app.config['MYSQL_DATABASE_DB'] = 'knjiznica'
app.config['MYASQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/knjige', methods=["GET"])
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


if __name__ == '__main__':
    app.run(debug=True)