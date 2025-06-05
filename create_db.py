from musicvibe import db, create_app
from musicvibe.models import User, Event, Booking, Comment
from flask_bcrypt import generate_password_hash
from datetime import datetime

app = create_app()
ctx = app.app_context()
ctx.push()

# Create all tables
db.create_all()

# Create sample users
user1 = User(
    name='admin',
    firstname='Admin',
    lastname='User',
    emailid='admin@musicvibe.com',
    password_hash=generate_password_hash('password123'),
    contactnumber='0412345678',
    address='123 Admin St, Brisbane, QLD'
)

user2 = User(
    name='johndoe',
    firstname='John',
    lastname='Doe',
    emailid='john@example.com',
    password_hash=generate_password_hash('password123'),
    contactnumber='0423456789',
    address='456 Music Ave, Brisbane, QLD'
)

user3 = User(
    name='janesmith',
    firstname='Jane',
    lastname='Smith',
    emailid='jane@example.com',
    password_hash=generate_password_hash('password123'),
    contactnumber='0434567890',
    address='789 Concert Blvd, Brisbane, QLD'
)

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

# Create sample events
event1 = Event(
    name='Summer Rock Festival',
    description='Join us for the biggest rock festival of the summer! The Summer Rock Festival brings together the best rock bands for an unforgettable evening of music, energy, and fun.',
    category='rock',
    date=datetime(2025, 6, 15),
    start_time=datetime(2025, 6, 15, 18, 0),
    end_time=datetime(2025, 6, 15, 23, 0),
    venue_name='Riverside Arena',
    venue_address='123 River St, Brisbane, QLD',
    capacity=5000,
    standard_price=50.00,
    vip_price=120.00,
    backstage_price=200.00,
    tickets_available=4800,
    status='Open',
    image='rockfes.jpg',
    organizer_name='Rock Productions',
    organizer_email='info@rockproductions.com',
    organizer_phone='0712345678',
    user_id=1
)

event2 = Event(
    name='Jazz Night in the Park',
    description='An intimate evening of smooth jazz under the stars. Featuring world-class musicians in a beautiful outdoor setting.',
    category='jazz',
    date=datetime(2025, 7, 20),
    start_time=datetime(2025, 7, 20, 19, 0),
    end_time=datetime(2025, 7, 20, 22, 30),
    venue_name='City Park Amphitheater',
    venue_address='456 Park Ave, Brisbane, QLD',
    capacity=2000,
    standard_price=45.00,
    vip_price=90.00,
    backstage_price=150.00,
    tickets_available=0,
    status='Sold Out',
    image='jazz.jpg',
    organizer_name='Jazz Society Brisbane',
    organizer_email='events@jazzsociety.com.au',
    organizer_phone='0723456789',
    user_id=1
)

event3 = Event(
    name='Pop Stars Live',
    description='The hottest pop stars performing their biggest hits live! A night of unforgettable performances and incredible energy.',
    category='pop',
    date=datetime(2025, 8, 10),
    start_time=datetime(2025, 8, 10, 20, 0),
    end_time=datetime(2025, 8, 10, 23, 30),
    venue_name='Entertainment Centre',
    venue_address='789 Entertainment Blvd, Brisbane, QLD',
    capacity=8000,
    standard_price=65.00,
    vip_price=150.00,
    backstage_price=250.00,
    tickets_available=7500,
    status='Open',
    image='pop.jpg',
    organizer_name='Pop Entertainment',
    organizer_email='booking@popentertainment.com',
    organizer_phone='0734567890',
    user_id=2
)

