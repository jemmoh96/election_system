from flask import Flask, render_template, redirect, url_for, flash, session
from config import Config
from models import db, Voter, Candidate, Vote
from forms import LoginForm, VoteForm
from flask_migrate import Migrate
import hashlib

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        voter = Voter.query.filter_by(secret_voting_id=form.secret_voting_id.data).first()
        if voter and voter.check_security_answer(form.security_answer.data):
            session['voter_id'] = voter.id
            return redirect(url_for('vote'))
        else:
            flash('Invalid Voter ID or Security Answer')
    return render_template('login.html', form=form)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'voter_id' not in session:
        return redirect(url_for('login'))

    form = VoteForm()
    form.president.choices = [(c.id, c.name + ' (' + c.party + ')') for c in Candidate.query.filter_by(position='President').all()]
    form.governor.choices = [(c.id, c.name + ' (' + c.party + ')') for c in Candidate.query.filter_by(position='Governor').all()]
    form.senator.choices = [(c.id, c.name + ' (' + c.party + ')') for c in Candidate.query.filter_by(position='Senator').all()]
    form.women_rep.choices = [(c.id, c.name + ' (' + c.party + ')') for c in Candidate.query.filter_by(position='County Women Representative').all()]
    form.mp.choices = [(c.id, c.name + ' (' + c.party + ')') for c in Candidate.query.filter_by(position='Member of Parliament').all()]
    form.mca.choices = [(c.id, c.name + ' (' + c.party + ')') for c in Candidate.query.filter_by(position='Member of County Assembly').all()]

    if form.validate_on_submit():
        votes = {
            'President': form.president.data,
            'Governor': form.governor.data,
            'Senator': form.senator.data,
            'County Women Representative': form.women_rep.data,
            'Member of Parliament': form.mp.data,
            'Member of County Assembly': form.mca.data
        }
        for position, candidate_id in votes.items():
            encrypted_vote = hashlib.sha256(f"{session['voter_id']},{position},{candidate_id}".encode()).hexdigest()
            vote = Vote(voter_id=session['voter_id'], position=position, candidate_id=candidate_id, encrypted_vote=encrypted_vote)
            db.session.add(vote)
        db.session.commit()
        flash('Your vote has been submitted!')
        return redirect(url_for('confirmation'))

    return render_template('vote.html', form=form)

@app.route('/confirmation')
def confirmation():
    if 'voter_id' not in session:
        return redirect(url_for('login'))
    return render_template('confirmation.html')

@app.route('/results')
def results():
    results = db.session.query(Vote.position, Vote.candidate_id, db.func.count(Vote.id).label('count')).group_by(Vote.position, Vote.candidate_id).all()
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
