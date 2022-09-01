"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False
app.config['SECRET_KEY'] = "cupcakez"

connect_db(app)

@app.route('/')
def home_page():
  return render_template('home_page.html')

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
  new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"])
  db.session.add(new_cupcake)
  db.session.commit()
  response_json = jsonify(cupcake=new_cupcake.serialize())
  return jsonify(response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  cupcake.flavor = request.json.get('flavor', cupcake.flavor)
  cupcake.size = request.json.get('size', cupcake.size)
  cupcake.rating = request.json.get('rating', cupcake.rating)
  cupcake.image = request.json.get('image', cupcake.image)

  db.session.commit()
  return jsonify(cupcake=cupcake.serialize())

@app.route('api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
  cupcake = Cupcake.query.get_or_404(id)
  db.session.delete(cupcake)
  db.session.commit()
  return jsonify(message="Deleted")

  
#   Make routes for the following:

# PATCH /api/cupcakes/[cupcake-id]
# Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend.

# This should raise a 404 if the cupcake cannot be found.

# Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.

# DELETE /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.

# Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.

# Test these routes in Insomnia.