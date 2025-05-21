from flask import Blueprint

# Create a Blueprint for admin functionalities
# The first argument 'admin' is the Blueprint's name, which is used by Flask's routing mechanism.
# The second argument __name__ helps Flask locate the Blueprint's resources (like templates and static files).
# url_prefix='/admin' means all routes defined in this blueprint will be prefixed with /admin.
bp = Blueprint('admin', __name__, url_prefix='/admin') # REMOVED template_folder='templates'

# Import routes at the end to avoid circular dependencies
from app.admin import routes