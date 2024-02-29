from .app import create_app
from dotenv import load_dotenv
load_dotenv()

app = create_app()

from .auth import auth  # noqa
app.register_blueprint(auth)

from .api import api  # noqa
app.register_blueprint(api)

from . import errorHandlers  # noqa
