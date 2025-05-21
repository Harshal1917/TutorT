from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SubjectForm(FlaskForm):
    name = StringField('Subject Name',
                       validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description',
                                validators=[Length(max=500)]) # Optional description
    category = StringField('Category',
                         validators=[Length(max=50)]) # e.g., Programming, Science, Arts
    submit = SubmitField('Add Subject')