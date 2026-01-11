from fastapi import Request
from aio_pika.abc import AbstractRobustConnection

def get_rabbitmq_connection(request: Request) -> AbstractRobustConnection:
    """
    Get a rabbitmq connection from app state
    """
    return request.app.state.resources.rabbitmq_conn