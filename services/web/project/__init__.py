from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

class MessageModel(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(), nullable=False)

@app.route('/')
def index():
    return jsonify(message="You shall not see this path!")

@app.route('/message', methods=['POST'])
def saveMessage():
    if request.method == 'POST':
      if request.is_json:
        data = request.get_json()
        new_message = MessageModel(message=data['message'])
        db.session.add(new_message)
        db.session.commit()
        return jsonify(result="Message saved successfully.")
      else:
        return jsonify(result="Specified request payload was not in JSON format.")
