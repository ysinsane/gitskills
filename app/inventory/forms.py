from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,IntegerField,FileField
class SearchRecordForm(FlaskForm):
    keyword=StringField("Please input a keyword for search!")
    username=StringField("Please input a username!")
    submit=SubmitField('Search')

class SearchForm(FlaskForm):
    keyword=StringField("Please input a keyword for search!")
    submit=SubmitField('Search')

class Take_comfirmForm(FlaskForm):
    num=IntegerField(validators=[DataRequired()])
    customer_name=StringField('Customer Name')
    submit=SubmitField('Take')

class FileForm(FlaskForm):
    file=FileField()
    submit=SubmitField('上传')