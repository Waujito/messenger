from .chatSockets import MessagingNamespace
from flask_socketio import SocketIO

socketio = SocketIO()


socketio.on_namespace(MessagingNamespace('/chat'))
