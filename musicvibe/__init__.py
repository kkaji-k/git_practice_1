from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Initialize extensions
    Bootstrap5(app)
    Bcrypt(app)

    # Secret key for session management
    app.secret_key = 'musicvibe-secret-key-2025'

    # Configure and initialize database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicvibedb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Configure upload folder
    UPLOAD_FOLDER = '/static/img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.init_app(app)

    # Create user loader function
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))

    # Register Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    
    from . import events
    app.register_blueprint(events.eventbp)
    
    from . import auth
    app.register_blueprint(auth.authbp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error=e), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html", error=e), 500

    # Context processor for template variables
    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    return app