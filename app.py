"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "cupcakez"

connect_db(app)

@app.route('/')
def index():
  cupcakes = Cupcake.query.all()
  return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def get_all_cupcakes():
  all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
  return jsonify(all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
  new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"] or None)
  db.session.add(new_cupcake)
  db.session.commit()
  return (jsonify(cupcake=new_cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  cupcake.flavor = request.json.get('flavor', cupcake.flavor)
  cupcake.size = request.json.get('size', cupcake.size)
  cupcake.rating = request.json.get('rating', cupcake.rating)
  cupcake.image = request.json.get('image', cupcake.image)

  db.session.commit()
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  db.session.delete(cupcake)
  db.session.commit()
  return jsonify(message = "Deleted")