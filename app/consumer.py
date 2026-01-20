import pika
import time
import sys
import os

def callback(ch, method, properties, body):
    """Process received message"""
    print(f" [x] Received: {body.decode()}")

    # Simulate work (count dots in message)
    time.sleep(body.count(b'.'))

    print(" [x] Done")

    # Send acknowledgment
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Establish connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            credentials=pika.PlainCredentials(
                os.getenv('RABBITMQ_USER', 'guest'),
                os.getenv('RABBITMQ_PASS', 'guest')
            )
        )
    )
    channel = connection.channel()

    # Declare queue (idempotent - safe to call multiple times)
    channel.queue_declare(queue='task_queue', durable=True)

    # Fair dispatch - don't give more than one message to a worker at a time
    channel.basic_qos(prefetch_count=1)

    # Set up consumer
    channel.basic_consume(
        queue='task_queue',
        on_message_callback=callback,
        auto_ack=False  # Manual acknowledgment for reliability
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)