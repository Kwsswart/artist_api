import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
    

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    """ Create application context """

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    with app.app_context():
        db.Model.metadata.reflect(db.engine)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.passphrase import bp as passphrase_bp
    app.register_blueprint(passphrase_bp)
    
    from app.scraper import bp as scraper_bp
    app.register_blueprint(scraper_bp)


    if not app.debug and not app.testing:
        # file based logger    
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '€(asctime)s €(levelname)s: €(message)s [in €pathnames:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
    
        app.logger.setLevel(logging.INFO)
        app.logger.info('API startup')
                    
    return app


from app import models