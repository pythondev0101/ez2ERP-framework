"""
app/__init__.py
====================================
Create our application
"""

from flask import Flask, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from config import app_config

# DEVELOPER-NOTE: -INCLUDE YOUR IMPORTS HERE-

#                  -END-

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
cors = CORS()
login_manager = LoginManager()

# DEVELOPER-NOTE: -INITIATE YOUR IMPORTS HERE-

#                   -END-


MODULES = []

SYSTEM_MODULES = []

CONTEXT = session

def internal_server_error(e):
    from flask import render_template
    return render_template('admin/internal_server_error.html'), 500


def create_app(config_name):
    """
    Return the app at crenecreate nito ang application
    ----------
    config_name
        A string para kung ano ang gagamiting environment configuration(eg.develop,production,testing)
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(app_config[config_name])
    app.register_error_handler(500, internal_server_error)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)

    # DEVELOPER-NOTE: -INITIALIZE YOUR IMPORTS HERE-

    #                    -END-

    login_manager.login_view = 'bp_auth.login'
    login_manager.login_message = "You must be logged in to access this page."

    with app.app_context():

        # DEVELOPER-NOTE: -IMPORT HERE THE SYSTEM MODULES-
        from app.core import bp_core
        from app.auth import bp_auth
        from app.admin import bp_admin
        # -Add here-
        #                   -END-

        # DEVELOPER-NOTE: -REGISTER HERE THE MODULE BLUEPRINTS-
        app.register_blueprint(bp_core, url_prefix='/')
        app.register_blueprint(bp_auth, url_prefix='/auth')
        app.register_blueprint(bp_admin, url_prefix='/admin')
        # -Add here-
        #               -END-

        # DEVELOPER-NOTE: -INCLUDE HERE YOUR MODULE Admin models FOR ADMIN TEMPLATE-
        from app.admin.admin import AdminModule
        from app.auth.auth import AuthModule
        # -Add here-
        #                  -END-
        
        # DEVELOPER-NOTE: -APPEND YOUR MODULE HERE-
        MODULES.append(AdminModule)
        MODULES.append(AuthModule)
        # -Add here-
        #                  -END-

        @app.before_first_request
        def setup_context():
            CONTEXT['system_modules'] = SYSTEM_MODULES
            CONTEXT['active']: str
            CONTEXT['errors']: dict
            CONTEXT['create_modal']: dict
            CONTEXT['header_color'] = 'header_color15' # Default color
            CONTEXT['sidebar_color'] = "sidebar_color15" # Default color
            CONTEXT['app_name'] = "Likes" # TODO

    return app
