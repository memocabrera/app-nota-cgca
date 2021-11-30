from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@localhost:5432/notas'
app.config['SQLALCHEMY_TRACK_MODIFTCATIONS']= False

class Notas(db.Model):
    __tablename__= "notas"
    idNota= db.Column(db.Integer, primary_key = True)
    tituloNota = db.Column(db.String(80))
    cuerpoNota = db.Column(db.String(80))

    def __init__(self,tituloNota,cuerpoNota):
        self.tituloNota = tituloNota
        self.cuerpoNota = cuerpoNota


@app.route('/')
def index():
    objeto = { "":  "", 
                "": ""
            }
    nombre = ""
    lista_nombres = ["", "", ""]
    return render_template("index.html", variable = lista_nombres )

@app.route("/about")
def about():
    return render_template ("about.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
    campotitulo  = request.form["campotitulo"]
    campocuerpo = request.form["campocuerpo"]
    print(campotitulo)
    print(campocuerpo)
    notaNueva = Notas(tituloNota=campotitulo, cuerpoNota=campocuerpo)
    db.session.add(notaNueva)
    db.session.commit()

    return render_template("index.html", titulo = campotitulo, cuerpo = campocuerpo)
    
@app.route("/leernotas")
def leernotas():
    conulta_notas= Notas.query.all()
    print(conulta_notas)
    for nota in conulta_notas:
        print(nota.tituloNota)
        print(nota.cuerpoNota)
    return render_template("leernota.html", constlta = conulta_notas)

@app.route("/eliminarnota/<id>")
def eliminar(id):
    nota = Notas.query.filter_by(idNota=int(id)).delete()
    print(nota)
    db.session.commit()
    return render_template("leernota.html")

@app.route("/editarnota/<id>")
def editar(id):
    nota = Notas.query.filter_by(idNota=int(id)).first()
    print(nota)
    print(nota.tituloNota)
    print(nota.cuerpoNota)
    return render_template("modificarNota.html", nota = nota)

@app.route("/modificarnota/", methods=['POST'])
def modificarnota():
    idnota = request.form['idnota']
    nuevo_titulo = request.form['campotitulo']
    nuevo_cuerpo = request.form['campocuerpo']
    nota = Notas.query.filter_by(idNota=int(idnota)).first()
    nota.tituloNota = nuevo_titulo
    nota.cuerpoNota = nuevo_cuerpo
    db.session.commit()
    return render_template("leernota.html")

if __name__ == "__main__":
    db.create_all() 
    app.run()