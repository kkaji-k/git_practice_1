from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create blueprint
authbp = Blueprint('auth', __name__)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        # Get form data
        username = register_form.user_name.data
        firstname = register_form.firstname.data
        lastname = register_form.lastname.data
        email = register_form.email_id.data
        contactnumber = register_form.contactnumber.data
        address = register_form.address.data
        password = register_form.password.data
        
        # Check if username already exists
        existing_user = db.session.scalar(db.select(User).where(User.name == username))
        if existing_user:
            flash('Username already exists, please choose another', 'error')
            return render_template('user.html', form=register_form, heading='Register')
        
        # Check if email already exists
        existing_email = db.session.scalar(db.select(User).where(User.emailid == email))
        if existing_email:
            flash('Email already registered, please use another email', 'error')
            return render_template('user.html', form=register_form, heading='Register')
        
        # Hash password and create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            name=username,
            firstname=firstname,
            lastname=lastname,
            emailid=email,
            contactnumber=contactnumber,
            address=address,
            password_hash=password_hash
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('user.html', form=register_form, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        username = login_form.user_name.data
        password = login_form.password.data
        
        # Find user in database
        user = db.session.scalar(db.select(User).where(User.name == username))
        
        if user is None:
            flash('Incorrect username or password', 'error')
        elif not check_password_hash(user.password_hash, password):
            flash('Incorrect username or password', 'error')
        else:
            # Login successful
            login_user(user)
            flash(f'Welcome back, {user.firstname}!', 'success')
            
            # Redirect to next page if it exists, otherwise to home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
    
    return render_template('user.html', form=login_form, heading='Log In')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('main.index'))