event4 = Event(
    name='Symphony Orchestra',
    description='Experience the beauty of classical music with our world-renowned symphony orchestra performing timeless masterpieces.',
    category='classical',
    date=datetime(2025, 9, 5),
    start_time=datetime(2025, 9, 5, 19, 30),
    end_time=datetime(2025, 9, 5, 22, 0),
    venue_name='Concert Hall',
    venue_address='321 Symphony St, Brisbane, QLD',
    capacity=1500,
    standard_price=55.00,
    vip_price=110.00,
    backstage_price=180.00,
    tickets_available=1200,
    status='Open',
    image='orche.jpg',
    organizer_name='Brisbane Symphony',
    organizer_email='tickets@brisbanesymphony.org',
    organizer_phone='0745678901',
    user_id=1
)

event5 = Event(
    name='Electronic Music Festival',
    description='Dance the night away at the most electrifying electronic music festival featuring top DJs from around the world.',
    category='electronic',
    date=datetime(2025, 6, 25),
    start_time=datetime(2025, 6, 25, 21, 0),
    end_time=datetime(2025, 6, 26, 3, 0),
    venue_name='Festival Grounds',
    venue_address='567 Dance Ave, Brisbane, QLD',
    capacity=10000,
    standard_price=70.00,
    vip_price=160.00,
    backstage_price=280.00,
    tickets_available=9500,
    status='Cancelled',
    image='electronic.jpg',
    organizer_name='Electronic Events Co',
    organizer_email='info@electronicevents.com',
    organizer_phone='0756789012',
    user_id=2
)

event6 = Event(
    name='K-POP MAMA 2025',
    description='The biggest K-pop event of the year featuring your favorite K-pop stars and groups live on stage.',
    category='pop',
    date=datetime(2025, 3, 15),
    start_time=datetime(2025, 3, 15, 18, 30),
    end_time=datetime(2025, 3, 15, 23, 0),
    venue_name='Arena Stadium',
    venue_address='890 Kpop Plaza, Brisbane, QLD',
    capacity=12000,
    standard_price=80.00,
    vip_price=200.00,
    backstage_price=350.00,
    tickets_available=11500,
    status='Completed',
    image='kpop.jpg',
    organizer_name='KPOP Events Australia',
    organizer_email='events@kpopaus.com',
    organizer_phone='0767890123',
    user_id=3
)

db.session.add(event1)
db.session.add(event2)
db.session.add(event3)
db.session.add(event4)
db.session.add(event5)
db.session.add(event6)
db.session.commit()

# Create sample bookings
booking1 = Booking(
    user_id=2,
    event_id=1,
    ticket_type='VIP',
    quantity=2,
    total_cost=240.00,
    booking_date=datetime(2025, 3, 30, 14, 23),
    status='Confirmed'
)

booking2 = Booking(
    user_id=2,
    event_id=5,
    ticket_type='Standard',
    quantity=1,
    total_cost=70.00,
    booking_date=datetime(2025, 3, 25, 9, 45),
    status='Confirmed'
)

booking3 = Booking(
    user_id=3,
    event_id=6,
    ticket_type='VIP',
    quantity=3,
    total_cost=600.00,
    booking_date=datetime(2025, 1, 15, 20, 30),
    status='Completed'
)

db.session.add(booking1)
db.session.add(booking2)
db.session.add(booking3)
db.session.commit()

# Create sample comments
comment1 = Comment(
    text="I went to last year's festival and it was amazing! Looking forward to this year's lineup. The Midnight Rocks put on such an incredible show!",
    user_id=2,
    event_id=1,
    created_at=datetime(2025, 5, 25)
)

comment2 = Comment(
    text="Does anyone know if there's parking available at the venue? Or is it better to use public transport?",
    user_id=3,
    event_id=1,
    created_at=datetime(2025, 5, 26)
)

comment3 = Comment(
    text="Just got my tickets! VIP all the way. Can't wait to see Electric Tigers, they're my favorite band right now.",
    user_id=1,
    event_id=1,
    created_at=datetime(2025, 5, 27, 5, 0)
)

db.session.add(comment1)
db.session.add(comment2)
db.session.add(comment3)
db.session.commit()

print("Database created and populated with sample data!")
ctx.pop()