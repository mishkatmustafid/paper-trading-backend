"""Application entry point: Main app"""

from app.server import init_server
from app.services import init_db

if __name__ == "__main__":
    init_db()
    init_server()
