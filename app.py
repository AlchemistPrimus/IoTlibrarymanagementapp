from flask import Flask
from views import routes
from extensions import db
from flask_login import LoginManager
from models import User


def create_app(settings="config.py"):
    """Factory function to start the web app when everthing(i.e configurations are set up in place.)"""
    app=Flask(__name__)#Creating app instance
    app.config.from_pyfile(settings)


    """Initializing extensions"""
    db.init_app(app)



    app.register_blueprint(routes)

    login_manager = LoginManager()
    login_manager.login_view = 'routes.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app.run(port=8080,debug=True)