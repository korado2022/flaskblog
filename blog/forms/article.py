from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators



class CreateArticleForm(FlaskForm):
    title = StringField('Title',[validators.DataRequired()])
    text = TextAreaField('Text', [validators.DataRequired()])
    submit = SubmitField('Create')