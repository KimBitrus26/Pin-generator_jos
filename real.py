from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid #to generate a random pin security


# init app object
app = Flask(__name__)
api = Api(app)

# set up database
app.config["SECRET_KEY"] = "123456KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["DATABASE_TRACK_MODIFITION"] = False

# init db object
db = SQLAlchemy(app)

#  create user class
class User(db.Model):
    __tablename__ = 'users'
    serial_number = db.Column(db.Integer, primary_key = True)
    pin = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, pin):
        self.pin = pin
db.create_all()


#route
@app.route("/pin", methods=["POST"])
def  create_pin():
    data = request.get_json()
    item = {
            
            "pin" : data["pin"]}
    pinLength = 15
    randompPin = uuid.uuid4().hex
    randompPin = randompPin.upper()[0:pinLength]
    item = randompPin
    user = User(pin=item)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg":"pin created"})

# validating a valid pin
@app.route("/pin/<string:serial_number>", methods=["POST"])
def  get_a_pin(serial_number):
    pinNumber = User.query.filter_by(serial_number=serial_number).first()
    if pinNumber:
        return jsonify({'msg':'Valid pin number '})
    

    return jsonify({'msg': 'Invalid pin number'})


# run server
if __name__ == "__main__":
    app.run(debug=True)