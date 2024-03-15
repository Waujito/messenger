from .chatSockets import MessagingNamespace
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")


socketio.on_namespace(MessagingNamespace('/chat'))
