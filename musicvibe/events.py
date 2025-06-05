from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from .models import Event, Comment, Booking, User
from .forms import EventForm, EventUpdateForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<int:id>')
def show(id):
    # Get event by id with 404 handling
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)
    
    # Create comment form
    comment_form = CommentForm()
    
    # Get comments for this event
    comments = db.session.scalars(
        db.select(Comment).where(Comment.event_id == id).order_by(Comment.created_at.desc())
    ).all()
    
    return render_template('events/show.html', 
                         event=event, 
                         form=comment_form, 
                         comments=comments)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    
    if form.validate_on_submit():
        # Handle file upload
        db_file_path = check_upload_file(form)
        
        # Create datetime objects from date and time fields
        start_datetime = datetime.combine(form.date.data, form.start_time.data)
        end_datetime = datetime.combine(form.date.data, form.end_time.data)
        
        # Create new event
        event = Event(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            date=form.date.data,
            start_time=start_datetime,
            end_time=end_datetime,
            venue_name=form.venue_name.data,
            venue_address=form.venue_address.data,
            capacity=form.capacity.data,
            standard_price=form.standard_price.data,
            vip_price=form.vip_price.data or 0,
            backstage_price=form.backstage_price.data or 0,
            tickets_available=form.capacity.data,  # Initially all tickets available
            status='Open',
            image=db_file_path,
            organizer_name=form.organizer_name.data,
            organizer_email=form.organizer_email.data,
            organizer_phone=form.organizer_phone.data,
            user_id=current_user.id
        )
        
        # Add to database
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('event.show', id=event.id))
    
    return render_template('events/create.html', form=form)

@eventbp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    # Get event and check ownership
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)
    
    if event.user_id != current_user.id:
        flash('You can only edit your own events', 'error')
        return redirect(url_for('event.show', id=id))
    
    form = EventUpdateForm(obj=event)
    
    if form.validate_on_submit():
        # Handle file upload if new image provided
        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path
        
        # Update event fields
        event.name = form.name.data
        event.description = form.description.data
        event.category = form.category.data
        event.date = form.date.data
        event.start_time = datetime.combine(form.date.data, form.start_time.data)
        event.end_time = datetime.combine(form.date.data, form.end_time.data)
        event.venue_name = form.venue_name.data
        event.venue_address = form.venue_address.data
        event.capacity = form.capacity.data
        event.standard_price = form.standard_price.data
        event.vip_price = form.vip_price.data or 0
        event.backstage_price = form.backstage_price.data or 0
        event.organizer_name = form.organizer_name.data
        event.organizer_email = form.organizer_email.data
        event.organizer_phone = form.organizer_phone.data
        event.updated_at = datetime.now()
        
        db.session.commit()
        
        flash('Event updated successfully!', 'success')
        return redirect(url_for('event.show', id=event.id))
    
    return render_template('events/edit.html', form=form, event=event)

@eventbp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    # Get event and check ownership
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)
    
    if event.user_id != current_user.id:
        flash('You can only cancel your own events', 'error')
        return redirect(url_for('event.show', id=id))
    
    # Update event status
    event.status = 'Cancelled'
    event.updated_at = datetime.now()
    db.session.commit()
    
    flash('Event has been cancelled', 'info')
    return redirect(url_for('event.show', id=id))

@eventbp.route('/<int:id>/comment', methods=['POST'])
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    
    if not event:
        abort(404)
    
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            event_id=id,
            user_id=current_user.id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        flash('Your comment has been added!', 'success')
    
    return redirect(url_for('event.show', id=id))

@eventbp.route('/<int:id>/book', methods=['POST'])
@login_required
def book(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if not event:
        abort(404)
    
    # Get booking details from form
    ticket_type = request.form.get('ticket_type', 'Standard')
    quantity = int(request.form.get('quantity', 1))
    
    # Calculate total cost
    ticket_price = event.get_ticket_price(ticket_type)
    total_cost = ticket_price * quantity
    
    # Check ticket availability
    if event.tickets_available < quantity:
        flash('Not enough tickets available', 'error')
        return redirect(url_for('event.show', id=id))
    
    # Create booking
    booking = Booking(
        user_id=current_user.id,
        event_id=id,
        ticket_type=ticket_type,
        quantity=quantity,
        total_cost=total_cost,
        status='Confirmed'
    )
    
    # Update tickets available
    event.tickets_available -= quantity
    if event.tickets_available <= 0:
        event.status = 'Sold Out'
    
    db.session.add(booking)
    db.session.commit()
    
    flash(f'Booking confirmed! Your booking ID is {booking.booking_id}', 'success')
    return redirect(url_for('event.booking_history'))

@eventbp.route('/booking-history')
@login_required
def booking_history():
    # Get user's bookings
    bookings = db.session.scalars(
        db.select(Booking).where(Booking.user_id == current_user.id)
        .order_by(Booking.booking_date.desc())
    ).all()
    
    return render_template('events/booking_history.html', bookings=bookings)

@eventbp.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = db.session.scalar(db.select(Booking).where(Booking.id == booking_id))
    if not booking or booking.user_id != current_user.id:
        abort(404)
    
    # Update booking status
    booking.status = 'Cancelled'
    
    # Return tickets to event
    event = booking.event
    event.tickets_available += booking.quantity
    if event.status == 'Sold Out':
        event.status = 'Open'
    
    db.session.commit()
    
    flash('Booking cancelled successfully', 'info')
    return redirect(url_for('event.booking_history'))

def check_upload_file(form):
    """Handle file upload and return database path"""
    fp = form.image.data
    filename = fp.filename
    
    # Get current path and create upload path
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    
    # Save file and return database path
    fp.save(upload_path)
    return secure_filename(filename)  # Just store filename, not full path