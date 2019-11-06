"""
Web Server entry point
"""
from src.core import Core


def init_server():
    core = Core()
    core.run()


if __name__ == '__main__':
    init_server()
