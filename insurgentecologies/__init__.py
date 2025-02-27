# from flask import Flask

"""Initialize app."""
from flask import Flask
from flask_assets import Environment
from insurgentecologies.addagtech.models import db
from flask_redis import FlaskRedis
# from ddtrace import patch_all
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_migrate import Migrate 
from flask_bootstrap import Bootstrap

# patch_all()

# Globally accessible libraries
r = FlaskRedis()



def create_app():
    """Construct the core flask_wtforms_tutorial."""
    print(Config.SQLALCHEMY_DATABASE_URI)
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # app.config["RECAPTCHA_PARAMETERS"] = {"size": "100%"}
    images = UploadSet('images', IMAGES)
    configure_uploads(app, images)
    
    assets = Environment()  # Create an assets environment
    assets.init_app(app)  # Initialize Flask-Assets

    migrate = Migrate(app, db, render_as_batch=True)
    
    bootstrap = Bootstrap(app)

    db.init_app(app)


    with app.app_context():
        # Import parts of our flask_wtforms_tutorial
        from .assets import compile_static_assets
        from .addagtech import homeroutes

         # Register Blueprints
        app.register_blueprint(homeroutes.home_bp)

        # Compile static assets
        compile_static_assets(assets)  # Execute logic
        
        db.create_all()  # Create sql tables for our data models
       


        return app


