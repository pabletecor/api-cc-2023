import sqlite3
from flask import Flask
from flask_restx import Resource, Api, fields

def create_connection():
    db = sqlite3.connect('superheroes.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS superheroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            power TEXT NOT NULL
        );
        ''')
    db.commit()
    return db

def insert_data(conn):

    # Inserción de los datos
    conn.execute('''INSERT INTO superheroes (name, power)
    VALUES ('Superman', 'Super strength'),
        ('Spider-Man', 'Spider abilities'),
        ('Wonder Woman', 'Superhuman strength and agility'),
        ('Iron Man', 'Powered exoskeleton'),
        ('Hulk', 'Superhuman strength and invulnerability'),
        ('Black Widow', 'Expert martial artist');
    ''')

    conn.commit() 


app = Flask(__name__)
api = Api(app, title="API sobre Superhéroes")


class SuperheroResource(Resource):
    def get(self, superhero_id=None):
        connection = create_connection()
        if superhero_id:
            value = connection.execute("SELECT * FROM superheroes WHERE id = ?", (superhero_id,))
            superhero = value.fetchone()
            if superhero:
                return {'id': superhero[0], 'name': superhero[1], 'power': superhero[2]}
            else:
                return {'message': 'Superhéroe no encontrado'}, 404
        else:
            value = connection.execute("SELECT * FROM superheroes")
            superheroes = value.fetchall()
            return [{'id': superhero[0], 'name': superhero[1], 'power': superhero[2]} for superhero in superheroes]


Superhero = api.model('Superhero', {
    'superhero_id': fields.Integer(readOnly=True, description='Identificador del superhéroe'),
    'name': fields.String(required=True, description='Nombre del superhéroe'),
    'power': fields.String(required=True, description='Poder del superhéroe')
})


class SuperheroesResource(Resource):
    def get(self, superhero_id=None):
        connection = create_connection()
        if superhero_id:
            value = connection.execute("SELECT * FROM superheroes WHERE id = ?", (superhero_id,))
            superhero = value.fetchone()
            if superhero:
                return {'id': superhero[0], 'name': superhero[1], 'power': superhero[2]}
            else:
                return {'message': 'Superhéroe no encontrado'}, 404
        else:
            value = connection.execute("SELECT * FROM superheroes")
            superheroes = value.fetchall()
            return [{'id': superhero[0], 'name': superhero[1], 'power': superhero[2]} for superhero in superheroes]

    @api.expect(Superhero)
    def post(self):
        superhero = api.payload
        connection = create_connection()
        connection.execute("INSERT INTO superheroes (name, power) VALUES (?, ?)", (superhero['name'], superhero['power']))
        connection.commit()
        return {'message': 'El superhéroe se ha introducido correctamente'}, 201

    @api.expect(Superhero)
    def put(self, superhero_id):
        superhero = api.payload
        connection = create_connection()
        connection.execute("UPDATE superheroes SET name = ?, power = ? WHERE id = ?", (superhero['name'], superhero['power'], superhero_id))
        connection.commit()
        return {'id': superhero_id, 'name': superhero['name'], 'power': superhero['power']}

    def delete(self, superhero_id):
        connection = create_connection()
        connection.execute("DELETE FROM superheroes WHERE id = ?", (superhero_id,))
        connection.commit()
        return {'message': 'Superhéroe eliminado'}


api.add_resource(SuperheroesResource, '/superheroes', '/superheroes/<int:superhero_id>')

#DESCOMENTAR PARA AÑADIR VALORES DESDE UN INICIO
#connection = create_connection()
#insert_data(connection)

if __name__ == '__main__':
    app.run(debug=True)
    create_connection()