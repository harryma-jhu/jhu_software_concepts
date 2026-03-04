import pika, os, json
from datetime import datetime,timezone

def _open_channel():
    url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    # Idempotent declaration: makes sure the "pipe" exists
    channel.exchange_declare(exchange='tasks', exchange_type='direct', durable=True)
    channel.queue_declare(queue='tasks_q', durable=True)
    channel.queue_bind(exchange='tasks', queue='tasks_q', routing_key='tasks')
    
    return connection, channel

def publish_task(kind: str, payload: dict | None = None):
    body = json.dumps({
        "kind": kind,
        "ts": datetime.now(timezone.utc).isoformat(),
        "payload": payload or {}
    }, separators=(",", ":")).encode("utf-8")
    
    conn, ch = _open_channel()
    try:
        ch.basic_publish(
            exchange='tasks',
            routing_key='tasks',
            body=body,
            properties=pika.BasicProperties(delivery_mode=2) # Persistent message
        )
    except Exception as e:
    # Don't swallow errors - Flask needs to know to return a 503
        raise e
    finally:
        conn.close()