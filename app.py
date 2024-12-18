from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notifications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
@app.route('/')
def home():
    return "welcome to the custom notification services!"

if __name__ == "__main__":
    app.run(debug=True)