from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contactnumber = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    events = db.relationship('Event', backref='creator', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f"User: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    venue_name = db.Column(db.String(200), nullable=False)
    venue_address = db.Column(db.String(500), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    standard_price = db.Column(db.Float, nullable=False)
    vip_price = db.Column(db.Float, nullable=True)
    backstage_price = db.Column(db.Float, nullable=True)
    tickets_available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open')  # Open, Inactive, Sold Out, Cancelled, Completed
    image = db.Column(db.String(400), nullable=False)
    organizer_name = db.Column(db.String(200), nullable=False)
    organizer_email = db.Column(db.String(100), nullable=False)
    organizer_phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy=True)

    @property
    def is_sold_out(self):
        return self.tickets_available <= 0

    @property
    def is_past_event(self):
        return self.date < datetime.now().date()

    def get_ticket_price(self, ticket_type):
        prices = {
            'Standard': self.standard_price,
            'VIP': self.vip_price,
            'Backstage': self.backstage_price
        }
        return prices.get(ticket_type, self.standard_price)

    def __repr__(self):
        return f"Event: {self.name}"

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(20), unique=True, nullable=False)
    ticket_type = db.Column(db.String(20), nullable=False)  # Standard, VIP, Backstage
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), nullable=False, default='Confirmed')  # Confirmed, Cancelled, Completed
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __init__(self, **kwargs):
        super(Booking, self).__init__(**kwargs)
        if not self.booking_id:
            # Generate booking ID like MV-12345678
            import random
            self.booking_id = f"MV-{random.randint(10000000, 99999999)}"

    def __repr__(self):
        return f"Booking: {self.booking_id}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"Comment by {self.user.name}: {self.text[:50]}..."