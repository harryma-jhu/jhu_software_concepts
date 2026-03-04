import os
import json
import pika
import psycopg
# Ensure your etl folder has an __init__.py for these imports to work
from etl.scrape import scrape_page, save_to_db 

# Configuration from Environment
DB_URL = os.getenv("DATABASE_URL")
RMQ_URL = os.getenv("RABBITMQ_URL")
EXCHANGE = "tasks"
QUEUE = "tasks_q"
ROUTING_KEY = "tasks"

def handle_scrape_new_data(conn, payload):
    """
    SHALL implement handle_scrape_new_data:
    Uses watermarks for idempotency and batch-inserts new records.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT last_seen FROM ingestion_watermarks WHERE source = 'scraper'")
        row = cur.fetchone()
        last_seen = row[0] if row else None

        print(f" [worker] Scraping records newer than: {last_seen}")
        
        # Fetch new records
        new_records = scrape_page(since=last_seen)

        if new_records:
            # Batch-insert with parameterized SQL (Logic inside save_to_db)
            # save_to_db should use: INSERT ... ON CONFLICT (url) DO NOTHING
            save_to_db(cur, new_records)
            
            # Advance the watermark to the max seen
            # Assuming 'date_added' or a similar sortable string is the key
            new_max = max(r.get('date_added') for r in new_records)
            cur.execute("""
                INSERT INTO ingestion_watermarks (source, last_seen, updated_at)
                VALUES ('scraper', %s, now())
                ON CONFLICT (source) DO UPDATE SET 
                    last_seen = EXCLUDED.last_seen, 
                    updated_at = now()
            """, (new_max,))
            print(f" [worker] Ingested {len(new_records)} records. Watermark: {new_max}")

def handle_recompute_analytics(conn, payload):
    """
    SHALL implement handle_recompute_analytics:
    Refreshes materialized views or summary tables.
    """
    with conn.cursor() as cur:
        print(" [worker] Refreshing analytics...")
        # Replace with your actual view or summary table refresh SQL
        cur.execute("REFRESH MATERIALIZED VIEW application_summaries;")

TASK_MAP = {
    "scrape_new_data": handle_scrape_new_data,
    "recompute_analytics": handle_recompute_analytics
}

def callback(ch, method, properties, body):
    """
    SHALL open a DB transaction per message and acknowledge only after commit.
    """
    try:
        message = json.loads(body)
        kind = message.get("kind")
        payload = message.get("payload", {})
        
        print(f" [received] Task: {kind}")

        with psycopg.connect(DB_URL) as conn:
            if kind in TASK_MAP:
                TASK_MAP[kind](conn, payload)
                
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(f" [success] Task {kind} committed and acked.")
            else:
                print(f" [!] Unknown task kind: {kind}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    except Exception as e:
        print(f" [!] Handler Error: {e}")
        # SHALL rollback (automatic via psycopg 'with') and nack(requeue=false)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    # Launch long-running process connecting to RabbitMQ
    params = pika.URLParameters(RMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # SHALL declare durable AMQP entities
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct", durable=True)
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=ROUTING_KEY)

    # SHALL set backpressure
    channel.basic_qos(prefetch_count=1)

    print(' [*] Worker waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue=QUEUE, on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    main()