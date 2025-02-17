from flask import Blueprint

routes = Blueprint('routes', __name__)

from . import routes  # Import routes to register them with the blueprint
