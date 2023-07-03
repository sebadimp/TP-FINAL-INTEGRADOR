from flask import Flask ,jsonify ,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sebadimp:milo1529@sebadimp.mysql.pythonanywhere-services.com/sebadimp$peliculas'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Pelicula(db.Model):   # la clase Producto hereda de db.Model
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    descripcion = db.Column(db.String(400))
    anio = db.Column(db.Integer)
    duracion = db.Column(db.Double)
    genero = db.Column(db.String(100))
    imagen = db.Column(db.String(400))
    def __init__(self,titulo,descripcion,anio,duracion,genero,imagen):   #crea el  constructor de la clase
        self.titulo = titulo
        self.descripcion = descripcion
        self.anio = anio
        self.duracion = duracion
        self.genero = genero
        self.imagen = imagen


    #  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class PeliculaSchema(ma.Schema):
    class Meta:
        fields=("id","titulo","descripcion","anio","duracion","genero","imagen")


pelicula_schema=PeliculaSchema()            # El objeto producto_schema es para traer un producto
peliculas_schema=PeliculaSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto


# crea los endpoint o rutas (json)
@app.route('/peliculas',methods=['GET'])
def get_Peliculas():
    all_peliculas=Pelicula.query.all()         # el metodo query.all() lo hereda de db.Model
    result=peliculas_schema.dump(all_peliculas)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla


@app.route('/peliculas/<id>',methods=['GET'])
def get_pelicula(id):
    pelicula=Pelicula.query.get(id)
    return pelicula_schema.jsonify(pelicula)   # retorna el JSON de un producto recibido como parametro


@app.route('/peliculas/<id>',methods=['DELETE'])
def delete_pelicula(id):
    pelicula=Pelicula.query.get(id)
    db.session.delete(pelicula)
    db.session.commit()
    return pelicula_schema.jsonify(pelicula)   # me devuelve un json con el registro eliminado

@app.route('/peliculas', methods=['POST']) # crea ruta o endpoint
def create_pelicula():
    #print(request.json)  # request.json contiene el json que envio el cliente
    titulo=request.json['titulo']
    descripcion=request.json['descripcion']
    anio=request.json['anio']
    duracion=request.json['duracion']
    genero=request.json['genero']
    imagen=request.json['imagen']
    new_pelicula=Pelicula(titulo,descripcion,anio,duracion,genero,imagen)
    db.session.add(new_pelicula)
    db.session.commit()
    return pelicula_schema.jsonify(new_pelicula)

@app.route('/peliculas/<id>' ,methods=['PUT'])
def update_pelicula(id):
    pelicula=Pelicula.query.get(id)

    pelicula.titulo=request.json['titulo']
    pelicula.descripcion=request.json['descripcion']
    pelicula.anio=request.json['anio']
    pelicula.duracion=request.json['duracion']
    pelicula.genero=request.json['genero']
    pelicula.imagen=request.json['imagen']

    db.session.commit()
    return pelicula_schema.jsonify(pelicula)

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''
# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)