from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class BookingForm(FlaskForm):
    guest_name = StringField('Your Name', validators=[DataRequired()])
    
    room_type = SelectField('Room Type', choices=[
        ('Budget', 'Budget'),
        ('Suite', 'Suite'),
        ('Luxury', 'Luxury')
    ], validators=[DataRequired()])
    
    check_in = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    adults = IntegerField('Number of Adults', validators=[
        DataRequired(), NumberRange(min=1, message="At least one adult required")
    ])
    
    children = IntegerField('Number of Children', validators=[
        NumberRange(min=0)
    ])
    
    submit = SubmitField('Book Now')
