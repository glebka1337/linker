import uuid
import aio_pika
import pytest
from aio_pika import Message, connect_robust
from test.docker.rabbit import (
    RABBITMQ_DEFAULT_USER,
    RABBITMQ_DEFAULT_PASS
)
@pytest.mark.asyncio
async def test_simple_message_sent(
    rabbitmq_container
):
    # 1. Send message
    
    conn: aio_pika.abc.AbstractRobustConnection = await connect_robust(
        url=f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@127.0.0.1/"
    )
    
    queue_name = 'test_q'
    routing_key = 'test_q'
    
    ch = await conn.channel()
    
    queue = await ch.declare_queue(name=queue_name)
    ex = await ch.declare_exchange('direct', auto_delete=True)
    
    await queue.bind(routing_key=routing_key, exchange=ex)
    
    msg = bytes(str(uuid.uuid4()).encode())
    
    await ex.publish(
        Message(
            body=msg
        ),
        routing_key=routing_key
    )
    
    # Receive message
    
    msg_from_queue = await queue.get(timeout=5)
    
    assert msg_from_queue.body == msg
    
    await msg_from_queue.ack()
    
    await queue.delete()
    await ch.close()
    await conn.close()
