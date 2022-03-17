from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    team_leader = StringField('Team Leader ID', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Сollaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Sumbit')