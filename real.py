from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid #to generate a random pin security


# init app object
app = Flask(__name__)


# set up database
app.config["SECRET_KEY"] = "123456KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
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


#route
@app.route("/pin", methods=["POST"])
def  create_a_pin():
    pinLength = 15
    user = User(pin=str(uuid.uuid4().hex).upper()[0:pinLength])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg":"Pin created"})

# validating a valid pin
@app.route("/pin/<string:serial_number>", methods=["GET"])
def  get_a_pin(serial_number):
    pinNum = User.query.filter_by(serial_number=serial_number).first()
    if not pinNum:
        return jsonify({"msg":"Invalid pin"})
       
    pin_data = {}
    pin_data['serial_number'] = pinNum.serial_number
    pin_data['pin'] = pinNum.pin

    return jsonify({'Valid pin':pin_data})



# run server
if __name__ == "__main__":
    app.run(debug=True)
