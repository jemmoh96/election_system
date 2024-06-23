from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    secret_voting_id = StringField('Voter ID', validators=[DataRequired()])
    security_answer = PasswordField('Security Answer', validators=[DataRequired()])
    submit = SubmitField('Login')

class VoteForm(FlaskForm):
    president = RadioField('President', choices=[], validators=[DataRequired()])
    governor = RadioField('Governor', choices=[], validators=[DataRequired()])
    senator = RadioField('Senator', choices=[], validators=[DataRequired()])
    women_rep = RadioField('County Women Representative', choices=[], validators=[DataRequired()])
    mp = RadioField('Member of Parliament', choices=[], validators=[DataRequired()])
    mca = RadioField('Member of County Assembly', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit Vote')
