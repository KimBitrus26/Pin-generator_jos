from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid #to generate a random pin security
import os

# init app object
app = Flask(__name__)

# set up database
app.config["SECRET_KEY"] = "123456KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///data.db"
app.config["DATABASE_TRACK_MODIFITION"] = False

# init db object
db = SQLAlchemy(app)

# create user class
class User(db.Model):
    __tablename__ = 'users'
    serial_number = db.Column(db.Integer, primary_key = True)
    pin = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, pin):
        self.pin = pin
db.create_all()

#index route
@app.route("/", methods=["GET"])
def index():
    return jsonify({"message":"Click Endpoint https://kimkazongapp.herokuapp.com/pin to generate pin AND Endpoint https://kimkazongapp.herokuapp/<string:serial_number> to validate pin"})


#generating a pin
@app.route("/pin", methods=["GET"])
def  create_a_pin():
    pinLength = 15
    user = User(pin=str(uuid.uuid4().int)[0:pinLength])
    db.session.add(user)
    db.session.commit()
    return jsonify({"PIn_generated:": user.pin, "Serial_number:": user.serial_number})

# validating a valid pin
@app.route("/<string:serial_number>", methods=["GET"])
def  get_a_pin(serial_number):
    pinNum = User.query.filter_by(serial_number=serial_number).first()
    if not pinNum:
        return jsonify({"msg":"Oops! Wrong PIN, try again"})
    
    return jsonify({"msg":"Valid PIN"})

# run server
if __name__ == "__main__":
    app.run(debug=True)
