from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DateField, TimeField, IntegerField, FloatField, HiddenField
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange, Optional
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# User Registration Form
class RegisterForm(FlaskForm):
    user_name = StringField("Username", validators=[
        InputRequired(), 
        Length(min=4, max=25, message="Username must be between 4 and 25 characters")
    ])
    firstname = StringField("First Name", validators=[InputRequired()])
    lastname = StringField("Last Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
        Email("Please enter a valid email"),
        InputRequired()
    ])
    contactnumber = StringField("Contact Number", validators=[
        InputRequired(),
        Length(min=10, max=15, message="Please enter a valid phone number")
    ])
    address = StringField("Street Address", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=6, message="Password must be at least 6 characters long"),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

# User Login Form
class LoginForm(FlaskForm):
    user_name = StringField("Username", validators=[InputRequired('Enter username')])
    password = PasswordField("Password", validators=[InputRequired('Enter password')])
    submit = SubmitField("Login")

# Event Creation Form
class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Event Description', validators=[InputRequired()])
    category = SelectField('Event Category', 
                          choices=[('rock', 'Rock'), ('pop', 'Pop'), ('jazz', 'Jazz'), 
                                 ('classical', 'Classical'), ('electronic', 'Electronic'), 
                                 ('hiphop', 'Hip Hop'), ('other', 'Other')],
                          validators=[InputRequired()])
    date = DateField('Event Date', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    venue_name = StringField('Venue Name', validators=[InputRequired()])
    venue_address = StringField('Venue Address', validators=[InputRequired()])
    capacity = IntegerField('Venue Capacity', validators=[
        InputRequired(),
        NumberRange(min=1, message="Capacity must be at least 1")
    ])
    standard_price = FloatField('Standard Ticket Price ($)', validators=[
        InputRequired(),
        NumberRange(min=0, message="Price must be positive")
    ])
    vip_price = FloatField('VIP Ticket Price ($)', validators=[
        Optional(),
        NumberRange(min=0, message="Price must be positive")
    ])
    backstage_price = FloatField('Backstage Pass Price ($)', validators=[
        Optional(),
        NumberRange(min=0, message="Price must be positive")
    ])
    image = FileField('Event Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    organizer_name = StringField('Organizer Name', validators=[InputRequired()])
    organizer_email = StringField('Organizer Email', validators=[
        Email("Please enter a valid email"),
        InputRequired()
    ])
    organizer_phone = StringField('Organizer Phone', validators=[Optional()])
    submit = SubmitField("Create Event")

# Event Update Form (similar to create but without image requirement)
class EventUpdateForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired()])
    description = TextAreaField('Event Description', validators=[InputRequired()])
    category = SelectField('Event Category', 
                          choices=[('rock', 'Rock'), ('pop', 'Pop'), ('jazz', 'Jazz'), 
                                 ('classical', 'Classical'), ('electronic', 'Electronic'), 
                                 ('hiphop', 'Hip Hop'), ('other', 'Other')],
                          validators=[InputRequired()])
    date = DateField('Event Date', validators=[InputRequired()])
    start_time = TimeField('Start Time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    venue_name = StringField('Venue Name', validators=[InputRequired()])
    venue_address = StringField('Venue Address', validators=[InputRequired()])
    capacity = IntegerField('Venue Capacity', validators=[
        InputRequired(),
        NumberRange(min=1, message="Capacity must be at least 1")
    ])
    standard_price = FloatField('Standard Ticket Price ($)', validators=[
        InputRequired(),
        NumberRange(min=0, message="Price must be positive")
    ])
    vip_price = FloatField('VIP Ticket Price ($)', validators=[
        Optional(),
        NumberRange(min=0, message="Price must be positive")
    ])
    backstage_price = FloatField('Backstage Pass Price ($)', validators=[
        Optional(),
        NumberRange(min=0, message="Price must be positive")
    ])
    image = FileField('Event Image', validators=[
        Optional(),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')
    ])
    organizer_name = StringField('Organizer Name', validators=[InputRequired()])
    organizer_email = StringField('Organizer Email', validators=[
        Email("Please enter a valid email"),
        InputRequired()
    ])
    organizer_phone = StringField('Organizer Phone', validators=[Optional()])
    submit = SubmitField("Update Event")

# Comment Form
class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment', validators=[
        InputRequired(),
        Length(min=1, max=500, message="Comment must be between 1 and 500 characters")
    ])
    submit = SubmitField('Post Comment')

# Booking Form
class BookingForm(FlaskForm):
    ticket_type = HiddenField('Ticket Type', validators=[InputRequired()])
    quantity = HiddenField('Quantity', validators=[InputRequired()])
    total_amount = HiddenField('Total Amount', validators=[InputRequired()])
    
    # Payment fields
    card_name = StringField('Name on Card', validators=[InputRequired()])
    card_number = StringField('Card Number', validators=[
        InputRequired(),
        Length(min=13, max=19, message="Please enter a valid card number")
    ])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[
        InputRequired(),
        Length(min=5, max=5, message="Please enter date in MM/YY format")
    ])
    cvv = StringField('CVV', validators=[
        InputRequired(),
        Length(min=3, max=4, message="Please enter a valid CVV")
    ])
    email = StringField('Email', validators=[
        Email("Please enter a valid email"),
        InputRequired()
    ])
    submit = SubmitField('Confirm Booking')