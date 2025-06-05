from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    # Get all events for display
    events = db.session.scalars(db.select(Event)).all()
    
    # Separate featured events (first 3) and upcoming events
    featured_events = events[:3] if events else []
    upcoming_events = events[3:] if len(events) > 3 else []
    
    return render_template('index.html', 
                         featured_events=featured_events, 
                         upcoming_events=upcoming_events)

@mainbp.route('/search')
def search():
    if request.args.get('search') and request.args['search'].strip() != "":
        search_term = request.args['search'].strip()
        print(f"Searching for: {search_term}")
        
        # Search in event name and description
        query = "%" + search_term + "%"
        events = db.session.scalars(
            db.select(Event).where(
                db.or_(
                    Event.name.like(query),
                    Event.description.like(query),
                    Event.category.like(query),
                    Event.venue_name.like(query)
                )
            )
        ).all()
        
        # Separate for display
        featured_events = events[:3] if events else []
        upcoming_events = events[3:] if len(events) > 3 else []
        
        return render_template('index.html', 
                             featured_events=featured_events, 
                             upcoming_events=upcoming_events,
                             search_term=search_term)
    else:
        return redirect(url_for('main.index'))

@mainbp.route('/category/<category>')
def filter_by_category(category):
    if category.lower() == 'all':
        return redirect(url_for('main.index'))
    
    # Filter events by category
    events = db.session.scalars(
        db.select(Event).where(Event.category == category.lower())
    ).all()
    
    # Separate for display
    featured_events = events[:3] if events else []
    upcoming_events = events[3:] if len(events) > 3 else []
    
    return render_template('index.html', 
                         featured_events=featured_events, 
                         upcoming_events=upcoming_events,
                         selected_category=category)