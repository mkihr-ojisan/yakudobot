from main import db
from flask_sqlalchemy import SQLAlchemy
import datetime


class YakudoScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    tweetid = db.Column(db.Text)
    score = db.Column(db.Float)
    date = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "YakudoScore!"


def init():
    db.create_all()