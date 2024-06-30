# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def earthquakes_id(id):
    earthquakes = Earthquake.query.get(id)
    if earthquakes:
        earthquakes_data = {
            'id': earthquakes.id,
            'magnitude': earthquakes.magnitude,
            'location': earthquakes.location,
            'year': earthquakes.year
        }
        response = make_response(earthquakes_data, 200)
        return response
    else:
        response = make_response({'message': f'Earthquake {id} not found.'}, 404)
        return response
    

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def earthquakes_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]
    quakes_data = {
        'count': len(quakes),
        'quakes': quakes
    }        
    response = make_response(quakes_data, 200)
    return response
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
