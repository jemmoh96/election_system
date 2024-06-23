from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    secret_voting_id = db.Column(db.String(100), unique=True, nullable=False)
    security_question = db.Column(db.String(100), nullable=False)
    security_answer_hash = db.Column(db.String(200), nullable=False)

    def set_security_answer(self, answer):
        self.security_answer_hash = generate_password_hash(answer)

    def check_security_answer(self, answer):
        return check_password_hash(self.security_answer_hash, answer)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voter.id'), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    encrypted_vote = db.Column(db.String(200), nullable=False)
